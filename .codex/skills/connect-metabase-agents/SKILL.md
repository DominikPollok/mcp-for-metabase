# Connect Metabase Agents Skill

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

Use this skill when configuring an agent or MCP client to connect to `mcp-for-metabase`.

## Connection Modes

- Prefer stdio when the client launches the server locally:
  `mcp-for-metabase serve --transport stdio`
- Prefer Streamable HTTP when the server runs in Docker:
  `mcp-for-metabase serve --transport http --host 0.0.0.0 --port 8000`
- Docker HTTP endpoint: `http://localhost:8000/mcp`

## Required Environment

Set:

- `METABASE_URL`
- `METABASE_API_KEY`
- `METABASE_MCP_WRITE_MODE=read-only`

Use `safe-writes` only after a successful read-only connection test. Use `all-writes` only for explicit admin/destructive tasks.

## Agent Startup

1. Run MCP-native discovery: `tools/list`, `resources/list`, `resourceTemplates/list`, `prompts/list`.
2. Read `metabase://agent/connection-guide`.
3. Call `metabase_connection_test`.
4. Call `metabase_discover_operations` to find API operations.
5. Call `metabase_get_operation` before using `metabase_api_request`.
6. Use `dry_run=true` before writes.

## Client Config Example

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
