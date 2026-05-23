# SPDX-License-Identifier: GPL-3.0-or-later
from mcp_for_metabase.api.discovery import (
    discover_operations as discover_operations,
)
from mcp_for_metabase.api.discovery import (
    get_operation as get_operation,
)
from mcp_for_metabase.api.discovery import (
    operation_to_dict as operation_to_dict,
)
from mcp_for_metabase.api.executor import (
    metabase_api_request as metabase_api_request,
)
from mcp_for_metabase.api.validation import (
    validate_api_request as validate_api_request,
)
from mcp_for_metabase.application.admin import (
    create_api_key as create_api_key,
)
from mcp_for_metabase.application.admin import (
    create_card_public_link as create_card_public_link,
)
from mcp_for_metabase.application.admin import (
    create_dashboard_public_link as create_dashboard_public_link,
)
from mcp_for_metabase.application.admin import (
    create_user as create_user,
)
from mcp_for_metabase.application.admin import (
    delete_api_key as delete_api_key,
)
from mcp_for_metabase.application.admin import (
    delete_card_public_link as delete_card_public_link,
)
from mcp_for_metabase.application.admin import (
    delete_dashboard_public_link as delete_dashboard_public_link,
)
from mcp_for_metabase.application.admin import (
    get_permission_group as get_permission_group,
)
from mcp_for_metabase.application.admin import (
    get_permissions_graph as get_permissions_graph,
)
from mcp_for_metabase.application.admin import (
    get_setting as get_setting,
)
from mcp_for_metabase.application.admin import (
    get_settings as get_settings,
)
from mcp_for_metabase.application.admin import (
    get_user as get_user,
)
from mcp_for_metabase.application.admin import (
    list_api_keys as list_api_keys,
)
from mcp_for_metabase.application.admin import (
    list_permission_groups as list_permission_groups,
)
from mcp_for_metabase.application.admin import (
    list_users as list_users,
)
from mcp_for_metabase.application.admin import (
    rescan_database_values as rescan_database_values,
)
from mcp_for_metabase.application.admin import (
    sync_database_schema as sync_database_schema,
)
from mcp_for_metabase.application.admin import (
    update_api_key as update_api_key,
)
from mcp_for_metabase.application.admin import (
    update_database as update_database,
)
from mcp_for_metabase.application.admin import (
    update_permissions_graph as update_permissions_graph,
)
from mcp_for_metabase.application.admin import (
    update_setting as update_setting,
)
from mcp_for_metabase.application.admin import (
    update_user as update_user,
)
from mcp_for_metabase.application.content import (
    add_dashboard_card as add_dashboard_card,
)
from mcp_for_metabase.application.content import (
    archive_card as archive_card,
)
from mcp_for_metabase.application.content import (
    archive_collection as archive_collection,
)
from mcp_for_metabase.application.content import (
    archive_dashboard as archive_dashboard,
)
from mcp_for_metabase.application.content import (
    collection_tree as collection_tree,
)
from mcp_for_metabase.application.content import (
    copy_card as copy_card,
)
from mcp_for_metabase.application.content import (
    copy_dashboard as copy_dashboard,
)
from mcp_for_metabase.application.content import (
    create_card as create_card,
)
from mcp_for_metabase.application.content import (
    create_collection as create_collection,
)
from mcp_for_metabase.application.content import (
    create_dashboard as create_dashboard,
)
from mcp_for_metabase.application.content import (
    create_or_update_card as create_or_update_card,
)
from mcp_for_metabase.application.content import (
    create_or_update_collection as create_or_update_collection,
)
from mcp_for_metabase.application.content import (
    create_or_update_dashboard as create_or_update_dashboard,
)
from mcp_for_metabase.application.content import (
    delete_card as delete_card,
)
from mcp_for_metabase.application.content import (
    delete_dashboard as delete_dashboard,
)
from mcp_for_metabase.application.content import (
    get_card as get_card,
)
from mcp_for_metabase.application.content import (
    get_dashboard as get_dashboard,
)
from mcp_for_metabase.application.content import (
    get_dashboard_items as get_dashboard_items,
)
from mcp_for_metabase.application.content import (
    remove_dashboard_card as remove_dashboard_card,
)
from mcp_for_metabase.application.content import (
    update_card as update_card,
)
from mcp_for_metabase.application.content import (
    update_collection as update_collection,
)
from mcp_for_metabase.application.content import (
    update_dashboard as update_dashboard,
)
from mcp_for_metabase.application.content import (
    update_dashboard_cards as update_dashboard_cards,
)
from mcp_for_metabase.application.content import (
    update_dashboard_parameters as update_dashboard_parameters,
)
from mcp_for_metabase.application.query import (
    connection_test as connection_test,
)
from mcp_for_metabase.application.query import (
    export_card_query as export_card_query,
)
from mcp_for_metabase.application.query import (
    get_card_series as get_card_series,
)
from mcp_for_metabase.application.query import (
    get_database_metadata as get_database_metadata,
)
from mcp_for_metabase.application.query import (
    get_table_metadata as get_table_metadata,
)
from mcp_for_metabase.application.query import (
    list_databases as list_databases,
)
from mcp_for_metabase.application.query import (
    run_card_query as run_card_query,
)
from mcp_for_metabase.application.query import (
    run_query as run_query,
)
from mcp_for_metabase.application.query import (
    search as search,
)
from mcp_for_metabase.application.secondary import (
    clear_cache as clear_cache,
)
from mcp_for_metabase.application.secondary import (
    copy_document as copy_document,
)
from mcp_for_metabase.application.secondary import (
    create_bookmark as create_bookmark,
)
from mcp_for_metabase.application.secondary import (
    create_document as create_document,
)
from mcp_for_metabase.application.secondary import (
    create_pulse as create_pulse,
)
from mcp_for_metabase.application.secondary import (
    create_segment as create_segment,
)
from mcp_for_metabase.application.secondary import (
    create_timeline as create_timeline,
)
from mcp_for_metabase.application.secondary import (
    create_timeline_event as create_timeline_event,
)
from mcp_for_metabase.application.secondary import (
    delete_bookmark as delete_bookmark,
)
from mcp_for_metabase.application.secondary import (
    delete_document as delete_document,
)
from mcp_for_metabase.application.secondary import (
    delete_pulse_subscription as delete_pulse_subscription,
)
from mcp_for_metabase.application.secondary import (
    delete_segment as delete_segment,
)
from mcp_for_metabase.application.secondary import (
    delete_timeline as delete_timeline,
)
from mcp_for_metabase.application.secondary import (
    delete_timeline_event as delete_timeline_event,
)
from mcp_for_metabase.application.secondary import (
    get_cache_config as get_cache_config,
)
from mcp_for_metabase.application.secondary import (
    get_document as get_document,
)
from mcp_for_metabase.application.secondary import (
    get_pulse as get_pulse,
)
from mcp_for_metabase.application.secondary import (
    get_segment as get_segment,
)
from mcp_for_metabase.application.secondary import (
    get_timeline as get_timeline,
)
from mcp_for_metabase.application.secondary import (
    invalidate_cache as invalidate_cache,
)
from mcp_for_metabase.application.secondary import (
    list_bookmarks as list_bookmarks,
)
from mcp_for_metabase.application.secondary import (
    list_documents as list_documents,
)
from mcp_for_metabase.application.secondary import (
    list_pulses as list_pulses,
)
from mcp_for_metabase.application.secondary import (
    list_revisions as list_revisions,
)
from mcp_for_metabase.application.secondary import (
    list_segments as list_segments,
)
from mcp_for_metabase.application.secondary import (
    list_timelines as list_timelines,
)
from mcp_for_metabase.application.secondary import (
    revert_revision as revert_revision,
)
from mcp_for_metabase.application.secondary import (
    update_bookmark_ordering as update_bookmark_ordering,
)
from mcp_for_metabase.application.secondary import (
    update_cache_config as update_cache_config,
)
from mcp_for_metabase.application.secondary import (
    update_document as update_document,
)
from mcp_for_metabase.application.secondary import (
    update_pulse as update_pulse,
)
from mcp_for_metabase.application.secondary import (
    update_segment as update_segment,
)
from mcp_for_metabase.application.secondary import (
    update_timeline as update_timeline,
)
from mcp_for_metabase.application.secondary import (
    update_timeline_event as update_timeline_event,
)
from mcp_for_metabase.application.snapshot_workflows import (
    restore_snapshot as restore_snapshot,
)
from mcp_for_metabase.application.snapshot_workflows import (
    snapshot_entity as snapshot_entity,
)
from mcp_for_metabase.application.snippets import (
    create_native_query_snippet as create_native_query_snippet,
)
from mcp_for_metabase.application.snippets import (
    create_or_update_native_query_snippet as create_or_update_native_query_snippet,
)
from mcp_for_metabase.application.snippets import (
    get_native_query_snippet as get_native_query_snippet,
)
from mcp_for_metabase.application.snippets import (
    list_native_query_snippets as list_native_query_snippets,
)
from mcp_for_metabase.application.snippets import (
    update_native_query_snippet as update_native_query_snippet,
)

