# Security Policy

## Reporting Vulnerabilities

Please report security issues privately through GitHub Security Advisories for this repository. If advisories are unavailable, contact the maintainer through a private channel before opening a public issue.

Do not include real Metabase API keys, session tokens, dashboard public links, SQL containing confidential data, or production audit logs in public reports.

## Supported Versions

Until the first stable release, security fixes target the latest `main` branch and the latest PyPI release, if one has been published.

## Operational Model

`mcp-for-metabase` does not bypass Metabase permissions. API keys and session credentials inherit the permissions configured in Metabase, so production deployments should use a dedicated least-privileged Metabase group.

Write modes are intentionally restrictive:

- `read-only`: default. Mutating requests are blocked.
- `safe-writes`: allows ordinary content create/update workflows.
- `all-writes`: allows destructive and admin operations only when the tool call also passes `confirm=true`.

Every write-capable tool must support `dry_run`, and every mutating HTTP request must be audit logged when `METABASE_MCP_AUDIT_LOG` is configured.

Native SQL is guarded by default with `METABASE_MCP_SQL_GUARD_MODE=strict`. The guard blocks stacked statements, comments, mutating/admin SQL keywords, and non-read-only native query starts before requests reach Metabase. Treat it as defense-in-depth and still use read-only database roles for agent-accessible data sources.

## Secret Handling

- Store credentials in environment variables or secret managers, not in source files.
- Keep `.env`, audit logs, rollback snapshots, and generated OpenAPI snapshots out of git.
- Rotate Metabase API keys after accidental disclosure.
- Prefer API-key auth over username/password session auth.

Additional implementation details are documented in [docs/SECURITY.md](docs/SECURITY.md).
