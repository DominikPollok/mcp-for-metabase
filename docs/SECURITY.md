# Security

For vulnerability reporting and supported-version policy, see the top-level
[Security Policy](../SECURITY.md).

## Authentication

Use `METABASE_API_KEY` whenever possible. API keys inherit group permissions in Metabase, so create a dedicated group with the minimum permissions required.

Session auth is supported only as a fallback with `METABASE_USERNAME` and `METABASE_PASSWORD`.

For Metabase instances behind a reverse proxy, use `METABASE_BASIC_AUTH_USERNAME`
and `METABASE_BASIC_AUTH_PASSWORD` or `METABASE_HTTP_HEADERS_JSON` for upstream
proxy authentication. Do not embed proxy credentials in `METABASE_URL`; URL
userinfo is more likely to leak through process listings and HTTP client logs.

## Write modes

- `read-only`: default. Mutating requests are blocked.
- `safe-writes`: allows common create/update operations for content.
- `all-writes`: allows admin and destructive operations when `confirm=true` is also provided.

## Native SQL guard

`METABASE_MCP_SQL_GUARD_MODE=strict` is enabled by default. It validates native SQL embedded in dataset queries, cards, native query snippets, and generic API requests before the request reaches Metabase.

Strict mode blocks:

- statement separators and stacked queries;
- SQL comments;
- write/admin keywords such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `MERGE`, `GRANT`, `REVOKE`, `CALL`, `EXECUTE`, `SET`, `INTO`, `OUTFILE`, transaction control, and `USE`;
- full native queries that do not start with a read-only statement token.

This is a defense-in-depth guard for agent-generated SQL. It is not a replacement for least-privileged Metabase groups, read-only database roles, database parameterization, or review of public-link/embed settings.

`METABASE_MCP_SQL_GUARD_MODE=disabled` exists for trusted internal deployments that need dialect-specific SQL outside the strict read-only subset. Do not disable it for shared or production-facing agent workflows unless the underlying database role is read-only and scoped to safe schemas.

## Audit logging

Every mutating HTTP request records method, path, operation ID, request body, status code, and result. Set `METABASE_MCP_AUDIT_LOG` to write JSONL audit events to disk.

## Rollback snapshots

Set `METABASE_MCP_SNAPSHOT_DIR` to control where `metabase_snapshot_entity` stores rollback snapshots. Snapshot files can contain SQL, card definitions, dashboard filters, collection metadata, and permission graphs, so store them with the same access controls as audit logs.

## Direct database writes

This server does not bypass Metabase to write directly to analytics databases. Query execution is routed through the Metabase API and Metabase permissions.
