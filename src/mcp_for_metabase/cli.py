# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Annotated

import typer

from mcp_for_metabase.config import Settings, Transport
from mcp_for_metabase.server import create_mcp

app = typer.Typer(help="Metabase MCP server")


@app.callback()
def main() -> None:
    """Metabase MCP command line interface."""


@app.command()
def serve(
    transport: Annotated[
        Transport | None,
        typer.Option("--transport", help="MCP transport: stdio or http"),
    ] = None,
    host: Annotated[str | None, typer.Option("--host", help="HTTP bind host")] = None,
    port: Annotated[int | None, typer.Option("--port", help="HTTP bind port")] = None,
) -> None:
    settings = Settings()
    selected_transport = transport or settings.metabase_mcp_transport
    if host is not None:
        settings.metabase_mcp_http_host = host
    if port is not None:
        settings.metabase_mcp_http_port = port

    mcp = create_mcp(settings)
    if selected_transport == Transport.HTTP:
        mcp.run(transport="streamable-http")
        return
    mcp.run(transport="stdio")
