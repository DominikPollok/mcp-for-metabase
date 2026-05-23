import pytest

from mcp_for_metabase.config import Settings
from mcp_for_metabase.server import create_mcp


async def call_tool(name: str, arguments: dict[str, object]) -> dict[str, object]:
    mcp = create_mcp(Settings(METABASE_URL="http://metabase.test"))
    _content, structured = await mcp.call_tool(name, arguments)
    assert isinstance(structured, dict)
    return structured


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "arguments", "expected_path"),
    [
        ("metabase_create_collection", {"name": "Collection", "dry_run": True}, "/api/collection"),
        (
            "metabase_update_collection",
            {"collection_id": 1, "updates": {"name": "Updated"}, "dry_run": True},
            "/api/collection/1",
        ),
        ("metabase_archive_collection", {"collection_id": 1, "dry_run": True}, "/api/collection/1"),
        (
            "metabase_create_card",
            {"name": "Card", "dataset_query": {"database": 1}, "dry_run": True},
            "/api/card",
        ),
        (
            "metabase_update_card",
            {"card_id": 2, "updates": {"name": "Updated"}, "dry_run": True},
            "/api/card/2",
        ),
        ("metabase_archive_card", {"card_id": 2, "dry_run": True}, "/api/card/2"),
        ("metabase_delete_card", {"card_id": 2, "dry_run": True}, "/api/card/2"),
        ("metabase_create_dashboard", {"name": "Dashboard", "dry_run": True}, "/api/dashboard"),
        (
            "metabase_update_dashboard",
            {"dashboard_id": 3, "updates": {"name": "Updated"}, "dry_run": True},
            "/api/dashboard/3",
        ),
        (
            "metabase_update_dashboard_parameters",
            {"dashboard_id": 3, "parameters": [], "dry_run": True},
            "/api/dashboard/3",
        ),
        ("metabase_archive_dashboard", {"dashboard_id": 3, "dry_run": True}, "/api/dashboard/3"),
        ("metabase_delete_dashboard", {"dashboard_id": 3, "dry_run": True}, "/api/dashboard/3"),
        (
            "metabase_add_dashboard_card",
            {
                "dashboard_id": 3,
                "card_id": 2,
                "row": 0,
                "col": 0,
                "size_x": 6,
                "size_y": 4,
                "dry_run": True,
            },
            "/api/dashboard/3/cards",
        ),
        (
            "metabase_update_dashboard_cards",
            {"dashboard_id": 3, "cards": [{"id": 4, "row": 0, "col": 0}], "dry_run": True},
            "/api/dashboard/3/cards",
        ),
        (
            "metabase_remove_dashboard_card",
            {"dashboard_id": 3, "dashcard_id": 4, "dry_run": True},
            "/api/dashboard/3/cards/4",
        ),
        (
            "metabase_create_native_query_snippet",
            {"name": "Snippet", "content": "where true", "dry_run": True},
            "/api/native-query-snippet",
        ),
        (
            "metabase_update_native_query_snippet",
            {"snippet_id": 5, "updates": {"name": "Snippet"}, "dry_run": True},
            "/api/native-query-snippet/5",
        ),
        (
            "metabase_create_user",
            {"email": "a@example.com", "first_name": "A", "last_name": "B", "dry_run": True},
            "/api/user",
        ),
        (
            "metabase_update_user",
            {"user_id": 6, "updates": {"first_name": "C"}, "dry_run": True},
            "/api/user/6",
        ),
        (
            "metabase_create_api_key",
            {"name": "Key", "group_id": 2, "dry_run": True},
            "/api/api-key",
        ),
        (
            "metabase_update_api_key",
            {"api_key_id": 7, "updates": {"name": "K"}, "dry_run": True},
            "/api/api-key/7",
        ),
        ("metabase_delete_api_key", {"api_key_id": 7, "dry_run": True}, "/api/api-key/7"),
        (
            "metabase_create_card_public_link",
            {"card_id": 8, "dry_run": True},
            "/api/card/8/public_link",
        ),
        (
            "metabase_delete_card_public_link",
            {"card_id": 8, "dry_run": True},
            "/api/card/8/public_link",
        ),
        (
            "metabase_create_dashboard_public_link",
            {"dashboard_id": 9, "dry_run": True},
            "/api/dashboard/9/public_link",
        ),
        (
            "metabase_delete_dashboard_public_link",
            {"dashboard_id": 9, "dry_run": True},
            "/api/dashboard/9/public_link",
        ),
        (
            "metabase_copy_dashboard",
            {"dashboard_id": 9, "name": "Copy", "dry_run": True},
            "/api/dashboard/9/copy",
        ),
        ("metabase_copy_card", {"card_id": 8, "name": "Copy", "dry_run": True}, "/api/card/8/copy"),
        ("metabase_run_card_query", {"card_id": 8, "dry_run": True}, "/api/card/8/query"),
        (
            "metabase_export_card_query",
            {"card_id": 8, "export_format": "csv", "dry_run": True},
            "/api/card/8/query/csv",
        ),
        (
            "metabase_create_pulse",
            {"name": "Pulse", "cards": [], "channels": [], "dry_run": True},
            "/api/pulse",
        ),
        (
            "metabase_update_pulse",
            {"pulse_id": 10, "updates": {"name": "P"}, "dry_run": True},
            "/api/pulse/10",
        ),
        (
            "metabase_delete_pulse_subscription",
            {"pulse_id": 10, "dry_run": True},
            "/api/pulse/10/subscription",
        ),
        (
            "metabase_create_bookmark",
            {"model": "card", "entity_id": 8, "dry_run": True},
            "/api/bookmark/card/8",
        ),
        (
            "metabase_delete_bookmark",
            {"model": "card", "entity_id": 8, "dry_run": True},
            "/api/bookmark/card/8",
        ),
        (
            "metabase_update_bookmark_ordering",
            {"ordering": [], "dry_run": True},
            "/api/bookmark/ordering",
        ),
        (
            "metabase_revert_revision",
            {"entity": "card", "entity_id": 8, "revision_id": 1, "dry_run": True},
            "/api/revision/revert",
        ),
        ("metabase_create_timeline", {"name": "Timeline", "dry_run": True}, "/api/timeline"),
        (
            "metabase_update_timeline",
            {"timeline_id": 11, "updates": {"name": "T"}, "dry_run": True},
            "/api/timeline/11",
        ),
        ("metabase_delete_timeline", {"timeline_id": 11, "dry_run": True}, "/api/timeline/11"),
        (
            "metabase_create_timeline_event",
            {"timeline_id": 11, "name": "E", "timestamp": "2026-05-23T00:00:00Z", "dry_run": True},
            "/api/timeline-event",
        ),
        (
            "metabase_update_timeline_event",
            {"event_id": 12, "updates": {"name": "E"}, "dry_run": True},
            "/api/timeline-event/12",
        ),
        (
            "metabase_delete_timeline_event",
            {"event_id": 12, "dry_run": True},
            "/api/timeline-event/12",
        ),
        ("metabase_create_segment", {"body": {"name": "Segment"}, "dry_run": True}, "/api/segment"),
        (
            "metabase_update_segment",
            {"segment_id": 13, "updates": {"name": "S"}, "dry_run": True},
            "/api/segment/13",
        ),
        ("metabase_delete_segment", {"segment_id": 13, "dry_run": True}, "/api/segment/13"),
        ("metabase_create_document", {"body": {"name": "Doc"}, "dry_run": True}, "/api/document"),
        (
            "metabase_update_document",
            {"document_id": 14, "updates": {"name": "D"}, "dry_run": True},
            "/api/document/14",
        ),
        ("metabase_delete_document", {"document_id": 14, "dry_run": True}, "/api/document/14"),
        (
            "metabase_copy_document",
            {"document_id": 14, "name": "Copy", "dry_run": True},
            "/api/document/14/copy",
        ),
        (
            "metabase_update_cache_config",
            {"config": {"enabled": True}, "dry_run": True},
            "/api/cache",
        ),
        ("metabase_invalidate_cache", {"body": {}, "dry_run": True}, "/api/cache/invalidate"),
        ("metabase_clear_cache", {"dry_run": True}, "/api/cache"),
    ],
)
async def test_server_write_tools_support_dry_run(
    tool_name: str,
    arguments: dict[str, object],
    expected_path: str,
) -> None:
    response = await call_tool(tool_name, arguments)

    assert response["dry_run"] is True
    assert response["request"]["path"] == expected_path


@pytest.mark.asyncio
async def test_server_generic_api_request_dry_run() -> None:
    response = await call_tool(
        "metabase_api_request",
        {
            "operation_id": "post_api_dashboard",
            "body": {"name": "Dashboard"},
            "dry_run": True,
        },
    )

    assert response["request"]["operation_id"] == "post_api_dashboard"


@pytest.mark.asyncio
async def test_server_saved_snapshot_resource_uses_snapshot_dir(tmp_path) -> None:  # type: ignore[no-untyped-def]
    mcp = create_mcp(
        Settings(
            METABASE_URL="http://metabase.test",
            METABASE_MCP_SNAPSHOT_DIR=tmp_path,
        ),
    )
    _content, structured = await mcp.call_tool("metabase_list_saved_snapshots", {"limit": 10})

    assert structured == {"snapshot_count": 0, "snapshots": []}
