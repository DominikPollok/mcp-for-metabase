import pytest

from mcp_for_metabase.config import SqlGuardMode
from mcp_for_metabase.errors import SafetyError
from mcp_for_metabase.sql_guard import enforce_sql_guard, extract_sql_fragments


def test_extracts_native_sql_from_dataset_query() -> None:
    fragments = extract_sql_fragments(
        {
            "dataset_query": {
                "database": 1,
                "type": "native",
                "native": {"query": "select count(*) from orders"},
            },
        },
        operation_id="post_api_card",
        path="/api/card",
    )

    assert [(fragment.sql, fragment.require_read_only_start) for fragment in fragments] == [
        ("select count(*) from orders", True)
    ]


def test_allows_read_only_native_sql_and_metabase_template_tags() -> None:
    enforce_sql_guard(
        mode=SqlGuardMode.STRICT,
        operation_id="post_api_dataset",
        path="/api/dataset",
        body={
            "type": "native",
            "query": {
                "query": "with scoped as (select * from orders where status = {{status}}) "
                "select * from scoped [[where created_at >= {{created_at}}]]"
            },
        },
    )


def test_allows_semicolons_inside_string_literals() -> None:
    enforce_sql_guard(
        mode=SqlGuardMode.STRICT,
        operation_id="post_api_dataset",
        path="/api/dataset",
        body={"type": "native", "query": {"query": "select ';' as separator"}},
    )


@pytest.mark.parametrize(
    "sql",
    [
        "select * from orders; drop table orders",
        "select * from orders -- hide the rest",
        "select * from orders /* comment */",
        "delete from orders",
        "with deleted as (delete from orders returning *) select * from deleted",
        "select * into scratch_orders from orders",
        "select * from orders into outfile '/tmp/orders.csv'",
        "set role admin",
        "begin transaction",
    ],
)
def test_blocks_dangerous_native_sql(sql: str) -> None:
    with pytest.raises(SafetyError) as exc:
        enforce_sql_guard(
            mode=SqlGuardMode.STRICT,
            operation_id="post_api_dataset",
            path="/api/dataset",
            body={"type": "native", "query": {"query": sql}},
        )

    assert "Native SQL blocked" in str(exc.value)


def test_blocks_non_read_only_start_for_full_native_query() -> None:
    with pytest.raises(SafetyError) as exc:
        enforce_sql_guard(
            mode=SqlGuardMode.STRICT,
            operation_id="post_api_dataset",
            path="/api/dataset",
            body={"type": "native", "query": {"query": "from orders select *"}},
        )

    assert exc.value.response_body["first_token"] == "from"


def test_snippet_guard_allows_fragments_but_blocks_mutations() -> None:
    enforce_sql_guard(
        mode=SqlGuardMode.STRICT,
        operation_id="post_api_native_query_snippet",
        path="/api/native-query-snippet",
        body={"content": "where status = {{status}}"},
    )

    with pytest.raises(SafetyError):
        enforce_sql_guard(
            mode=SqlGuardMode.STRICT,
            operation_id="post_api_native_query_snippet",
            path="/api/native-query-snippet",
            body={"content": "where true; delete from orders"},
        )


def test_sql_guard_can_be_disabled() -> None:
    enforce_sql_guard(
        mode=SqlGuardMode.DISABLED,
        operation_id="post_api_dataset",
        path="/api/dataset",
        body={"type": "native", "query": {"query": "delete from orders"}},
    )
