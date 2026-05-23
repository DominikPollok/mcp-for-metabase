# Agent Development Guide

Start here when developing the project with an agent.

1. Read `AGENTS.md`, `docs/REQUIREMENTS.md`, and `docs/SECURITY.md`.
2. Run the test suite before changing safety-sensitive code.
3. Add new Metabase API operations to the registry through OpenAPI generation whenever possible.
4. Prefer a curated high-level tool when it improves dashboard-building quality.
5. Route every API request through `MetabaseClient.request`.
6. Add tests for allowed, dry-run, blocked, and confirmed paths for any new write tool.
7. Update `docs/TOOL_CATALOG.md` and `docs/API_COVERAGE.md`.

Acceptance for a new tool:

- It has typed parameters.
- It supports `dry_run` if it writes.
- It has unit tests for request shape and safety behavior.
- It has docs and an example call.
