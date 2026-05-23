# SPDX-License-Identifier: GPL-3.0-or-later
import os
from uuid import uuid4

import pytest

from mcp_for_metabase.client import MetabaseClient
from mcp_for_metabase.config import Settings, WriteMode
from mcp_for_metabase.tools import (
    add_dashboard_card,
    archive_card,
    archive_collection,
    archive_dashboard,
    create_card,
    create_collection,
    create_dashboard,
    get_dashboard,
    list_databases,
    snapshot_entity,
)

pytestmark = pytest.mark.integration


def live_settings() -> Settings:
    api_key = os.environ.get("METABASE_API_KEY")
    url = os.environ.get("METABASE_URL")
    if not api_key or not url:
        pytest.skip("METABASE_URL and METABASE_API_KEY are required for integration tests")
    return Settings(
        METABASE_URL=url,
        METABASE_API_KEY=api_key,
        METABASE_MCP_WRITE_MODE=WriteMode.SAFE_WRITES,
    )


@pytest.mark.asyncio
async def test_live_dashboard_lifecycle() -> None:
    settings = live_settings()
    suffix = uuid4().hex[:8]
    async with MetabaseClient(settings) as client:
        databases = await list_databases(client)
        database_items = databases.get("data", {}).get("data", databases.get("data", []))
        assert isinstance(database_items, list)
        assert database_items, "Metabase instance has no visible databases"
        database_id = database_items[0]["id"]

        collection = await create_collection(
            client,
            name=f"MCP integration {suffix}",
            description="Created by mcp-for-metabase integration tests",
        )
        collection_id = collection["data"]["id"]

        dataset_query = {
            "database": database_id,
            "type": "native",
            "native": {"query": "select 1 as value"},
        }
        card = await create_card(
            client,
            name=f"MCP integration card {suffix}",
            dataset_query=dataset_query,
            display="scalar",
            collection_id=collection_id,
        )
        card_id = card["data"]["id"]

        dashboard = await create_dashboard(
            client,
            name=f"MCP integration dashboard {suffix}",
            collection_id=collection_id,
        )
        dashboard_id = dashboard["data"]["id"]

        snapshot = await snapshot_entity(client, entity_type="dashboard", entity_id=dashboard_id)
        assert snapshot["snapshot"]["id"] == dashboard_id

        await add_dashboard_card(
            client,
            dashboard_id=dashboard_id,
            card_id=card_id,
            row=0,
            col=0,
            size_x=6,
            size_y=4,
        )
        fetched = await get_dashboard(client, dashboard_id=dashboard_id)
        assert fetched["data"]["id"] == dashboard_id

        await archive_card(client, card_id=card_id)
        await archive_dashboard(client, dashboard_id=dashboard_id)
        await archive_collection(client, collection_id=collection_id)
