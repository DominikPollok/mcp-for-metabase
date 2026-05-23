# Implementation Status

## Implemented

- Python package, CLI, Dockerfile, Docker Compose, CI, and `uv.lock`.
- FastMCP server with stdio and Streamable HTTP support.
- Metabase client with API-key auth, session-auth fallback, retries, structured errors, safety checks, path-parameter interpolation, dry-runs, and mutation audit logging.
- Generated API registry with 600 operations from the official public Metabase OpenAPI document.
- Generic `metabase_api_request` executor for all generated operations with required field validation, path/query parameter schema validation, and OpenAPI JSON request-body schema validation.
- MCP-native discovery through tools, resources, resource templates, and prompts.
- Discovery helpers: `metabase_discover_operations`, `metabase_get_operation`, `metabase://api/coverage`, `metabase://api/operations`, and `metabase://agent/connection-guide`.
- Curated high-level tools for connection testing, search, database/table metadata, query execution, collections, cards, dashboards, dashboard card layout, SQL snippets, permissions, users, API keys, public links, copies, card queries, card exports, pulses, bookmarks, revisions, timelines, segments, documents, and cache operations.
- Durable local rollback snapshot store for dashboards, cards, collections, and permissions graphs.
- MCP stdio protocol test coverage using the official MCP client.
- CI matrix for Python 3.12/3.13 plus Docker smoke tests, generated-registry freshness checks, package checks, and live Metabase integration tests against `v0.59.7`, `v0.60.6`, and `v0.61.2`.

## Remaining Full API Ergonomics Work

- Curated MCP tools for lower-frequency domains such as actions, alerts, embedding, transforms, serialization, uploads, moderation, SCIM, and other Enterprise-specific workflows. The generic executor covers them, but agents get a better experience when important workflows have typed high-level tools.
- Non-JSON request/response validation before sending generic calls. Path/query parameter schema validation and JSON request-body schema validation are implemented.
- Idempotent create-or-update workflows across all content types.
- One-step transactional wrappers that snapshot, mutate, and roll back automatically on failed multi-call dashboard workflows.
- Generated examples for each major API group.

## Coverage Snapshot

The generated registry currently contains:

- 600 total operations.
- 315 read operations.
- 192 safe-write operations.
- 33 destructive operations.
- 60 admin operations.

The exact numbers may change whenever Metabase updates `https://www.metabase.com/docs/latest/api.json`.