__all__ = [
    "add_dashboard_card",
    "archive_card",
    "archive_collection",
    "archive_dashboard",
    "clear_cache",
    "collection_tree",
    "connection_test",
    "copy_card",
    "copy_dashboard",
    "copy_document",
    "create_api_key",
    "create_bookmark",
    "create_card",
    "create_card_public_link",
    "create_collection",
    "create_dashboard",
    "create_dashboard_public_link",
    "create_document",
    "create_native_query_snippet",
    "create_or_update_card",
    "create_or_update_collection",
    "create_or_update_dashboard",
    "create_or_update_native_query_snippet",
    "create_pulse",
    "create_segment",
    "create_timeline",
    "create_timeline_event",
    "create_user",
    "delete_api_key",
    "delete_bookmark",
    "delete_card",
    "delete_card_public_link",
    "delete_dashboard",
    "delete_dashboard_public_link",
    "delete_document",
    "delete_pulse_subscription",
    "delete_segment",
    "delete_timeline",
    "delete_timeline_event",
    "discover_operations",
    "export_card_query",
    "get_cache_config",
    "get_card",
    "get_card_series",
    "get_dashboard",
    "get_dashboard_items",
    "get_database_metadata",
    "get_document",
    "get_native_query_snippet",
    "get_operation",
    "get_permission_group",
    "get_permissions_graph",
    "get_pulse",
    "get_segment",
    "get_setting",
    "get_settings",
    "get_table_metadata",
    "get_timeline",
    "get_user",
    "invalidate_cache",
    "list_api_keys",
    "list_bookmarks",
    "list_databases",
    "list_documents",
    "list_native_query_snippets",
    "list_permission_groups",
    "list_pulses",
    "list_revisions",
    "list_segments",
    "list_timelines",
    "list_users",
    "metabase_api_request",
    "operation_to_dict",
    "remove_dashboard_card",
    "rescan_database_values",
    "restore_snapshot",
    "revert_revision",
    "run_card_query",
    "run_query",
    "search",
    "snapshot_entity",
    "sync_database_schema",
    "update_api_key",
    "update_bookmark_ordering",
    "update_cache_config",
    "update_card",
    "update_collection",
    "update_dashboard",
    "update_dashboard_cards",
    "update_dashboard_parameters",
    "update_database",
    "update_document",
    "update_native_query_snippet",
    "update_permissions_graph",
    "update_pulse",
    "update_segment",
    "update_setting",
    "update_timeline",
    "update_timeline_event",
    "update_user",
    "validate_api_request",
]
