# SPDX-License-Identifier: GPL-3.0-or-later
from mcp.server.fastmcp import FastMCP

from mcp_for_metabase.config import Settings
from mcp_for_metabase.mcp_app.factory import create_mcp as _create_mcp


def create_mcp(settings: Settings | None = None) -> FastMCP:
    return _create_mcp(settings)
