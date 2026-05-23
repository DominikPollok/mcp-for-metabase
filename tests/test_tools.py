import httpx
import pytest
from pydantic import SecretStr

from mcp_for_metabase.client import MetabaseClient
from mcp_for_metabase.config import Settings, WriteMode
from mcp_for_metabase.errors import RegistryError, SafetyError
from mcp_for_metabase.tools import (
    add_dashboard_card,
    archive_card,
    archive_collection,
    archive_dashboard,
    clear_cache,
    collection_tree,
    copy_card,
    copy_dashboard,
    copy_document,
    create_api_key,
    create_bookmark,
    create_card_public_link,
    create_dashboard,
    create_dashboard_public_link,
    create_document,
    create_native_query_snippet,
    create_or_update_card,
    create_or_update_dashboard,
    create_or_update_native_query_snippet,
    create_pulse,
    create_segment,
    create_timeline,
    create_timeline_event,
    create_user,
    delete_api_key,
    delete_bookmark,
    delete_card,
    delete_card_public_link,
    delete_dashboard,
    delete_dashboard_public_link,
    delete_document,
    delete_pulse_subscription,
    delete_segment,
    delete_timeline,
    delete_timeline_event,
    discover_operations,
    get_cache_config,
    get_card,
    get_card_series,
    get_dashboard,
    get_dashboard_items,
    get_document,
    get_native_query_snippet,
    get_permission_group,
    get_permissions_graph,
    get_pulse,
    get_segment,
    get_setting,
    get_timeline,
    get_user,
    invalidate_cache,
    list_api_keys,
    list_bookmarks,
    list_databases,
    list_documents,
    list_native_query_snippets,
    list_permission_groups,
    list_pulses,
    list_revisions,
    list_segments,
    list_timelines,
    list_users,
    metabase_api_request,
    remove_dashboard_card,
    rescan_database_values,
    restore_snapshot,
    revert_revision,
    run_card_query,
    snapshot_entity,
    sync_database_schema,
    update_api_key,
    update_bookmark_ordering,
    update_cache_config,
    update_card,
    update_collection,
    update_dashboard_cards,
    update_dashboard_parameters,
    update_document,
    update_native_query_snippet,
    update_permissions_graph,
    update_pulse,
    update_segment,
    update_setting,
    update_timeline,
    update_timeline_event,
    update_user,
)


def make_client(handler: httpx.MockTransport) -> MetabaseClient:
    return MetabaseClient(
        Settings(
            METABASE_URL="http://metabase.test",
            METABASE_API_KEY=SecretStr("mb_key"),
            METABASE_MCP_WRITE_MODE=WriteMode.SAFE_WRITES,
        ),
        transport=handler,
    )


@pytest.mark.asyncio
async def test_create_dashboard_builds_expected_body() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["path"] = request.url.path
        seen["body"] = request.read().decode()
        return httpx.Response(200, json={"id": 12})

    client = make_client(httpx.MockTransport(handler))
    try:
        response = await create_dashboard(client, name="Revenue", collection_id=5)
    finally:
        await client.aclose()

    assert response["data"] == {"id": 12}
    assert seen["path"] == "/api/dashboard"
    assert '"name":"Revenue"' in str(seen["body"])


@pytest.mark.asyncio
async def test_generic_executor_uses_registry() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["path"] = request.url.path
        return httpx.Response(200, json={"id": 1})

    client = make_client(httpx.MockTransport(handler))
    try:
        await metabase_api_request(client, operation_id="post_api_dashboard", body={"name": "Ops"})
    finally:
        await client.aclose()

    assert seen == {"method": "POST", "path": "/api/dashboard"}


@pytest.mark.asyncio
async def test_generic_executor_validates_required_body_fields() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        with pytest.raises(RegistryError) as exc:
            await metabase_api_request(client, operation_id="post_api_dashboard", body={})
    finally:
        await client.aclose()

    assert exc.value.response_body == {
        "operation_id": "post_api_dashboard",
        "missing_path_parameters": [],
        "missing_query_parameters": [],
        "missing_body_fields": ["name"],
    }


@pytest.mark.asyncio
async def test_generic_executor_validates_openapi_schema() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        with pytest.raises(RegistryError) as exc:
            await metabase_api_request(
                client,
                operation_id="post_api_dashboard",
                body={"name": 123},
            )
    finally:
        await client.aclose()

    assert exc.value.response_body["operation_id"] == "post_api_dashboard"
    assert "not of type" in exc.value.response_body["validation_error"]


