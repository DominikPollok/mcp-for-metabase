# Tool Catalog

## Read tools

- `metabase_connection_test`: verifies auth and returns instance properties.
- `metabase_discover_operations`: searches the generated Metabase API catalog.
- `metabase_get_operation`: returns method, path, tags, parameters, docs metadata, and safety tier for one operation.
- `metabase_snapshot_entity`: snapshots a dashboard, card, collection, or permissions graph and persists it locally.
- `metabase_list_saved_snapshots`: lists locally persisted rollback snapshots.
- `metabase_search`: searches cards, dashboards, collections, and related content.
- `metabase_collection_tree`: returns the visible collection hierarchy.
- `metabase_list_databases`: lists databases visible to the API key.
- `metabase_get_database_metadata`: inspects database schemas, tables, and fields.
- `metabase_get_table_metadata`: inspects a table's query metadata.
- `metabase_get_permissions_graph`: reads the full permissions graph.
- `metabase_list_permission_groups`: lists permission groups.
- `metabase_get_permission_group`: reads one permission group.
- `metabase_list_users`: lists users.
- `metabase_get_user`: reads one user.
- `metabase_list_api_keys`: lists API keys.
- `metabase_list_bookmarks`: lists bookmarks.
- `metabase_list_revisions`: lists revision history for an entity.
- `metabase_list_timelines`: lists timelines.
- `metabase_get_timeline`: gets a timeline.
- `metabase_list_segments`: lists segments.
- `metabase_get_segment`: gets a segment.
- `metabase_list_documents`: lists documents.
- `metabase_get_document`: gets a document.
- `metabase_get_cache_config`: gets cache configuration.

## Dashboard authoring tools

- `metabase_create_collection`: creates a collection.
- `metabase_create_or_update_collection`: creates a collection or updates an exact-name match.
- `metabase_restore_snapshot`: restores an inline snapshot created by `metabase_snapshot_entity`.
- `metabase_restore_saved_snapshot`: restores a persisted snapshot by `snapshot_id`.
- `metabase_update_collection`: updates a collection.
- `metabase_archive_collection`: moves a collection to trash.
- `metabase_create_card`: creates a question/card.
- `metabase_create_or_update_card`: creates a card/question or updates an exact-name match.
- `metabase_get_card`: returns a card/question.
- `metabase_update_card`: updates a card/question.
- `metabase_archive_card`: moves a card/question to trash.
- `metabase_delete_card`: deletes a card/question with destructive confirmation gates.
- `metabase_copy_card`: copies a card/question.
- `metabase_run_card_query`: runs a saved card/question query.
- `metabase_export_card_query`: exports a saved card/question query.
- `metabase_create_card_public_link`: creates or returns a card public link.
- `metabase_delete_card_public_link`: deletes a card public link with destructive confirmation gates.
- `metabase_create_dashboard`: creates a dashboard.
- `metabase_create_or_update_dashboard`: creates a dashboard or updates an exact-name match.
- `metabase_get_dashboard`: returns a dashboard.
- `metabase_update_dashboard`: updates dashboard metadata, settings, or parameters.
- `metabase_update_dashboard_parameters`: replaces dashboard filters/parameters.
- `metabase_get_dashboard_items`: lists dashboard items/cards.
- `metabase_archive_dashboard`: moves a dashboard to trash.
- `metabase_delete_dashboard`: deletes a dashboard with destructive confirmation gates.
- `metabase_copy_dashboard`: copies a dashboard.
- `metabase_create_dashboard_public_link`: creates or returns a dashboard public link.
- `metabase_delete_dashboard_public_link`: deletes a dashboard public link with destructive confirmation gates.
- `metabase_add_dashboard_card`: adds a card to a dashboard with grid position.
- `metabase_update_dashboard_cards`: replaces/updates dashboard card layout via `PUT /api/dashboard/{id}/cards`.
- `metabase_remove_dashboard_card`: removes a dashcard from a dashboard with destructive confirmation gates.
- `metabase_run_query`: runs a Metabase dataset query.
- `metabase_create_native_query_snippet`: creates a reusable SQL snippet.
- `metabase_list_native_query_snippets`: lists reusable SQL snippets.
- `metabase_get_native_query_snippet`: gets a reusable SQL snippet.
- `metabase_update_native_query_snippet`: updates a reusable SQL snippet.
- `metabase_create_or_update_native_query_snippet`: creates a SQL snippet or updates an exact-name match.
- `metabase_update_permissions_graph`: updates the permissions graph with admin confirmation gates.
- `metabase_create_user`: creates a user with admin confirmation gates.
- `metabase_update_user`: updates a user with admin confirmation gates.
- `metabase_create_api_key`: creates an API key.
- `metabase_update_api_key`: updates an API key.
- `metabase_delete_api_key`: deletes an API key with destructive confirmation gates.
- `metabase_get_settings`: lists visible instance settings.
- `metabase_get_setting`: gets one instance setting.
- `metabase_update_setting`: updates one instance setting with admin confirmation gates.
- `metabase_update_database`: updates database configuration.
- `metabase_sync_database_schema`: triggers database schema sync.
- `metabase_rescan_database_values`: triggers database field value rescanning.
- `metabase_list_pulses`: lists pulses/subscriptions.
- `metabase_get_pulse`: gets one pulse/subscription.
- `metabase_create_pulse`: creates a pulse/subscription.
- `metabase_update_pulse`: updates a pulse/subscription.
- `metabase_delete_pulse_subscription`: deletes a pulse subscription with destructive confirmation gates.
- `metabase_create_bookmark`: creates a bookmark.
- `metabase_delete_bookmark`: removes a bookmark with destructive confirmation gates.
- `metabase_update_bookmark_ordering`: updates bookmark ordering.
- `metabase_revert_revision`: reverts an entity to a previous revision.
- `metabase_create_timeline`: creates a timeline.
- `metabase_update_timeline`: updates a timeline.
- `metabase_delete_timeline`: deletes a timeline with destructive confirmation gates.
- `metabase_create_timeline_event`: creates a timeline event.
- `metabase_update_timeline_event`: updates a timeline event.
- `metabase_delete_timeline_event`: deletes a timeline event with destructive confirmation gates.
- `metabase_create_segment`: creates a segment.
- `metabase_update_segment`: updates a segment.
- `metabase_delete_segment`: deletes a segment with destructive confirmation gates.
- `metabase_create_document`: creates a document.
- `metabase_update_document`: updates a document.
- `metabase_delete_document`: deletes a document with destructive confirmation gates.
- `metabase_copy_document`: copies a document.
- `metabase_update_cache_config`: updates cache configuration.
- `metabase_invalidate_cache`: invalidates cache entries.
- `metabase_clear_cache`: clears cache with destructive confirmation gates.

All write-capable dashboard authoring tools accept `dry_run`.

## Generic tool

- `metabase_api_request`: calls an operation from the OpenAPI registry with `operation_id`, `path_params`, `query`, `body`, `dry_run`, and `confirm`.

Use the generic tool for API areas that are not yet ergonomic enough for a curated high-level MCP tool.
The generic tool validates required path parameters, required query parameters, path/query parameter schemas, required top-level JSON body fields, and JSON request-body schemas before sending the request.

The generated registry currently covers 600 operations from the official Metabase OpenAPI document.

Native SQL passed through curated tools or `metabase_api_request` is inspected by the default strict SQL guard before any request is sent to Metabase. Use Metabase variables such as `{{value}}` instead of string concatenation, and keep the underlying database role read-only for agent-accessible connections.
