from pathlib import Path

import httpx
import pytest
from pydantic import SecretStr

from mcp_for_metabase.client import MetabaseClient
from mcp_for_metabase.config import Settings, SqlGuardMode, WriteMode
from mcp_for_metabase.errors import MetabaseError, SafetyError


def settings(
    write_mode: WriteMode = WriteMode.READ_ONLY,
    audit_log: Path | None = None,
    sql_guard_mode: SqlGuardMode = SqlGuardMode.STRICT,
) -> Settings:
    return Settings(
        METABASE_URL="http://metabase.test",
        METABASE_API_KEY=SecretStr("mb_key"),
        METABASE_MCP_WRITE_MODE=write_mode,
        METABASE_MCP_AUDIT_LOG=audit_log,
        METABASE_MCP_SQL_GUARD_MODE=sql_guard_mode,
    )


@pytest.mark.asyncio
async def test_client_sends_api_key_and_parses_json() -> None:
    seen_headers: dict[str, str] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen_headers.update(request.headers)
        return httpx.Response(200, json={"version": "test"})

    client = MetabaseClient(settings(), transport=httpx.MockTransport(handler))
    try:
        response = await client.request("GET", "/api/session/properties")
    finally:
        await client.aclose()

    assert response["data"] == {"version": "test"}
    assert seen_headers["x-api-key"] == "mb_key"


@pytest.mark.asyncio
async def test_client_dry_run_does_not_send_request() -> None:
    sent = False

    async def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal sent
        sent = True
        return httpx.Response(200, json={})

    client = MetabaseClient(settings(), transport=httpx.MockTransport(handler))
    try:
        response = await client.request("POST", "/api/dashboard", dry_run=True, body={"name": "A"})
    finally:
        await client.aclose()

    assert sent is False
    assert response["dry_run"] is True
    assert response["request"]["body"] == {"name": "A"}


@pytest.mark.asyncio
async def test_client_blocks_write_in_read_only() -> None:
    client = MetabaseClient(
        settings(), transport=httpx.MockTransport(lambda _request: httpx.Response(200))
    )
    try:
        with pytest.raises(SafetyError):
            await client.request("POST", "/api/dashboard", body={"name": "A"})
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_client_audits_mutations(tmp_path: Path) -> None:
    audit_path = tmp_path / "audit.log"

    async def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"id": 1})

    client = MetabaseClient(
        settings(WriteMode.SAFE_WRITES, audit_path),
        transport=httpx.MockTransport(handler),
    )
    try:
        await client.request("POST", "/api/dashboard", body={"name": "A"})
    finally:
        await client.aclose()

    assert "post" not in audit_path.read_text(encoding="utf-8")
    assert '"method": "POST"' in audit_path.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_client_uses_session_auth_when_api_key_missing() -> None:
    seen_session_header: str | None = None

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_session_header
        if request.url.path == "/api/session":
            return httpx.Response(200, json={"id": "session-1"})
        seen_session_header = request.headers.get("x-metabase-session")
        return httpx.Response(200, json={"ok": True})

    client = MetabaseClient(
        Settings(
            METABASE_URL="http://metabase.test",
            METABASE_USERNAME="user@example.com",
            METABASE_PASSWORD=SecretStr("password"),
        ),
        transport=httpx.MockTransport(handler),
    )
    try:
        await client.request("GET", "/api/session/properties")
    finally:
        await client.aclose()

    assert seen_session_header == "session-1"


@pytest.mark.asyncio
async def test_client_raises_structured_error() -> None:
    async def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"message": "Forbidden"})

    client = MetabaseClient(settings(), transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(MetabaseError) as exc:
            await client.request("GET", "/api/session/properties")
    finally:
        await client.aclose()

    assert exc.value.status_code == 403
    assert exc.value.response_body == {"message": "Forbidden"}


@pytest.mark.asyncio
async def test_client_paginates_until_short_page() -> None:
    calls = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        offset = request.url.params.get("offset")
        if offset == "0":
            return httpx.Response(200, json={"data": [{"id": 1}, {"id": 2}]})
        return httpx.Response(200, json={"data": [{"id": 3}]})

    client = MetabaseClient(settings(), transport=httpx.MockTransport(handler))
    try:
        results = await client.paginate("/api/search", limit=2)
    finally:
        await client.aclose()

    assert calls == 2
    assert results == [{"id": 1}, {"id": 2}, {"id": 3}]


@pytest.mark.asyncio
async def test_client_resolves_hyphenated_path_params_from_pythonic_keys() -> None:
    seen_path = ""

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_path
        seen_path = request.url.path
        return httpx.Response(200, json={"ok": True})

    client = MetabaseClient(settings(), transport=httpx.MockTransport(handler))
    try:
        await client.request(
            "GET",
            "/api/card/{card-id}/query",
            path_params={"card_id": 42},
        )
    finally:
        await client.aclose()

    assert seen_path == "/api/card/42/query"


@pytest.mark.asyncio
async def test_client_blocks_unsafe_native_sql_before_sending_request() -> None:
    sent = False

    async def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal sent
        sent = True
        return httpx.Response(200, json={})

    client = MetabaseClient(settings(), transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(SafetyError):
            await client.request(
                "POST",
                "/api/dataset",
                operation_id="post_api_dataset",
                body={
                    "type": "native",
                    "query": {"query": "select * from orders; drop table orders"},
                },
            )
    finally:
        await client.aclose()

    assert sent is False


@pytest.mark.asyncio
async def test_client_can_disable_sql_guard_explicitly() -> None:
    seen_body = ""

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_body
        seen_body = request.read().decode()
        return httpx.Response(200, json={})

    client = MetabaseClient(
        settings(sql_guard_mode=SqlGuardMode.DISABLED),
        transport=httpx.MockTransport(handler),
    )
    try:
        await client.request(
            "POST",
            "/api/dataset",
            operation_id="post_api_dataset",
            body={"type": "native", "query": {"query": "delete from orders"}},
        )
    finally:
        await client.aclose()

    assert "delete from orders" in seen_body
