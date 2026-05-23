# Architecture

The server is a compatibility-preserving modular monolith. Public modules such as
`server.py`, `tools.py`, `client.py`, `registry.py`, `safety.py`, and `snapshots.py`
remain stable import surfaces, while implementation code is split by responsibility.

1. MCP adapter layer: `mcp_app/` constructs FastMCP, owns resources, prompts, and tool
   registration, and delegates behavior to application or API modules.
2. Application layer: `application/` contains curated Metabase workflows for content,
   snippets, query execution, admin operations, secondary domains, and snapshots.
3. Generic API layer: `api/` contains operation discovery, OpenAPI request validation,
   and the generic `metabase_api_request` executor.
4. Client infrastructure layer: `client.py` owns async HTTP, auth, retries, path
   interpolation, response parsing, audit logging, and safety enforcement.
5. Safety layer: `safety.py` enforces write policy, with shared classification rules
   in `safety_rules.py` used by both runtime requests and registry generation.
6. Registry layer: `registry.py`, `api_registry.json`, and `openapi.json` provide
   generated OpenAPI operation metadata for discovery and generic execution.

All Metabase network calls must route through `MetabaseClient.request(...)`. Curated
tools and the generic executor therefore share the same safety policy, dry-run behavior,
and mutation audit logging.

Metabase API changes are handled by fetching current OpenAPI from a live instance,
regenerating the registry, reviewing safety classifications, and then adding curated
high-level tools only where they improve agent ergonomics.
