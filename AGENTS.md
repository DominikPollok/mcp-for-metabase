# Agent Guide

This repository is built for agent-based development. Favor small, tested changes and keep safety gates intact.

## Source of truth

- Metabase API docs: https://www.metabase.com/docs/latest/api
- Metabase API changelog: https://www.metabase.com/docs/latest/developers-guide/api-changelog
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Requirements: `docs/REQUIREMENTS.md`
- Definition of Done: `docs/DEFINITION_OF_DONE.md`

## Commands

```bash
uv sync --all-extras
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy src
```

Fallback without `uv`:

```bash
python -m pip install -e ".[dev]"
pytest
```

## Safety rules

- Never bypass `SafetyPolicy` for Metabase mutations.
- Never bypass `enforce_sql_guard` for native SQL. All request bodies must go through `MetabaseClient.request` so native queries, cards, snippets, and generic API calls are inspected before reaching Metabase.
- New mutating tools must support `dry_run`.
- Destructive or admin operations must require `METABASE_MCP_WRITE_MODE=all-writes` and `confirm=true`.
- Keep audit logging on every request with method other than `GET`, `HEAD`, or `OPTIONS`.
- Keep native SQL read-only by default. Prefer Metabase variables such as `{{value}}` over literal interpolation, and document any reason for setting `METABASE_MCP_SQL_GUARD_MODE=disabled`.
- Prefer high-level tools for dashboard authoring; use the generic executor for coverage gaps.

## Adding API coverage

1. Fetch current OpenAPI from a live Metabase instance with `scripts/fetch_openapi.py`.
2. Regenerate the runtime registry with `scripts/build_api_registry.py`.
3. Add or update high-level tools only when they improve agent ergonomics.
4. Update `docs/TOOL_CATALOG.md`, `docs/API_COVERAGE.md`, and tests.
