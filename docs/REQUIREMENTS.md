# Requirements

## Functional requirements

- Expose Metabase metadata, collections, cards/questions, dashboards, snippets, models, metrics, timelines, permissions, and administrative endpoints through MCP.
- Provide high-level tools for clean dashboard authoring.
- Provide a generic OpenAPI-backed executor for API operations without curated tools.
- Support Docker deployment and local stdio operation.
- Support API-key auth and session-auth fallback.
- Support dry-runs for write-capable operations.
- Maintain an API coverage report generated from OpenAPI.

## Non-functional requirements

- Default to read-only.
- Require explicit write mode for all mutations.
- Require `confirm=true` for destructive and admin operations.
- Record audit logs for every mutating request.
- Keep implementation typed, tested, and compatible with current Metabase API behavior.
