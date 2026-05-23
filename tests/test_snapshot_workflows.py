import httpx
import pytest
from pydantic import SecretStr

from mcp_for_metabase.application.snapshot_workflows import restore_snapshot, snapshot_entity
from mcp_for_metabase.client import MetabaseClient
from mcp_for_metabase.config import Settings, WriteMode
from mcp_for_metabase.errors import RegistryError


def make_client(handler: httpx.MockTransport) -> MetabaseClient:
    return MetabaseClient(
        Settings(
            METABASE_URL="http://metabase.test",
            METABASE_API_KEY=SecretStr("mb_key"),
            METABASE_MCP_WRITE_MODE=WriteMode.READ_ONLY,
        ),
        transport=handler,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("entity_type", "entity_id", "expected_path"),
    [
        ("dashboard", 1, "/api/dashboard/1"),
        ("card", 2, "/api/card/2"),
        ("collection", 3, "/api/collection/3"),
        ("permissions_graph", None, "/api/permissions/graph"),
    ],
)
async def test_snapshot_entity_supported_types(
    entity_type: str,
    entity_id: int | None,
    expected_path: str,
) -> None:
    seen_path = ""

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_path
        seen_path = request.url.path
        return httpx.Response(
            200,
            json={"id": entity_id, "name": entity_type},
            headers={"X-Request-ID": "request-1"},
        )

    client = make_client(httpx.MockTransport(handler))
    try:
        snapshot = await snapshot_entity(client, entity_type=entity_type, entity_id=entity_id)
    finally:
        await client.aclose()

    assert seen_path == expected_path
    assert snapshot["entity_type"] == entity_type
    assert snapshot["entity_id"] == entity_id
    assert snapshot["snapshot"]["name"] == entity_type


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("snapshot", "expected_path"),
    [
        (
            {"entity_type": "dashboard", "entity_id": 1, "snapshot": {"name": "Dashboard"}},
            "/api/dashboard/1",
        ),
        ({"entity_type": "card", "entity_id": 2, "snapshot": {"name": "Card"}}, "/api/card/2"),
        (
            {"entity_type": "collection", "entity_id": 3, "snapshot": {"name": "Collection"}},
            "/api/collection/3",
        ),
        (
            {"entity_type": "permissions_graph", "snapshot": {"groups": {}}},
            "/api/permissions/graph",
        ),
    ],
)
async def test_restore_snapshot_supported_types(
    snapshot: dict[str, object],
    expected_path: str,
) -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        response = await restore_snapshot(client, snapshot=snapshot, dry_run=True)
    finally:
        await client.aclose()

    assert response["request"]["path"] == expected_path


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "entity_type",
    ["dashboard", "card", "collection"],
)
async def test_snapshot_entity_requires_id(entity_type: str) -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        with pytest.raises(RegistryError):
            await snapshot_entity(client, entity_type=entity_type)
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_restore_snapshot_rejects_invalid_payloads() -> None:
    client = make_client(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    try:
        with pytest.raises(RegistryError):
            await restore_snapshot(client, snapshot={"entity_type": "dashboard"})
        with pytest.raises(RegistryError):
            await restore_snapshot(
                client,
                snapshot={"entity_type": "dashboard", "snapshot": {}},
            )
        with pytest.raises(RegistryError):
            await restore_snapshot(
                client,
                snapshot={"entity_type": "unknown", "snapshot": {}},
            )
    finally:
        await client.aclose()