@pytest.mark.asyncio
async def test_generic_executor_uses_sql_guard_for_native_queries() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        with pytest.raises(SafetyError):
            await metabase_api_request(
                client,
                operation_id="post_api_dataset",
                body={
                    "database": 1,
                    "type": "native",
                    "query": {"query": "select * from orders; drop table orders"},
                },
            )
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_generic_executor_accepts_hyphenated_path_params_as_underscored() -> None:
    response = await metabase_api_request(
        make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={}))),
        operation_id="delete_api_card_card_id_public_link",
        path_params={"card_id": 42},
        dry_run=True,
    )

    assert response["request"]["path"] == "/api/card/42/public_link"


@pytest.mark.asyncio
async def test_generic_executor_validates_path_parameter_schema() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        with pytest.raises(RegistryError) as exc:
            await metabase_api_request(
                client,
                operation_id="get_api_dashboard_id",
                path_params={"id": 0},
            )
    finally:
        await client.aclose()

    assert exc.value.response_body["location"] == "path"
    assert exc.value.response_body["parameter"] == "id"
    assert "0" in exc.value.response_body["validation_error"]


@pytest.mark.asyncio
async def test_discover_operations_returns_api_catalog_matches() -> None:
    result = await discover_operations(text="dashboard", method="POST", limit=10)

    assert result["operation_count"] >= 500
    assert result["returned_count"] > 0
    assert any(
        operation["operation_id"] == "post_api_dashboard" for operation in result["operations"]
    )


@pytest.mark.asyncio
async def test_update_dashboard_cards_and_snippet_dry_runs() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        layout = await update_dashboard_cards(
            client,
            dashboard_id=3,
            cards=[{"id": 10, "row": 0, "col": 0, "size_x": 6, "size_y": 4}],
            dry_run=True,
        )
        added = await add_dashboard_card(
            client,
            dashboard_id=3,
            card_id=9,
            row=0,
            col=6,
            size_x=6,
            size_y=4,
            dry_run=True,
        )
        snippet = await create_native_query_snippet(
            client,
            name="Active customers",
            content="where active = true",
            dry_run=True,
        )
    finally:
        await client.aclose()

    assert layout["request"]["path"] == "/api/dashboard/3/cards"
    assert layout["request"]["body"]["cards"][0]["id"] == 10
    assert added["request"]["method"] == "PUT"
    assert added["request"]["body"]["cards"][0]["id"] == -1
    assert added["request"]["body"]["cards"][0]["card_id"] == 9
    assert snippet["request"]["path"] == "/api/native-query-snippet"
    assert snippet["request"]["body"]["content"] == "where active = true"


@pytest.mark.asyncio
async def test_public_link_copy_card_query_and_api_key_tools_dry_run() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        public_link = await create_dashboard_public_link(client, dashboard_id=7, dry_run=True)
        copy = await copy_dashboard(
            client,
            dashboard_id=7,
            name="Copy",
            collection_id=2,
            dry_run=True,
        )
        card_query = await run_card_query(client, card_id=9, dry_run=True)
        api_keys = await list_api_keys(client)
    finally:
        await client.aclose()

    assert public_link["request"]["path"] == "/api/dashboard/7/public_link"
    assert copy["request"]["path"] == "/api/dashboard/7/copy"
    assert copy["request"]["body"] == {"name": "Copy", "collection_id": 2}
    assert card_query["request"]["path"] == "/api/card/9/query"
    assert api_keys["data"] == {}


