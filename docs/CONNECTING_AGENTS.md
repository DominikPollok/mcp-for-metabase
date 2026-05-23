# Connecting Agents

Use this guide when connecting Claude Desktop, Codex, Cursor, custom MCP clients, or other agents to the Metabase MCP server.

## Choose A Transport

Use stdio when the MCP client launches the server process directly.

```bash
mcp-for-metabase serve --transport stdio
```

Use Streamable HTTP when the server runs in Docker or on another host.

```bash
mcp-for-metabase serve --transport http --host 0.0.0.0 --port 8000
```

HTTP endpoint:

```text
http://localhost:8000/mcp
```

## Required Environment

```bash
METABASE_URL=https://metabase.example.com
METABASE_API_KEY=mb_your_key
METABASE_MCP_WRITE_MODE=read-only
```

Use `read-only` for first connection tests. Move to `safe-writes` only when the agent should create or update content. Use `all-writes` only for admin/destructive workflows.

## Example stdio Config

```json
{
  "mcpServers": {
    "metabase": {
      "command": "mcp-for-metabase",
      "args": ["serve", "--transport", "stdio"],
      "env": {
        "METABASE_URL": "https://metabase.example.com",
        "METABASE_API_KEY": "mb_your_key",
        "METABASE_MCP_WRITE_MODE": "read-only"
      }
    }
  }
}
```

## Installing via PyPI

Install once with pipx (recommended) or pip:

```bash
pipx install mcp-for-metabase
```

```bash
pip install mcp-for-metabase
```

Run the server:

```bash
mcp-for-metabase serve --transport stdio
```

Or run with inline environment variables:

```bash
METABASE_URL=https://metabase.example.com \
METABASE_API_KEY=mb_your_key \
METABASE_MCP_WRITE_MODE=read-only \
mcp-for-metabase serve --transport stdio
```

## Example Docker HTTP Config

Start the server:

```bash
docker compose up --build mcp
```

Configure the client to connect to:

```text
http://localhost:8000/mcp
```

## Agent Startup Checklist

1. Run native MCP discovery: `tools/list`, `resources/list`, `resourceTemplates/list`, `prompts/list`.
2. Read `metabase://agent/connection-guide`.
3. Call `metabase_connection_test`.
4. Read `metabase://api/coverage` or call `metabase_discover_operations`.
5. Use curated dashboard tools for common workflows.
6. Use `metabase_get_operation` and `metabase_api_request` for API operations without a curated tool.
7. Use `dry_run=true` before any write on shared or production Metabase instances.

## Recommended Agent Prompt

```text
You are connected to Metabase through the metabase MCP server.
Start with MCP-native discovery, then call metabase_connection_test.
Prefer high-level dashboard tools for dashboard work.
For uncovered API areas, use metabase_discover_operations, metabase_get_operation, and metabase_api_request.
Use dry_run=true before writes.
Never request all-writes mode unless the user explicitly asks for admin or destructive operations.
Keep dashboard cards in the same collection as their dashboard unless the user asks for a different permission model.
```
