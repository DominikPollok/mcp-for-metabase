import pytest
from typer.testing import CliRunner

from mcp_for_metabase.cli import app
from mcp_for_metabase.config import Settings
from mcp_for_metabase.healthcheck import main as healthcheck_main
from mcp_for_metabase.server import create_mcp


def test_create_mcp_registers_without_error() -> None:
    mcp = create_mcp(Settings(METABASE_URL="http://metabase.test"))

    assert mcp.name == "Metabase MCP"


@pytest.mark.asyncio
async def test_mcp_native_discovery_lists_tools_resources_and_prompts() -> None:
    mcp = create_mcp(Settings(METABASE_URL="http://metabase.test"))

    tools = await mcp.list_tools()
    resources = await mcp.list_resources()
    prompts = await mcp.list_prompts()
    resource_templates = await mcp.list_resource_templates()

    assert {tool.name for tool in tools} >= {
        "metabase_api_request",
        "metabase_update_dashboard_cards",
        "metabase_create_native_query_snippet",
        "metabase_update_permissions_graph",
        "metabase_list_api_keys",
        "metabase_create_dashboard_public_link",
        "metabase_copy_dashboard",
        "metabase_remove_dashboard_card",
        "metabase_run_card_query",
        "metabase_snapshot_entity",
        "metabase_list_saved_snapshots",
        "metabase_restore_snapshot",
        "metabase_restore_saved_snapshot",
        "metabase_create_or_update_dashboard",
        "metabase_create_or_update_card",
        "metabase_get_settings",
        "metabase_sync_database_schema",
        "metabase_create_pulse",
        "metabase_list_bookmarks",
        "metabase_revert_revision",
        "metabase_create_timeline",
        "metabase_create_segment",
        "metabase_create_document",
        "metabase_invalidate_cache",
        "metabase_discover_operations",
        "metabase_get_operation",
    }
    assert {str(resource.uri) for resource in resources} >= {
        "metabase://api/coverage",
        "metabase://api/operations",
        "metabase://snapshots",
        "metabase://agent/connection-guide",
    }
    assert {prompt.name for prompt in prompts} >= {"build_dashboard", "audit_dashboard"}
    assert {str(template.uriTemplate) for template in resource_templates} >= {
        "metabase://dashboard/{dashboard_id}",
        "metabase://card/{card_id}",
        "metabase://database/{database_id}/metadata",
    }


@pytest.mark.asyncio
async def test_mcp_prompts_render_dashboard_workflows() -> None:
    mcp = create_mcp(Settings(METABASE_URL="http://metabase.test"))

    prompts = [
        await mcp.get_prompt(
            "build_dashboard",
            {"topic": "sales", "database_id": 1, "collection_name": "Ops"},
        ),
        await mcp.get_prompt("audit_dashboard", {"dashboard_id": 2}),
        await mcp.get_prompt("improve_dashboard", {"dashboard_id": 2, "goal": "speed"}),
        await mcp.get_prompt("create_semantic_model", {"database_id": 1, "table_id": 3}),
        await mcp.get_prompt(
            "migrate_content",
            {"source_collection_id": 4, "target_collection_id": 5},
        ),
    ]

    rendered = "\n".join(prompt.messages[0].content.text for prompt in prompts)
    assert "Build a Metabase dashboard" in rendered
    assert "Audit Metabase dashboard 2" in rendered
    assert "Improve Metabase dashboard 2" in rendered
    assert "semantic model" in rendered
    assert "Migrate reusable Metabase content" in rendered


@pytest.mark.asyncio
async def test_mcp_static_resources_are_readable(tmp_path) -> None:  # type: ignore[no-untyped-def]
    mcp = create_mcp(
        Settings(
            METABASE_URL="http://metabase.test",
            METABASE_MCP_SNAPSHOT_DIR=tmp_path,
        ),
    )

    connection_guide = await mcp.read_resource("metabase://agent/connection-guide")
    api_operations = await mcp.read_resource("metabase://api/operations")
    snapshots = await mcp.read_resource("metabase://snapshots")

    assert "mcp-for-metabase" in connection_guide[0].content
    assert '"operation_count": 600' in api_operations[0].content
    assert '"snapshot_count": 0' in snapshots[0].content


def test_healthcheck_loads_settings() -> None:
    healthcheck_main()


def test_cli_serve_uses_http_transport(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    calls: dict[str, object] = {}

    class FakeMcp:
        def run(self, *, transport: str) -> None:
            calls["transport"] = transport

    def fake_create_mcp(settings: Settings) -> FakeMcp:
        calls["host"] = settings.metabase_mcp_http_host
        calls["port"] = settings.metabase_mcp_http_port
        return FakeMcp()

    monkeypatch.setattr("mcp_for_metabase.cli.create_mcp", fake_create_mcp)
    result = CliRunner().invoke(
        app,
        ["serve", "--transport", "http", "--host", "0.0.0.0", "--port", "9000"],
    )

    assert result.exit_code == 0
    assert calls == {"host": "0.0.0.0", "port": 9000, "transport": "streamable-http"}
