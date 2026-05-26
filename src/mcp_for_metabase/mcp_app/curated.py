# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_for_metabase import tools
from mcp_for_metabase.mcp_app.context import McpAppContext


def register_curated_tools(mcp: FastMCP, context: McpAppContext) -> None:
    with_client = context.with_client
    snapshot_store = context.snapshot_store

    @mcp.tool()
    async def metabase_connection_test() -> dict[str, Any]:
        """Verify connectivity/authentication and return compact identity/version data."""
        return await with_client(lambda client: tools.connection_test(client))

    @mcp.tool()
    async def metabase_search(
        query: str, models: list[str] | None = None, limit: int = 20
    ) -> dict[str, Any]:
        """Search Metabase content visible to the current API key."""
        return await with_client(
            lambda client: tools.search(client, query=query, models=models, limit=limit)
        )

    @mcp.tool()
    async def metabase_list_databases() -> dict[str, Any]:
        return await with_client(lambda client: tools.list_databases(client))

    @mcp.tool()
    async def metabase_collection_tree() -> dict[str, Any]:
        """Return the visible Metabase collection hierarchy."""
        return await with_client(lambda client: tools.collection_tree(client))

    @mcp.tool()
    async def metabase_get_database_metadata(database_id: int) -> dict[str, Any]:
        return await with_client(
            lambda client: tools.get_database_metadata(client, database_id=database_id),
        )

    @mcp.tool()
    async def metabase_get_table_metadata(table_id: int) -> dict[str, Any]:
        """Inspect one table's query metadata, fields, and semantic metadata."""
        return await with_client(lambda client: tools.get_table_metadata(client, table_id=table_id))

    @mcp.tool()
    async def metabase_run_query(
        database_id: int,
        query: dict[str, Any],
        query_type: str = "query",
        dry_run: bool = False,
    ) -> dict[str, Any]:
        return await with_client(
            lambda client: tools.run_query(
                client,
                database_id=database_id,
                query=query,
                query_type=query_type,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_create_collection(
        name: str,
        description: str | None = None,
        parent_id: int | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        return await with_client(
            lambda client: tools.create_collection(
                client,
                name=name,
                description=description,
                parent_id=parent_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_create_or_update_collection(
        name: str,
        description: str | None = None,
        parent_id: int | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Create a collection or update an exact-name existing collection."""
        return await with_client(
            lambda client: tools.create_or_update_collection(
                client,
                name=name,
                description=description,
                parent_id=parent_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_snapshot_entity(
        entity_type: str,
        entity_id: int | None = None,
    ) -> dict[str, Any]:
        """Snapshot dashboard, card, collection, or permissions_graph before mutation."""
        snapshot = await with_client(
            lambda client: tools.snapshot_entity(
                client,
                entity_type=entity_type,
                entity_id=entity_id,
            ),
        )
        return snapshot_store().save(snapshot)

    @mcp.tool()
    async def metabase_list_saved_snapshots(limit: int = 50) -> dict[str, Any]:
        """List locally saved rollback snapshots."""
        snapshots = snapshot_store().list(limit=limit)
        return {"snapshot_count": len(snapshots), "snapshots": snapshots}

    @mcp.tool()
    async def metabase_restore_snapshot(
        snapshot: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Restore a snapshot produced by metabase_snapshot_entity."""
        return await with_client(
            lambda client: tools.restore_snapshot(
                client,
                snapshot=snapshot,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_restore_saved_snapshot(
        snapshot_id: str,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Restore a locally saved snapshot by ID."""
        snapshot = snapshot_store().load(snapshot_id)
        return await with_client(
            lambda client: tools.restore_snapshot(
                client,
                snapshot=snapshot,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_update_collection(
        collection_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a collection by ID."""
        return await with_client(
            lambda client: tools.update_collection(
                client,
                collection_id=collection_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_archive_collection(
        collection_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Move a collection to trash by setting archived=true."""
        return await with_client(
            lambda client: tools.archive_collection(
                client,
                collection_id=collection_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_create_card(
        name: str,
        dataset_query: dict[str, Any],
        display: str = "table",
        collection_id: int | None = None,
        visualization_settings: dict[str, Any] | None = None,
        description: str | None = None,
        parameters: list[dict[str, Any]] | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Create a card/question, optionally with card-level filter parameters."""
        return await with_client(
            lambda client: tools.create_card(
                client,
                name=name,
                dataset_query=dataset_query,
                display=display,
                collection_id=collection_id,
                visualization_settings=visualization_settings,
                description=description,
                parameters=parameters,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_create_or_update_card(
        name: str,
        dataset_query: dict[str, Any],
        display: str = "table",
        collection_id: int | None = None,
        visualization_settings: dict[str, Any] | None = None,
        description: str | None = None,
        parameters: list[dict[str, Any]] | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Create or update a card/question, optionally with card-level filter parameters."""
        return await with_client(
            lambda client: tools.create_or_update_card(
                client,
                name=name,
                dataset_query=dataset_query,
                display=display,
                collection_id=collection_id,
                visualization_settings=visualization_settings,
                description=description,
                parameters=parameters,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_get_card(card_id: int) -> dict[str, Any]:
        """Get a Metabase card/question by ID."""
        return await with_client(lambda client: tools.get_card(client, card_id=card_id))

    @mcp.tool()
    async def metabase_update_card(
        card_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a card/question by ID, including card-level filter parameters."""
        return await with_client(
            lambda client: tools.update_card(
                client,
                card_id=card_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_archive_card(
        card_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Move a card/question to trash by setting archived=true."""
        return await with_client(
            lambda client: tools.archive_card(
                client,
                card_id=card_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_delete_card(
        card_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a card/question through a destructive, confirmation-gated API call."""
        return await with_client(
            lambda client: tools.delete_card(
                client,
                card_id=card_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_create_dashboard(
        name: str,
        description: str | None = None,
        collection_id: int | None = None,
        parameters: list[dict[str, Any]] | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        return await with_client(
            lambda client: tools.create_dashboard(
                client,
                name=name,
                description=description,
                collection_id=collection_id,
                parameters=parameters,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_create_or_update_dashboard(
        name: str,
        description: str | None = None,
        collection_id: int | None = None,
        parameters: list[dict[str, Any]] | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Create a dashboard or update an exact-name existing dashboard."""
        return await with_client(
            lambda client: tools.create_or_update_dashboard(
                client,
                name=name,
                description=description,
                collection_id=collection_id,
                parameters=parameters,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_get_dashboard(
        dashboard_id: int,
        include: list[str] | None = None,
        compact: bool = False,
    ) -> dict[str, Any]:
        """Get a dashboard, optionally selecting top-level fields and compacting dashcards."""
        return await with_client(
            lambda client: tools.get_dashboard(
                client,
                dashboard_id=dashboard_id,
                include=include,
                compact=compact,
            ),
        )

    @mcp.tool()
    async def metabase_update_dashboard(
        dashboard_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update dashboard metadata, tabs, parameters, or settings by ID."""
        return await with_client(
            lambda client: tools.update_dashboard(
                client,
                dashboard_id=dashboard_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_update_dashboard_parameters(
        dashboard_id: int,
        parameters: list[dict[str, Any]],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Replace dashboard filters/parameters."""
        return await with_client(
            lambda client: tools.update_dashboard_parameters(
                client,
                dashboard_id=dashboard_id,
                parameters=parameters,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_get_dashboard_items(dashboard_id: int) -> dict[str, Any]:
        """List dashboard items/cards and layout details."""
        return await with_client(
            lambda client: tools.get_dashboard_items(client, dashboard_id=dashboard_id),
        )

    @mcp.tool()
    async def metabase_archive_dashboard(
        dashboard_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Move a dashboard to trash by setting archived=true."""
        return await with_client(
            lambda client: tools.archive_dashboard(
                client,
                dashboard_id=dashboard_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_delete_dashboard(
        dashboard_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a dashboard through a destructive, confirmation-gated API call."""
        return await with_client(
            lambda client: tools.delete_dashboard(
                client,
                dashboard_id=dashboard_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_add_dashboard_card(
        dashboard_id: int,
        card_id: int,
        row: int,
        col: int,
        size_x: int,
        size_y: int,
        dashboard_tab_id: int | None = None,
        parameter_mappings: list[dict[str, Any]] | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        return await with_client(
            lambda client: tools.add_dashboard_card(
                client,
                dashboard_id=dashboard_id,
                card_id=card_id,
                row=row,
                col=col,
                size_x=size_x,
                size_y=size_y,
                dashboard_tab_id=dashboard_tab_id,
                parameter_mappings=parameter_mappings,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_update_dashboard_cards(
        dashboard_id: int,
        cards: list[dict[str, Any]],
        tabs: list[dict[str, Any]] | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Replace/update the dashboard card layout using PUT /api/dashboard/{id}/cards."""
        return await with_client(
            lambda client: tools.update_dashboard_cards(
                client,
                dashboard_id=dashboard_id,
                cards=cards,
                tabs=tabs,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_remove_dashboard_card(
        dashboard_id: int,
        dashcard_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Remove a dashcard from a dashboard; destructive and confirmation-gated."""
        return await with_client(
            lambda client: tools.remove_dashboard_card(
                client,
                dashboard_id=dashboard_id,
                dashcard_id=dashcard_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_create_native_query_snippet(
        name: str,
        content: str,
        description: str | None = None,
        collection_id: int | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Create a reusable native SQL query snippet."""
        return await with_client(
            lambda client: tools.create_native_query_snippet(
                client,
                name=name,
                content=content,
                description=description,
                collection_id=collection_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_list_native_query_snippets() -> dict[str, Any]:
        """List reusable native SQL query snippets."""
        return await with_client(lambda client: tools.list_native_query_snippets(client))

    @mcp.tool()
    async def metabase_get_native_query_snippet(snippet_id: int) -> dict[str, Any]:
        """Get one reusable native SQL query snippet."""
        return await with_client(
            lambda client: tools.get_native_query_snippet(
                client,
                snippet_id=snippet_id,
            ),
        )

    @mcp.tool()
    async def metabase_update_native_query_snippet(
        snippet_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a reusable native SQL query snippet."""
        return await with_client(
            lambda client: tools.update_native_query_snippet(
                client,
                snippet_id=snippet_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_create_or_update_native_query_snippet(
        name: str,
        content: str,
        description: str | None = None,
        collection_id: int | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Create a SQL snippet or update an exact-name existing snippet."""
        return await with_client(
            lambda client: tools.create_or_update_native_query_snippet(
                client,
                name=name,
                content=content,
                description=description,
                collection_id=collection_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_update_permissions_graph(
        graph: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update the Metabase permissions graph; requires all-writes and confirm=true."""
        return await with_client(
            lambda client: tools.update_permissions_graph(
                client,
                graph=graph,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_get_permissions_graph() -> dict[str, Any]:
        """Read the full Metabase permissions graph."""
        return await with_client(lambda client: tools.get_permissions_graph(client))

    @mcp.tool()
    async def metabase_list_permission_groups() -> dict[str, Any]:
        """List Metabase permission groups."""
        return await with_client(lambda client: tools.list_permission_groups(client))

    @mcp.tool()
    async def metabase_get_permission_group(group_id: int) -> dict[str, Any]:
        """Get one Metabase permission group."""
        return await with_client(
            lambda client: tools.get_permission_group(client, group_id=group_id),
        )

    @mcp.tool()
    async def metabase_list_users() -> dict[str, Any]:
        """List Metabase users visible to the current API key."""
        return await with_client(lambda client: tools.list_users(client))

    @mcp.tool()
    async def metabase_get_user(user_id: int) -> dict[str, Any]:
        """Get one Metabase user."""
        return await with_client(lambda client: tools.get_user(client, user_id=user_id))

    @mcp.tool()
    async def metabase_create_user(
        email: str,
        first_name: str,
        last_name: str,
        password: str | None = None,
        user_group_memberships: list[dict[str, Any]] | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Create a Metabase user; admin-gated."""
        return await with_client(
            lambda client: tools.create_user(
                client,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                user_group_memberships=user_group_memberships,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_update_user(
        user_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a Metabase user; admin-gated."""
        return await with_client(
            lambda client: tools.update_user(
                client,
                user_id=user_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_list_api_keys() -> dict[str, Any]:
        """List Metabase API keys."""
        return await with_client(lambda client: tools.list_api_keys(client))

    @mcp.tool()
    async def metabase_get_settings() -> dict[str, Any]:
        """List Metabase instance settings visible to the API key."""
        return await with_client(lambda client: tools.get_settings(client))

    @mcp.tool()
    async def metabase_get_setting(key: str) -> dict[str, Any]:
        """Get one Metabase instance setting."""
        return await with_client(lambda client: tools.get_setting(client, key=key))

    @mcp.tool()
    async def metabase_update_setting(
        key: str,
        value: Any,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update one Metabase instance setting; admin-gated."""
        return await with_client(
            lambda client: tools.update_setting(
                client,
                key=key,
                value=value,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_update_database(
        database_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update Metabase database configuration."""
        return await with_client(
            lambda client: tools.update_database(
                client,
                database_id=database_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_sync_database_schema(
        database_id: int,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Trigger a Metabase database schema sync."""
        return await with_client(
            lambda client: tools.sync_database_schema(
                client,
                database_id=database_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_rescan_database_values(
        database_id: int,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Trigger Metabase field value rescanning for a database."""
        return await with_client(
            lambda client: tools.rescan_database_values(
                client,
                database_id=database_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_create_api_key(
        name: str,
        group_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Create a Metabase API key; admin/safety-gated by Metabase permissions."""
        return await with_client(
            lambda client: tools.create_api_key(
                client,
                name=name,
                group_id=group_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_update_api_key(
        api_key_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a Metabase API key."""
        return await with_client(
            lambda client: tools.update_api_key(
                client,
                api_key_id=api_key_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_delete_api_key(
        api_key_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a Metabase API key; destructive and confirmation-gated."""
        return await with_client(
            lambda client: tools.delete_api_key(
                client,
                api_key_id=api_key_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_create_card_public_link(
        card_id: int, dry_run: bool = False
    ) -> dict[str, Any]:
        """Create or return a public link for a card/question."""
        return await with_client(
            lambda client: tools.create_card_public_link(
                client,
                card_id=card_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_delete_card_public_link(
        card_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a card/question public link; destructive and confirmation-gated."""
        return await with_client(
            lambda client: tools.delete_card_public_link(
                client,
                card_id=card_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_create_dashboard_public_link(
        dashboard_id: int,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Create or return a public link for a dashboard."""
        return await with_client(
            lambda client: tools.create_dashboard_public_link(
                client,
                dashboard_id=dashboard_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_delete_dashboard_public_link(
        dashboard_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a dashboard public link; destructive and confirmation-gated."""
        return await with_client(
            lambda client: tools.delete_dashboard_public_link(
                client,
                dashboard_id=dashboard_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_copy_dashboard(
        dashboard_id: int,
        name: str | None = None,
        collection_id: int | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Copy a dashboard."""
        return await with_client(
            lambda client: tools.copy_dashboard(
                client,
                dashboard_id=dashboard_id,
                name=name,
                collection_id=collection_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_copy_card(
        card_id: int,
        name: str | None = None,
        collection_id: int | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Copy a card/question."""
        return await with_client(
            lambda client: tools.copy_card(
                client,
                card_id=card_id,
                name=name,
                collection_id=collection_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_run_card_query(
        card_id: int,
        parameters: list[dict[str, Any]] | None = None,
        ignore_cache: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Run a saved card/question query."""
        return await with_client(
            lambda client: tools.run_card_query(
                client,
                card_id=card_id,
                parameters=parameters,
                ignore_cache=ignore_cache,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_export_card_query(
        card_id: int,
        export_format: str,
        parameters: list[dict[str, Any]] | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Export a saved card/question query in a Metabase-supported format."""
        return await with_client(
            lambda client: tools.export_card_query(
                client,
                card_id=card_id,
                export_format=export_format,
                parameters=parameters,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_get_card_series(card_id: int) -> dict[str, Any]:
        """List series cards attached to a card/question."""
        return await with_client(lambda client: tools.get_card_series(client, card_id=card_id))

    @mcp.tool()
    async def metabase_list_pulses() -> dict[str, Any]:
        """List Metabase pulses/subscriptions."""
        return await with_client(lambda client: tools.list_pulses(client))

    @mcp.tool()
    async def metabase_get_pulse(pulse_id: int) -> dict[str, Any]:
        """Get one Metabase pulse/subscription."""
        return await with_client(lambda client: tools.get_pulse(client, pulse_id=pulse_id))

    @mcp.tool()
    async def metabase_create_pulse(
        name: str,
        cards: list[dict[str, Any]],
        channels: list[dict[str, Any]],
        skip_if_empty: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Create a pulse/subscription."""
        return await with_client(
            lambda client: tools.create_pulse(
                client,
                name=name,
                cards=cards,
                channels=channels,
                skip_if_empty=skip_if_empty,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_update_pulse(
        pulse_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a pulse/subscription."""
        return await with_client(
            lambda client: tools.update_pulse(
                client,
                pulse_id=pulse_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_delete_pulse_subscription(
        pulse_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a pulse subscription; destructive and confirmation-gated."""
        return await with_client(
            lambda client: tools.delete_pulse_subscription(
                client,
                pulse_id=pulse_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_list_bookmarks() -> dict[str, Any]:
        """List bookmarks visible to the current user."""
        return await with_client(lambda client: tools.list_bookmarks(client))

    @mcp.tool()
    async def metabase_create_bookmark(
        model: str,
        entity_id: int,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Bookmark a Metabase entity such as card, dashboard, collection, or model."""
        return await with_client(
            lambda client: tools.create_bookmark(
                client,
                model=model,
                entity_id=entity_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_delete_bookmark(
        model: str,
        entity_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Remove a bookmark; destructive-gated."""
        return await with_client(
            lambda client: tools.delete_bookmark(
                client,
                model=model,
                entity_id=entity_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_update_bookmark_ordering(
        ordering: list[dict[str, Any]],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Replace bookmark ordering."""
        return await with_client(
            lambda client: tools.update_bookmark_ordering(
                client,
                ordering=ordering,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_list_revisions(entity: str, entity_id: int) -> dict[str, Any]:
        """List revision history for a Metabase entity."""
        return await with_client(
            lambda client: tools.list_revisions(
                client,
                entity=entity,
                entity_id=entity_id,
            ),
        )

    @mcp.tool()
    async def metabase_revert_revision(
        entity: str,
        entity_id: int,
        revision_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Revert an entity to a previous revision."""
        return await with_client(
            lambda client: tools.revert_revision(
                client,
                entity=entity,
                entity_id=entity_id,
                revision_id=revision_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_list_timelines() -> dict[str, Any]:
        """List timelines."""
        return await with_client(lambda client: tools.list_timelines(client))

    @mcp.tool()
    async def metabase_get_timeline(timeline_id: int) -> dict[str, Any]:
        """Get a timeline."""
        return await with_client(
            lambda client: tools.get_timeline(client, timeline_id=timeline_id),
        )

    @mcp.tool()
    async def metabase_create_timeline(
        name: str,
        collection_id: int | None = None,
        default: bool | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Create a timeline."""
        return await with_client(
            lambda client: tools.create_timeline(
                client,
                name=name,
                collection_id=collection_id,
                default=default,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_update_timeline(
        timeline_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a timeline."""
        return await with_client(
            lambda client: tools.update_timeline(
                client,
                timeline_id=timeline_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_delete_timeline(
        timeline_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a timeline; destructive-gated."""
        return await with_client(
            lambda client: tools.delete_timeline(
                client,
                timeline_id=timeline_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_create_timeline_event(
        timeline_id: int,
        name: str,
        timestamp: str,
        description: str | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Create a timeline event."""
        return await with_client(
            lambda client: tools.create_timeline_event(
                client,
                timeline_id=timeline_id,
                name=name,
                timestamp=timestamp,
                description=description,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_update_timeline_event(
        event_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a timeline event."""
        return await with_client(
            lambda client: tools.update_timeline_event(
                client,
                event_id=event_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_delete_timeline_event(
        event_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a timeline event; destructive-gated."""
        return await with_client(
            lambda client: tools.delete_timeline_event(
                client,
                event_id=event_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_list_segments() -> dict[str, Any]:
        """List segments."""
        return await with_client(lambda client: tools.list_segments(client))

    @mcp.tool()
    async def metabase_get_segment(segment_id: int) -> dict[str, Any]:
        """Get a segment."""
        return await with_client(lambda client: tools.get_segment(client, segment_id=segment_id))

    @mcp.tool()
    async def metabase_create_segment(
        body: dict[str, Any], dry_run: bool = False
    ) -> dict[str, Any]:
        """Create a segment from a Metabase segment API body."""
        return await with_client(
            lambda client: tools.create_segment(client, body=body, dry_run=dry_run),
        )

    @mcp.tool()
    async def metabase_update_segment(
        segment_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a segment."""
        return await with_client(
            lambda client: tools.update_segment(
                client,
                segment_id=segment_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_delete_segment(
        segment_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a segment; destructive-gated."""
        return await with_client(
            lambda client: tools.delete_segment(
                client,
                segment_id=segment_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_list_documents() -> dict[str, Any]:
        """List documents."""
        return await with_client(lambda client: tools.list_documents(client))

    @mcp.tool()
    async def metabase_get_document(document_id: int) -> dict[str, Any]:
        """Get a document."""
        return await with_client(
            lambda client: tools.get_document(client, document_id=document_id),
        )

    @mcp.tool()
    async def metabase_create_document(
        body: dict[str, Any],
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Create a document from a Metabase document API body."""
        return await with_client(
            lambda client: tools.create_document(client, body=body, dry_run=dry_run),
        )

    @mcp.tool()
    async def metabase_update_document(
        document_id: int,
        updates: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update a document."""
        return await with_client(
            lambda client: tools.update_document(
                client,
                document_id=document_id,
                updates=updates,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_delete_document(
        document_id: int,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Delete a document; destructive-gated."""
        return await with_client(
            lambda client: tools.delete_document(
                client,
                document_id=document_id,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_copy_document(
        document_id: int,
        name: str | None = None,
        collection_id: int | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Copy a document."""
        return await with_client(
            lambda client: tools.copy_document(
                client,
                document_id=document_id,
                name=name,
                collection_id=collection_id,
                dry_run=dry_run,
            ),
        )

    @mcp.tool()
    async def metabase_get_cache_config() -> dict[str, Any]:
        """Get Metabase cache configuration."""
        return await with_client(lambda client: tools.get_cache_config(client))

    @mcp.tool()
    async def metabase_update_cache_config(
        config: dict[str, Any],
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Update Metabase cache configuration."""
        return await with_client(
            lambda client: tools.update_cache_config(
                client,
                config=config,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_invalidate_cache(
        body: dict[str, Any] | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Invalidate cache entries."""
        return await with_client(
            lambda client: tools.invalidate_cache(
                client,
                body=body,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )

    @mcp.tool()
    async def metabase_clear_cache(
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Clear Metabase cache; destructive-gated."""
        return await with_client(
            lambda client: tools.clear_cache(
                client,
                dry_run=dry_run,
                confirm=confirm,
            ),
        )
