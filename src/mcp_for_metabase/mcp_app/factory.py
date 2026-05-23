# SPDX-License-Identifier: GPL-3.0-or-later
from mcp.server.fastmcp import FastMCP

from mcp_for_metabase.config import Settings
from mcp_for_metabase.mcp_app.context import McpAppContext
from mcp_for_metabase.mcp_app.curated import register_curated_tools
from mcp_for_metabase.mcp_app.generic import register_generic_tools
from mcp_for_metabase.mcp_app.prompts import register_prompts
from mcp_for_metabase.mcp_app.resources import register_resources


def create_mcp(settings: Settings | None = None) -> FastMCP:
    settings = settings or Settings()
    mcp = FastMCP(
        "Metabase MCP",
        json_response=True,
        host=settings.metabase_mcp_http_host,
        port=settings.metabase_mcp_http_port,
    )
    context = McpAppContext(settings)
    register_resources(mcp, context)
    register_prompts(mcp, context)
    register_curated_tools(mcp, context)
    register_generic_tools(mcp, context)
    return mcp
