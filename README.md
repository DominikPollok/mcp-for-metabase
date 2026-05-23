# mcp-for-metabase

`mcp-for-metabase` is a safety-gated Python MCP server for Metabase. It lets MCP clients and agents inspect Metabase, run governed queries, and create or maintain dashboards, cards/questions, collections, snippets, permissions, and other Metabase assets through the Metabase REST API.

The server is Docker-first, uses the official MCP Python SDK/FastMCP, and defaults to read-only mode.

## Project Status

This project is in production-readiness beta. It has broad generated Metabase API coverage, curated tools for common dashboard and content workflows, Docker-first deployment, live integration coverage, and restrictive default safety gates. Some lower-frequency API areas are available through the generic executor rather than polished high-level tools.

Current highlights:

- MCP transports: stdio and Streamable HTTP.
- Auth: Metabase API key via `X-API-Key`, with username/password session fallback.
- Generic API coverage: 600 generated operations from the Metabase OpenAPI document.
- Curated tools for discovery, search, metadata inspection, query execution, collections, cards, dashboards, snippets, permissions, users, API keys, public links, copies, card queries, and exports.
- Generic API validation for required path/query/body fields, path/query parameter schemas, and OpenAPI JSON request-body schemas.
- Safety gates: `read-only` by default, `safe-writes` for normal content writes, and `all-writes` plus `confirm=true` for destructive/admin operations.
- `dry_run=true` support for write-capable tools.
- Audit logging for mutating requests.
- CI gates for formatting, linting, typing, unit tests, MCP stdio protocol tests, Docker smoke tests, package checks, generated-registry freshness, and live Metabase integration tests across supported Docker tags.

Detailed capability tables live in [docs/CAPABILITIES.md](docs/CAPABILITIES.md), with generated API coverage in [docs/API_COVERAGE.md](docs/API_COVERAGE.md).
Live test instructions are in [docs/INTEGRATION_TESTING.md](docs/INTEGRATION_TESTING.md).

## Installation

From PyPI, after the first public release:

```bash
python -m pip install mcp-for-metabase
```

From source:

```bash
git clone https://github.com/DominikPollok/mcp-for-metabase.git
cd mcp-for-metabase
python -m pip install -e ".[dev]"
```

The package name and primary console command are both `mcp-for-metabase`. The legacy `metabase-mcp` console command is also installed as a compatibility alias. There are similarly named Metabase MCP packages on PyPI, so check the repository URL and license metadata before installing.

## Quickstart With Docker

Create an environment file:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
METABASE_URL=http://metabase:3000
METABASE_IMAGE=metabase/metabase:v0.61.2
METABASE_API_KEY=your_metabase_api_key
METABASE_MCP_TRANSPORT=http
METABASE_MCP_WRITE_MODE=read-only
METABASE_MCP_SQL_GUARD_MODE=strict
METABASE_MCP_SNAPSHOT_DIR=/data/snapshots
```

Start the stack:

```bash
docker compose up --build
```

The MCP server listens on `http://localhost:8000/mcp` in Streamable HTTP mode. Metabase is exposed on `http://localhost:3000`.

## Running The MCP Server

stdio:

```bash
mcp-for-metabase serve --transport stdio
```

Streamable HTTP:

```bash
mcp-for-metabase serve --transport http --host 0.0.0.0 --port 8000
```

Core environment variables:

| Variable | Required | Description |
| --- | --- | --- |
| `METABASE_URL` | Yes | Metabase base URL. |
| `METABASE_IMAGE` | Optional | Docker Compose Metabase image tag for local integration work. |
| `METABASE_API_KEY` | Recommended | Preferred authentication method. |
| `METABASE_USERNAME` / `METABASE_PASSWORD` | Optional | Session-auth fallback. |
| `METABASE_MCP_TRANSPORT` | Optional | `stdio` or `http`. |
| `METABASE_MCP_WRITE_MODE` | Optional | `read-only`, `safe-writes`, or `all-writes`. |
| `METABASE_MCP_SQL_GUARD_MODE` | Optional | `strict` by default. Use `disabled` only for trusted internal deployments. |
| `METABASE_MCP_AUDIT_LOG` | Optional | JSONL path for mutation audit events. |
| `METABASE_MCP_SNAPSHOT_DIR` | Optional | Directory for durable dashboard/card/collection rollback snapshots. |
| `METABASE_MCP_TIMEOUT` | Optional | HTTP timeout in seconds. |

## Safety Model

The server never bypasses Metabase permissions. API keys inherit their Metabase group permissions, so create a dedicated least-privileged group for agent work.

Write modes:

- `read-only`: default. Read/query operations are allowed; mutations are blocked.
- `safe-writes`: allows common create/update/content operations.
- `all-writes`: allows destructive/admin operations only when the tool call also passes `confirm=true`.

Every mutating request is audited when `METABASE_MCP_AUDIT_LOG` is set. Read [SECURITY.md](SECURITY.md) before connecting the server to production Metabase.

Native SQL guard:

- `strict` is the default and applies to both curated tools and `metabase_api_request`.
- Native SQL is limited to single-statement read-only queries starting with `SELECT`, `WITH`, `EXPLAIN`, `SHOW`, `DESCRIBE`, or `DESC`.
- SQL comments, statement separators, and mutation/admin keywords such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `MERGE`, `GRANT`, and `CALL` are blocked before any request is sent to Metabase.
- Native SQL snippets may be fragments, but the same separator/comment/mutation keyword blocklist applies.
- This guard is defense-in-depth; still use least-privileged Metabase API keys and database roles.

