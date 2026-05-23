# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_for_metabase import tools
from mcp_for_metabase.mcp_app.context import McpAppContext
from mcp_for_metabase.registry import ApiRegistry


def register_resources(mcp: FastMCP, context: McpAppContext) -> None:
    with_client = context.with_client
    snapshot_store = context.snapshot_store

    @mcp.resource("metabase://instance/info")
    async def instance_info() -> dict[str, Any]:
        return await with_client(lambda client: tools.connection_test(client))

    @mcp.resource("metabase://api/coverage")
    async def api_coverage() -> dict[str, Any]:
        """Return the complete generated Metabase API operation catalog."""
        registry = ApiRegistry.load_default()
        return {
            "operation_count": len(registry.operations),
            "operations": [
                tools.operation_to_dict(operation) for operation in registry.operations.values()
            ],
        }

    @mcp.resource("metabase://api/operations")
    async def api_operations() -> dict[str, Any]:
        """Return MCP-native discovery metadata for generic Metabase API calls."""
        return await tools.discover_operations(limit=600)

    @mcp.resource("metabase://snapshots")
    async def saved_snapshots() -> dict[str, Any]:
        """Return locally persisted rollback snapshots."""
        snapshots = snapshot_store().list(limit=100)
        return {"snapshot_count": len(snapshots), "snapshots": snapshots}

    @mcp.resource("metabase://agent/connection-guide")
    async def agent_connection_guide() -> dict[str, Any]:
        """Return connection guidance for MCP clients and coding agents."""
        return {
            "server_name": "mcp-for-metabase",
            "transports": ["stdio", "streamable-http"],
            "stdio_command": "mcp-for-metabase serve --transport stdio",
            "http_command": "mcp-for-metabase serve --transport http --host 0.0.0.0 --port 8000",
            "required_env": ["METABASE_URL"],
            "auth_env": ["METABASE_API_KEY", "METABASE_USERNAME", "METABASE_PASSWORD"],
            "write_modes": ["read-only", "safe-writes", "all-writes"],
            "discovery": {
                "native": ["tools/list", "resources/list", "prompts/list"],
                "resources": ["metabase://api/coverage", "metabase://api/operations"],
                "tools": ["metabase_discover_operations", "metabase_get_operation"],
            },
        }

    @mcp.resource("metabase://collections/tree")
    async def collections_tree() -> dict[str, Any]:
        return await with_client(lambda client: tools.collection_tree(client))

    @mcp.resource("metabase://dashboard/{dashboard_id}")
    async def dashboard(dashboard_id: int) -> dict[str, Any]:
        return await with_client(
            lambda client: tools.get_dashboard(client, dashboard_id=dashboard_id)
        )

    @mcp.resource("metabase://card/{card_id}")
    async def card(card_id: int) -> dict[str, Any]:
        return await with_client(lambda client: tools.get_card(client, card_id=card_id))

    @mcp.resource("metabase://database/{database_id}/metadata")
    async def database_metadata(database_id: int) -> dict[str, Any]:
        return await with_client(
            lambda client: tools.get_database_metadata(client, database_id=database_id),
        )