@pytest.mark.asyncio
async def test_snapshot_and_restore_dashboard() -> None:
    requests: list[tuple[str, str]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append((request.method, request.url.path))
        if request.method == "GET":
            return httpx.Response(200, json={"id": 4, "name": "Before"})
        return httpx.Response(200, json={"id": 4, "name": "Before"})

    client = make_client(httpx.MockTransport(handler))
    try:
        snapshot = await snapshot_entity(client, entity_type="dashboard", entity_id=4)
        restored = await restore_snapshot(
            client,
            snapshot=snapshot,
            dry_run=True,
        )
    finally:
        await client.aclose()

    assert snapshot["snapshot"] == {"id": 4, "name": "Before"}
    assert restored["request"]["method"] == "PUT"
    assert restored["request"]["path"] == "/api/dashboard/4"
    assert requests == [("GET", "/api/dashboard/4")]


@pytest.mark.asyncio
async def test_create_or_update_helpers_update_exact_matches() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/search":
            query = request.url.params.get("q")
            if query == "Dashboard":
                return httpx.Response(200, json={"data": [{"id": 1, "name": "Dashboard"}]})
            if query == "Card":
                return httpx.Response(200, json={"data": [{"id": 2, "name": "Card"}]})
        return httpx.Response(200, json={"ok": True})

    client = make_client(httpx.MockTransport(handler))
    try:
        dashboard = await create_or_update_dashboard(
            client,
            name="Dashboard",
            description="Updated",
            dry_run=True,
        )
        card = await create_or_update_card(
            client,
            name="Card",
            dataset_query={"database": 1, "type": "query", "query": {}},
            dry_run=True,
        )
    finally:
        await client.aclose()

    assert dashboard["request"]["path"] == "/api/dashboard/1"
    assert dashboard["request"]["body"]["description"] == "Updated"
    assert card["request"]["path"] == "/api/card/2"
    assert card["request"]["body"]["name"] == "Card"


@pytest.mark.asyncio
async def test_create_or_update_snippet_updates_exact_match() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return httpx.Response(200, json=[{"id": 8, "name": "Common filter"}])
        return httpx.Response(200, json={"ok": True})

    client = make_client(httpx.MockTransport(handler))
    try:
        response = await create_or_update_native_query_snippet(
            client,
            name="Common filter",
            content="where active",
            dry_run=True,
        )
    finally:
        await client.aclose()

    assert response["request"]["path"] == "/api/native-query-snippet/8"
    assert response["request"]["body"]["content"] == "where active"


@pytest.mark.asyncio
async def test_settings_database_and_pulse_helpers() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        setting = await get_setting(client, key="site-name")
        update = await update_setting(client, key="site-name", value="Metabase", dry_run=True)
        sync = await sync_database_schema(client, database_id=3, dry_run=True)
        rescan = await rescan_database_values(client, database_id=3, dry_run=True)
        pulse = await create_pulse(
            client,
            name="Daily metrics",
            cards=[],
            channels=[],
            dry_run=True,
        )
    finally:
        await client.aclose()

    assert setting["data"] == {}
    assert update["request"]["path"] == "/api/setting/site-name"
    assert sync["request"]["path"] == "/api/database/3/sync_schema"
    assert rescan["request"]["path"] == "/api/database/3/rescan_values"
    assert pulse["request"]["path"] == "/api/pulse"


@pytest.mark.asyncio
async def test_bookmark_revision_timeline_segment_document_and_cache_helpers() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        bookmarks = await list_bookmarks(client)
        bookmark = await create_bookmark(client, model="dashboard", entity_id=7, dry_run=True)
        revisions = await list_revisions(client, entity="dashboard", entity_id=7)
        revert = await revert_revision(
            client,
            entity="dashboard",
            entity_id=7,
            revision_id=2,
            dry_run=True,
        )
        timeline = await create_timeline(client, name="Launches", collection_id=3, dry_run=True)
        event = await create_timeline_event(
            client,
            timeline_id=4,
            name="Launch",
            timestamp="2026-05-23T00:00:00Z",
            dry_run=True,
        )
        segment = await create_segment(client, body={"name": "Active"}, dry_run=True)
        document = await create_document(client, body={"name": "Plan"}, dry_run=True)
        copy = await copy_document(client, document_id=5, name="Plan copy", dry_run=True)
        cache = await get_cache_config(client)
        invalidate = await invalidate_cache(client, body={"database_id": 1}, dry_run=True)
    finally:
        await client.aclose()

    assert bookmarks["data"] == {}
    assert bookmark["request"]["path"] == "/api/bookmark/dashboard/7"
    assert revisions["data"] == {}
    assert revert["request"]["path"] == "/api/revision/revert"
    assert revert["request"]["body"]["revision_id"] == 2
    assert timeline["request"]["path"] == "/api/timeline"
    assert event["request"]["path"] == "/api/timeline-event"
    assert segment["request"]["path"] == "/api/segment"
    assert document["request"]["path"] == "/api/document"
    assert copy["request"]["path"] == "/api/document/5/copy"
    assert cache["data"] == {}
    assert invalidate["request"]["path"] == "/api/cache/invalidate"


@pytest.mark.asyncio
async def test_remaining_curated_helpers_build_expected_requests() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        read_results = [
            await collection_tree(client),
            await list_databases(client),
            await get_card(client, card_id=1),
            await get_dashboard(client, dashboard_id=2),
            await get_dashboard_items(client, dashboard_id=2),
            await list_native_query_snippets(client),
            await get_native_query_snippet(client, snippet_id=3),
            await get_permissions_graph(client),
            await list_permission_groups(client),
            await get_permission_group(client, group_id=4),
            await list_users(client),
            await get_user(client, user_id=5),
            await list_pulses(client),
            await get_pulse(client, pulse_id=6),
            await get_card_series(client, card_id=7),
            await list_timelines(client),
            await get_timeline(client, timeline_id=8),
            await list_segments(client),
            await get_segment(client, segment_id=9),
            await list_documents(client),
            await get_document(client, document_id=10),
        ]
        dry_runs = [
            await update_collection(client, collection_id=1, updates={"name": "A"}, dry_run=True),
            await archive_collection(client, collection_id=1, dry_run=True),
            await update_card(client, card_id=2, updates={"name": "B"}, dry_run=True),
            await archive_card(client, card_id=2, dry_run=True),
            await delete_card(client, card_id=2, dry_run=True),
            await update_dashboard_parameters(client, dashboard_id=3, parameters=[], dry_run=True),
            await archive_dashboard(client, dashboard_id=3, dry_run=True),
            await delete_dashboard(client, dashboard_id=3, dry_run=True),
            await remove_dashboard_card(client, dashboard_id=3, dashcard_id=4, dry_run=True),
            await update_native_query_snippet(
                client,
                snippet_id=4,
                updates={"name": "Snippet"},
                dry_run=True,
            ),
            await update_permissions_graph(client, graph={"groups": {}}, dry_run=True),
            await create_user(
                client,
                email="a@example.com",
                first_name="A",
                last_name="B",
                dry_run=True,
            ),
            await update_user(client, user_id=5, updates={"first_name": "C"}, dry_run=True),
            await create_api_key(client, name="key", group_id=2, dry_run=True),
            await update_api_key(client, api_key_id=6, updates={"name": "key2"}, dry_run=True),
            await delete_api_key(client, api_key_id=6, dry_run=True),
            await create_card_public_link(client, card_id=7, dry_run=True),
            await delete_card_public_link(client, card_id=7, dry_run=True),
            await delete_dashboard_public_link(client, dashboard_id=8, dry_run=True),
            await copy_card(client, card_id=9, name="Copy", dry_run=True),
            await update_pulse(client, pulse_id=10, updates={"name": "Pulse"}, dry_run=True),
            await delete_pulse_subscription(client, pulse_id=10, dry_run=True),
            await delete_bookmark(client, model="card", entity_id=11, dry_run=True),
            await update_bookmark_ordering(client, ordering=[], dry_run=True),
            await update_timeline(client, timeline_id=12, updates={"name": "T"}, dry_run=True),
            await delete_timeline(client, timeline_id=12, dry_run=True),
            await update_timeline_event(client, event_id=13, updates={"name": "E"}, dry_run=True),
            await delete_timeline_event(client, event_id=13, dry_run=True),
            await update_segment(client, segment_id=14, updates={"name": "S"}, dry_run=True),
            await delete_segment(client, segment_id=14, dry_run=True),
            await update_document(client, document_id=15, updates={"name": "D"}, dry_run=True),
            await delete_document(client, document_id=15, dry_run=True),
            await update_cache_config(client, config={"enabled": True}, dry_run=True),
            await clear_cache(client, dry_run=True),
        ]
    finally:
        await client.aclose()

    assert all(result["data"] == {} for result in read_results)
    assert {item["request"]["path"] for item in dry_runs} >= {
        "/api/collection/1",
        "/api/card/2",
        "/api/dashboard/3",
        "/api/dashboard/3/cards/4",
        "/api/native-query-snippet/4",
        "/api/permissions/graph",
        "/api/user",
        "/api/user/5",
        "/api/api-key",
        "/api/api-key/6",
        "/api/card/7/public_link",
        "/api/dashboard/8/public_link",
        "/api/card/9/copy",
        "/api/pulse/10",
        "/api/pulse/10/subscription",
        "/api/bookmark/card/11",
        "/api/bookmark/ordering",
        "/api/timeline/12",
        "/api/timeline-event/13",
        "/api/segment/14",
        "/api/document/15",
        "/api/cache",
    }
