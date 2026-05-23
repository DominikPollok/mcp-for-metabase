# Definition of Done

The project is done when:

- A new contributor can clone the repo, configure `.env`, run Docker Compose, and create a test dashboard end to end.
- Every MCP tool has typed inputs, structured output, documentation, examples, safety classification, and tests.
- `docs/API_COVERAGE.md` lists every OpenAPI operation as implemented, generically available, intentionally blocked, or unsupported.
- No write-capable path can mutate a real Metabase instance unless `METABASE_MCP_WRITE_MODE` and confirmation requirements pass.
- CI passes formatting, linting, typing, unit tests, integration tests, MCP protocol tests, and coverage gates.
- Security docs explain auth, permissions, write modes, audit logs, and operational risks.
