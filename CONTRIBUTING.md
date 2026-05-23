# Contributing

Thanks for contributing to `mcp-for-metabase`. This project is safety-sensitive because it can operate against real Metabase instances, so small, reviewed changes with tests are preferred.

## Development Setup

Use `uv` when available:

```bash
uv sync --all-extras
```

Fallback:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Required Checks

Run these before opening a pull request:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
```

Fallback without `uv`:

```bash
ruff format --check .
ruff check .
mypy src
pytest
```

## Safety Rules

- Never bypass `SafetyPolicy` for Metabase mutations.
- New write-capable tools must support `dry_run`.
- Destructive or admin operations must require `METABASE_MCP_WRITE_MODE=all-writes` and `confirm=true`.
- Route all Metabase HTTP requests through `MetabaseClient.request`.
- Keep audit logging enabled for every request with method other than `GET`, `HEAD`, or `OPTIONS`.

## Pull Requests

- Keep changes focused and explain the behavior change.
- Add or update tests for new tools, safety gates, request validation, and error paths.
- Update docs when tool behavior, environment variables, API coverage, or safety behavior changes.
- For API coverage changes, regenerate `src/mcp_for_metabase/api_registry.json` and `docs/API_COVERAGE.md` from OpenAPI.
- Do not commit `.env`, audit logs, `docs/openapi.json`, caches, or build artifacts.

## Agent Assets

The `.codex/skills` files are public project assets for agent-assisted development. Keep them aligned with `AGENTS.md`, `docs/REQUIREMENTS.md`, and `docs/SECURITY.md`.