Snapshot tools persist rollback payloads under `METABASE_MCP_SNAPSHOT_DIR`:

- `metabase_snapshot_entity` saves a dashboard, card, collection, or permissions graph snapshot and returns a `snapshot_id`.
- `metabase_list_saved_snapshots` lists saved snapshots.
- `metabase_restore_saved_snapshot` restores by `snapshot_id` with the same write-mode and confirmation gates as direct updates.

Treat snapshot files as sensitive because they can contain dashboard definitions, SQL, collection metadata, and permission graph data.

## Capability Overview

The server exposes the complete generated operation catalog through `metabase_api_request`, with curated high-level tools for the workflows agents need most often.

| Area | MCP support |
| --- | --- |
| API discovery | Native MCP `tools/list`, `resources/list`, `prompts/list`, `metabase://api/coverage`, `metabase://api/operations`, and operation search/get tools. |
| Dashboards | Curated create/get/update/archive/delete/copy, parameters, public links, item/layout management, snapshots, and saved snapshot restore. |
| Cards/questions | Curated create/get/update/archive/delete/copy, query, export, public links, series lookup, and idempotent create-or-update. |
| Collections | Curated tree, create, create-or-update, update, archive, and snapshot/restore. |
| Metadata/querying | Curated database/table metadata reads and governed dataset/card query execution. |
| Snippets | Curated list/get/create/update/create-or-update native SQL snippets. |
| Admin/security | Curated permissions graph, permission groups, users, settings, API keys, and database sync/rescan helpers with admin gates. |
| Notifications | Curated pulse list/get/create/update/delete subscription helpers. |
| Content management | Curated bookmarks, revisions, timelines, timeline events, segments, documents, and cache operations. |
| Remaining Metabase API | Available through `metabase_api_request` with registry discovery, schema validation, safety classification, dry-run support, and audit logging for mutations. |

## Connecting Agents

Read [docs/CONNECTING_AGENTS.md](docs/CONNECTING_AGENTS.md) or use the optional Codex skill at [.codex/skills/connect-metabase-agents/SKILL.md](.codex/skills/connect-metabase-agents/SKILL.md).

Example stdio client config:

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

Agents should start with native MCP discovery:

1. Call `tools/list`.
2. Call `resources/list`.
3. Call `resourceTemplates/list`.
4. Call `prompts/list`.
5. Read `metabase://agent/connection-guide`.
6. Read `metabase://api/coverage` or call `metabase_discover_operations`.

## Local Development

Recommended:

```bash
uv sync --all-extras
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
```

Run the disposable live integration path:

```bash
docker compose up -d postgres metabase
uv run python scripts/bootstrap_metabase_test_instance.py --output-env .metabase-test.env
set -a && . ./.metabase-test.env && set +a
uv run pytest tests/integration -q --no-cov
docker compose down -v
```

Fallback without `uv`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
```

Build and inspect distributions:

```bash
python -m build
twine check dist/*
```

## API Registry

Refresh the registry from the official public docs:

```bash
python scripts/fetch_openapi.py --output docs/openapi.json
python scripts/build_api_registry.py --openapi docs/openapi.json
```

Refresh from a live instance:

```bash
python scripts/fetch_openapi.py \
  --base-url "$METABASE_URL" \
  --api-key "$METABASE_API_KEY" \
  --output docs/openapi.json
python scripts/build_api_registry.py --openapi docs/openapi.json
```

Compare two generated registry snapshots before upgrading Metabase docs:

```bash
python scripts/diff_api_registry.py \
  --old src/mcp_for_metabase/api_registry.json \
  --new /tmp/new_api_registry.json \
  --format markdown \
  --fail-on-removal
```

Generated outputs:

- `src/mcp_for_metabase/api_registry.json`
- `src/mcp_for_metabase/openapi.json`
- `docs/API_COVERAGE.md`

`docs/openapi.json` is intentionally ignored because it is a temporary fetch target. The runtime package includes the normalized OpenAPI snapshot under `src/mcp_for_metabase/openapi.json`.

## Documentation

- [Requirements](docs/REQUIREMENTS.md)
- [Definition of Done](docs/DEFINITION_OF_DONE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Security](SECURITY.md)
- [Tool catalog](docs/TOOL_CATALOG.md)
- [Capabilities](docs/CAPABILITIES.md)
- [API coverage](docs/API_COVERAGE.md)
- [Implementation status](docs/IMPLEMENTATION_STATUS.md)
- [Agent development guide](docs/AGENT_DEVELOPMENT_GUIDE.md)
- [Connecting agents](docs/CONNECTING_AGENTS.md)
- [Compatibility](docs/COMPATIBILITY.md)
- [Dependency licenses](docs/DEPENDENCY_LICENSES.md)
- [Release checklist](docs/RELEASE_CHECKLIST.md)

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), keep changes small, and preserve the safety gates around Metabase mutations.

The `.codex/skills` directory is intentionally included as optional agent workflow guidance for contributors who use Codex or compatible agent tooling.

## License

`mcp-for-metabase` is licensed under `GPL-3.0-or-later`. See [LICENSE](LICENSE).
