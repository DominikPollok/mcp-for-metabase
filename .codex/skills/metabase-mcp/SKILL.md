# Metabase MCP Skill

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

Use this skill when adding or changing MCP tools for Metabase.

## Workflow

1. Read `AGENTS.md`, `docs/REQUIREMENTS.md`, and `docs/SECURITY.md`.
2. Confirm whether the endpoint exists in `src/mcp_for_metabase/api_registry.json`.
3. If missing, fetch OpenAPI from a live Metabase instance and regenerate the registry.
4. Implement high-level behavior in the appropriate `src/mcp_for_metabase/application/*.py` module, then re-export stable helpers from `src/mcp_for_metabase/tools.py` when needed.
5. Register MCP tools/resources/prompts in `src/mcp_for_metabase/mcp_app/*.py`; `src/mcp_for_metabase/server.py` only exposes the app factory.
6. Route all HTTP through `MetabaseClient.request`.
7. Add tests for request shape, safety gates, and native SQL guard behavior when the endpoint can carry SQL.
8. Update `docs/TOOL_CATALOG.md`.

## Safety

Never send write requests directly through `httpx`. Use `SafetyPolicy` through `MetabaseClient`.

Never send Metabase native SQL directly through `httpx`. Keep SQL-carrying request bodies on the `MetabaseClient.request` path so `enforce_sql_guard` can block stacked statements, comments, mutating/admin keywords, and non-read-only native query starts before the request reaches Metabase. Use Metabase template variables for parameters and keep agent-accessible database roles read-only.
