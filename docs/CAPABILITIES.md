# Capabilities

`mcp-for-metabase` combines curated MCP tools for common workflows with a generated OpenAPI-backed executor for broader Metabase API coverage.

Support levels:

- **Curated tools**: dedicated MCP tools/resources/prompts with ergonomic typed inputs for common agent workflows.
- **Generic API**: available through `metabase_discover_operations`, `metabase_get_operation`, and `metabase_api_request`.
- **Safety-gated**: write, destructive, or admin operations require the configured write mode and sometimes `confirm=true`.
- **SQL-guarded**: native SQL in curated tools and the generic executor is inspected by the default strict read-only SQL guard.
- **Planned**: the API is discoverable, but richer validation, examples, or high-level workflows are still missing.

| Metabase API area | Generated operations | Current MCP support | Notes |
| --- | ---: | --- | --- |
| API discovery and coverage | 600 total | Curated tools + resources | `metabase_discover_operations`, `metabase_get_operation`, `metabase://api/coverage`, and `metabase://api/operations`. |
| Dashboard authoring | 25 dashboard ops | Curated tools + generic API | Create/get/update/archive/delete/copy dashboards, public links, parameters, tabs via layout updates, compact dashboard reads, durable snapshots, saved snapshot restore, and dashboard card layouts are curated. Subscriptions are generic today. |
| Cards/questions/models | 20 card ops | Curated tools + generic API | Create/get/update/archive/delete/copy/query/export/public-link card workflows, series reads, and durable snapshots are curated. Remapping helpers are generic. |
| Collections | 16 ops | Curated tools + generic API | Create, create-or-update, update, archive, and tree are covered; item movement and detailed collection item APIs are generic. |
| Databases, tables, fields, metadata | 31 database ops, 16 table ops, 12 field ops | Curated read tools + generic API | Database metadata inspection is curated. Database/table/field admin writes are generic and safety-gated. |
| Query execution and datasets | 8 dataset ops | Curated query tool + generic API | `POST /api/dataset` and dataset query paths are classified as read/query operations; native SQL is blocked unless it passes the strict read-only SQL guard. |
| Search and activity | Search + activity ops | Curated search + generic API | Search has a high-level tool; recents/activity APIs are generic. |
| Native query snippets | 5 snippet-related ops | Curated tools + generic API | Create and update snippets are curated; list/get and Enterprise dependency checks are generic. |
| Permissions | 14 ops | Curated read/write helpers + generic API, admin-gated | Permissions graph reads, group reads, and permissions graph writes are curated. Writes require `all-writes` and `confirm=true`. A safer guided diff workflow is planned. |
| Users, groups, sessions, API keys | 25+ ops | Curated core tools + generic API, admin/destructive-gated | Users and API keys have curated list/get/create/update/delete helpers where appropriate. Session and advanced membership flows remain generic. |
| Actions and writeback workflows | 10 action ops | Generic API, safety-gated | Actions can write to underlying databases through Metabase; endpoint-specific safety tuning and curated tools are planned. |
| Alerts, pulses, notifications, subscriptions | 20+ ops | Curated pulse helpers + generic API | Pulse list/get/create/update/delete-subscription is curated. Alert and notification APIs remain generic. |
| Embedding, public links, preview embed, themes | 35+ ops | Curated public-link tools + generic API | Card and dashboard public links are curated. Embed/preview/theme management remains generic. |
| Metrics, measures, segments, timelines | 25+ ops | Curated segment/timeline helpers + generic API | Segment and timeline CRUD/event helpers are curated. Metrics/measures remain generic. |
| Snippets, documents, comments, bookmarks, revisions | 30+ ops | Curated document/bookmark/revision helpers + generic API | Documents, bookmarks, and revision reads/reverts are curated. Comments and moderation remain generic. |
| Cache, persistence, transforms, tasks | 35+ ops | Curated cache helpers + generic API, safety-gated | Cache config, invalidation, and clearing are curated. Persistence, transforms, and tasks remain generic. |
| Enterprise endpoints (`/api/ee/*`, SCIM, serialization, tenant, remote sync) | 80+ ops | Generic API, safety-gated | Exposed when the target Metabase supports them; compatibility tests and curated workflows are planned. |
| Public and anonymous endpoints | 24 public ops | Generic API | Available through generated operations; use carefully because public-link behavior depends on instance settings. |

Generated registry safety snapshot:

| Safety tier | Operations | Behavior |
| --- | ---: | --- |
| `read` | 316 | Allowed in `read-only` mode. |
| `safe-write` | 193 | Requires `METABASE_MCP_WRITE_MODE=safe-writes` or `all-writes`, unless `dry_run=true`. |
| `destructive` | 33 | Requires `all-writes` and `confirm=true`, unless `dry_run=true`. |
| `admin` | 58 | Requires `all-writes` and `confirm=true`, unless `dry_run=true`. |

## Known Gaps

- Add curated tools for more Metabase domains: actions, alerts/notifications, subscriptions, embedding, transforms, serialization, uploads, moderation, and Enterprise endpoints.
- Expand OpenAPI validation to cover non-JSON request/response shapes. Path/query parameter schema validation and JSON request-body schema validation are implemented.
- Expand live integration tests beyond the current dashboard lifecycle into permissions, public links, documents, cache, and admin flows.
- Add one-step transactional wrappers that snapshot, mutate, and roll back automatically on failed multi-call dashboard workflows. Durable snapshot and restore tools are implemented.
- Add richer idempotent `create_or_update_*` helpers for dashboards, cards, snippets, collections, models, metrics, and permissions.
- Keep compatibility CI current as new Metabase Docker tags become available.
