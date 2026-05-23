# SPDX-License-Identifier: GPL-3.0-or-later

from mcp.server.fastmcp import FastMCP

from mcp_for_metabase.mcp_app.context import McpAppContext


def register_prompts(mcp: FastMCP, _context: McpAppContext) -> None:
    @mcp.prompt()
    def build_dashboard(topic: str, database_id: int, collection_name: str) -> str:
        return (
            f"Build a Metabase dashboard about {topic!r} in database {database_id}. "
            f"Create or reuse collection {collection_name!r}, inspect metadata first, "
            "create reusable questions/cards, then assemble a dashboard with filters and "
            "a clear layout. Keep all dashboard cards in the same collection unless the "
            "user explicitly requests otherwise."
        )

    @mcp.prompt()
    def audit_dashboard(dashboard_id: int) -> str:
        return (
            f"Audit Metabase dashboard {dashboard_id}. Check broken cards, unclear titles, "
            "missing descriptions, filter mappings, collection placement, and permission risks."
        )

    @mcp.prompt()
    def improve_dashboard(dashboard_id: int, goal: str) -> str:
        return (
            f"Improve Metabase dashboard {dashboard_id} for this goal: {goal}. Inspect before "
            "writing, prefer dry-runs, and preserve existing working cards unless replacement "
            "is explicitly justified."
        )

    @mcp.prompt()
    def create_semantic_model(database_id: int, table_id: int) -> str:
        return (
            f"Create or improve a semantic model for table {table_id} in database {database_id}. "
            "Inspect field metadata, propose naming and visibility changes, and only apply "
            "writes after safety checks pass."
        )

    @mcp.prompt()
    def migrate_content(source_collection_id: int, target_collection_id: int) -> str:
        return (
            f"Migrate reusable Metabase content from collection {source_collection_id} to "
            f"{target_collection_id}. Inventory dependencies first, preserve permissions, "
            "and use dry-runs before updates."
        )
