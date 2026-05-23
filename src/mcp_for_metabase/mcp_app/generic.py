# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_for_metabase import tools
from mcp_for_metabase.mcp_app.context import McpAppContext


def register_generic_tools(mcp: FastMCP, context: McpAppContext) -> None:
    with_client = context.with_client

    @mcp.tool()
    async def metabase_discover_operations(
        text: str | None = None,
        method: str | None = None,
        safety_tier: str | None = None,
        tag: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        """Discover generated Metabase API operations for generic API calls."""
        return await tools.discover_operations(
            text=text,
            method=method,
            safety_tier=safety_tier,
            tag=tag,
            limit=limit,
        )

    @mcp.tool()
    async def metabase_get_operation(operation_id: str) -> dict[str, Any]:
        """Return method, path, parameters, safety tier, and docs metadata for one operation."""
        return await tools.get_operation(operation_id=operation_id)

    @mcp.tool()
    async def metabase_api_request(
        operation_id: str,
        path_params: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        body: Any | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Execute any generated Metabase API operation through the central safety policy."""
        return await with_client(
            lambda client: tools.metabase_api_request(
                client,
                operation_id=operation_id,
                path_params=path_params,
                query=query,
                body=body,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )
