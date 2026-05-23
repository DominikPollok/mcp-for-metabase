# Connecting Agents

Use this guide to connect Codex, Claude Code, Claude Desktop, Cursor, or a custom MCP client to `mcp-for-metabase`.

## The Short Version

1. Create a Metabase API key in **Admin settings -> Authentication -> API keys** and assign it to a least-privileged group.
2. Keep the first connection in `read-only` mode.
3. Choose one transport:
   - `stdio`: the agent launches `mcp-for-metabase` directly.
   - `http`: the MCP server runs separately, usually in Docker, and agents connect to `/mcp`.
4. Connect your client with one of the copy/paste commands below.
5. Ask the agent to call `metabase_connection_test`.

Official client references:

- Codex MCP configuration: <https://developers.openai.com/codex/mcp>
- Claude Code MCP configuration: <https://code.claude.com/docs/en/mcp>
- Metabase API keys: <https://www.metabase.com/docs/latest/people-and-groups/api-keys>

## Required Values

```bash
METABASE_URL=https://metabase.example.com
METABASE_API_KEY=mb_your_key
METABASE_MCP_WRITE_MODE=read-only
```

Use a real Metabase base URL, without a trailing `/api`. Common examples:

| Where Metabase runs | `METABASE_URL` |
| --- | --- |
| Metabase Cloud or hosted HTTPS | `https://metabase.example.com` |
| Metabase on the same host as a stdio server | `http://localhost:3000` |
| Metabase on your host, MCP server in Docker on macOS/Windows | `http://host.docker.internal:3000` |
| The bundled Docker Compose Metabase service | `http://metabase:3000` |

Keep credentials out of `METABASE_URL`. If a reverse proxy in front of Metabase requires Basic auth, set:

```bash
METABASE_BASIC_AUTH_USERNAME=proxy_user
METABASE_BASIC_AUTH_PASSWORD=proxy_password
```

For non-Basic proxy headers, set `METABASE_HTTP_HEADERS_JSON` to a JSON object such as:

```bash
METABASE_HTTP_HEADERS_JSON='{"X-Forwarded-User":"agent"}'
```

## Option A: Local stdio

Use stdio when the MCP client should start the server process itself. This is the simplest setup for one machine.

Install the command once:

```bash
pipx install mcp-for-metabase
```

If the PyPI package is not available yet, install from GitHub:

```bash
pipx install git+https://github.com/DominikPollok/mcp-for-metabase.git
```

If you are developing from a local clone instead, install it in editable mode:

```bash
git clone https://github.com/DominikPollok/mcp-for-metabase.git
cd mcp-for-metabase
python -m pip install -e ".[dev]"
```

### Codex stdio

```bash
codex mcp add metabase \
  --env METABASE_URL=https://metabase.example.com \
  --env METABASE_API_KEY=mb_your_key \
  --env METABASE_MCP_WRITE_MODE=read-only \
  -- mcp-for-metabase serve --transport stdio
codex mcp list
```

Equivalent `~/.codex/config.toml`:

```toml
[mcp_servers.metabase]
command = "mcp-for-metabase"
args = ["serve", "--transport", "stdio"]
enabled = true
startup_timeout_sec = 30

[mcp_servers.metabase.env]
METABASE_URL = "https://metabase.example.com"
METABASE_API_KEY = "mb_your_key"
METABASE_MCP_WRITE_MODE = "read-only"
METABASE_MCP_SQL_GUARD_MODE = "strict"
```

### Claude Code stdio

```bash
claude mcp add --transport stdio --scope user \
  --env METABASE_URL=https://metabase.example.com \
  --env METABASE_API_KEY=mb_your_key \
  --env METABASE_MCP_WRITE_MODE=read-only \
  metabase -- mcp-for-metabase serve --transport stdio
claude mcp list
```

In Claude Code, run `/mcp` and confirm the `metabase` server is connected.

Project-level `.mcp.json` alternative:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "mcp-for-metabase",
      "args": ["serve", "--transport", "stdio"],
      "env": {
        "METABASE_URL": "https://metabase.example.com",
        "METABASE_API_KEY": "mb_your_key",
        "METABASE_MCP_WRITE_MODE": "read-only",
        "METABASE_MCP_SQL_GUARD_MODE": "strict"
      }
    }
  }
}
```

Claude Code options such as `--transport`, `--scope`, and `--env` must appear before the server name. The command that launches this server comes after `--`.

## Option B: Docker HTTP

Use HTTP when you want a long-running MCP server that multiple clients can connect to.

Build and run against an existing Metabase:

```bash
git clone https://github.com/DominikPollok/mcp-for-metabase.git
cd mcp-for-metabase
docker build -t mcp-for-metabase .
docker run --rm -p 8000:8000 \
  -e METABASE_URL=https://metabase.example.com \
  -e METABASE_API_KEY=mb_your_key \
  -e METABASE_MCP_TRANSPORT=http \
  -e METABASE_MCP_WRITE_MODE=read-only \
  -e METABASE_MCP_SQL_GUARD_MODE=strict \
  -e METABASE_MCP_AUDIT_LOG=/data/audit.log \
  -e METABASE_MCP_SNAPSHOT_DIR=/data/snapshots \
  -v mcp-for-metabase-data:/data \
  mcp-for-metabase
```

The MCP endpoint is:

```text
http://localhost:8000/mcp
```

### Codex HTTP

```bash
codex mcp add metabase --url http://localhost:8000/mcp
codex mcp list
```

Equivalent `~/.codex/config.toml`:

```toml
[mcp_servers.metabase]
url = "http://localhost:8000/mcp"
enabled = true
```

### Claude Code HTTP

```bash
claude mcp add --transport http --scope user metabase http://localhost:8000/mcp
claude mcp list
```

In Claude Code, run `/mcp` and confirm the `metabase` server is connected.

## Option C: Local Playground

Use Docker Compose when you want disposable Metabase, Postgres, and MCP services for testing.

```bash
cp .env.example .env
```

Edit `.env`:

```bash
METABASE_URL=http://metabase:3000
METABASE_IMAGE=metabase/metabase:v0.61.2
METABASE_API_KEY=mb_your_key
METABASE_MCP_TRANSPORT=http
METABASE_MCP_WRITE_MODE=read-only
METABASE_MCP_SQL_GUARD_MODE=strict
METABASE_MCP_AUDIT_LOG=/data/audit.log
METABASE_MCP_SNAPSHOT_DIR=/data/snapshots
```

Start everything:

```bash
docker compose up --build
```

Open Metabase at `http://localhost:3000`. Connect agents to `http://localhost:8000/mcp`.

## Claude Desktop

Add this to `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "mcp-for-metabase",
      "args": ["serve", "--transport", "stdio"],
      "env": {
        "METABASE_URL": "https://metabase.example.com",
        "METABASE_API_KEY": "mb_your_key",
        "METABASE_MCP_WRITE_MODE": "read-only",
        "METABASE_MCP_SQL_GUARD_MODE": "strict"
      }
    }
  }
}
```

Restart Claude Desktop. To reuse this config in Claude Code on macOS or WSL, run:

```bash
claude mcp add-from-claude-desktop
claude mcp list
```

## What To Ask First

After the MCP server is connected, ask the agent:

```text
Use the metabase MCP server. First call metabase_connection_test. Then list available tools and read metabase://agent/connection-guide.
```

For dashboard work, add:

```text
Prefer high-level dashboard, card, collection, and query tools. Use dry_run=true before writes. Do not request all-writes mode unless I explicitly ask for destructive or admin operations.
```

## Safety Settings

| Setting | Recommended first value | When to change it |
| --- | --- | --- |
| `METABASE_MCP_WRITE_MODE` | `read-only` | Use `safe-writes` when the agent may create or update normal content. Use `all-writes` only for explicit admin or destructive workflows with `confirm=true`. |
| `METABASE_MCP_SQL_GUARD_MODE` | `strict` | Use `disabled` only in trusted internal environments where another control already prevents unsafe SQL. |
| `METABASE_MCP_AUDIT_LOG` | `/data/audit.log` for Docker or a local JSONL path | Set whenever writes are enabled. |
| `METABASE_MCP_SNAPSHOT_DIR` | `/data/snapshots` for Docker or a local directory | Set when using snapshot and restore tools. |

API keys inherit the permissions of their Metabase group. Create a dedicated group for agent access instead of reusing a human admin key.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `mcp-for-metabase: command not found` | Install with `pipx install mcp-for-metabase`, install from GitHub with `pipx install git+https://github.com/DominikPollok/mcp-for-metabase.git`, or use an absolute path to the command. |
| Codex does not show tools | Run `codex mcp list`, check `~/.codex/config.toml`, and restart the Codex session or IDE window. |
| Claude Code does not show tools | Run `claude mcp list`, then `/mcp` inside Claude Code. If you used `.mcp.json`, restart Claude Code from that project directory. |
| HTTP client cannot connect | Confirm the MCP server is still running and the client URL ends in `/mcp`. |
| Docker cannot reach local Metabase | Use `METABASE_URL=http://host.docker.internal:3000` on macOS/Windows. On Linux, use a reachable host IP or Docker network name. |
| Metabase returns unauthorized | Regenerate the API key, confirm it belongs to a group with the needed Metabase permissions, and verify `METABASE_URL` has no `/api` suffix. |
| Writes are blocked | Set `METABASE_MCP_WRITE_MODE=safe-writes` for normal content writes. Destructive/admin tools require `all-writes` and `confirm=true`. |

## Generic MCP Client Configs

stdio:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "mcp-for-metabase",
      "args": ["serve", "--transport", "stdio"],
      "env": {
        "METABASE_URL": "https://metabase.example.com",
        "METABASE_API_KEY": "mb_your_key",
        "METABASE_MCP_WRITE_MODE": "read-only",
        "METABASE_MCP_SQL_GUARD_MODE": "strict"
      }
    }
  }
}
```

Streamable HTTP:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```
