# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.application.admin import get_permissions_graph, update_permissions_graph
from mcp_for_metabase.application.content import (
    get_card,
    get_dashboard,
    update_card,
    update_collection,
    update_dashboard,
)
from mcp_for_metabase.client import MetabaseClient
from mcp_for_metabase.errors import RegistryError


async def snapshot_entity(
    client: MetabaseClient,
    *,
    entity_type: str,
    entity_id: int | None = None,
) -> dict[str, Any]:
    if entity_type == "dashboard":
        if entity_id is None:
            raise RegistryError("dashboard snapshot requires entity_id")
        snapshot = await get_dashboard(client, dashboard_id=entity_id)
    elif entity_type == "card":
        if entity_id is None:
            raise RegistryError("card snapshot requires entity_id")
        snapshot = await get_card(client, card_id=entity_id)
    elif entity_type == "collection":
        if entity_id is None:
            raise RegistryError("collection snapshot requires entity_id")
        snapshot = await client.request(
            "GET",
            "/api/collection/{id}",
            operation_id="get_api_collection_id",
            path_params={"id": entity_id},
        )
    elif entity_type == "permissions_graph":
        snapshot = await get_permissions_graph(client)
    else:
        raise RegistryError(
            f"Unsupported snapshot entity_type: {entity_type}",
            response_body={
                "supported_entity_types": [
                    "dashboard",
                    "card",
                    "collection",
                    "permissions_graph",
                ],
            },
        )

    return {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "snapshot": snapshot.get("data"),
        "source_request_id": snapshot.get("request_id"),
    }


async def restore_snapshot(
    client: MetabaseClient,
    *,
    snapshot: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    entity_type = snapshot.get("entity_type")
    entity_id = snapshot.get("entity_id")
    data = snapshot.get("snapshot")
    if not isinstance(data, dict):
        raise RegistryError("snapshot must contain an object-valued 'snapshot' field")

    if entity_type == "dashboard":
        if entity_id is None:
            raise RegistryError("dashboard restore requires entity_id")
        return await update_dashboard(
            client,
            dashboard_id=int(entity_id),
            updates=data,
            dry_run=dry_run,
            confirm=confirm,
        )
    if entity_type == "card":
        if entity_id is None:
            raise RegistryError("card restore requires entity_id")
        return await update_card(
            client,
            card_id=int(entity_id),
            updates=data,
            dry_run=dry_run,
            confirm=confirm,
        )
    if entity_type == "collection":
        if entity_id is None:
            raise RegistryError("collection restore requires entity_id")
        return await update_collection(
            client,
            collection_id=int(entity_id),
            updates=data,
            dry_run=dry_run,
            confirm=confirm,
        )
    if entity_type == "permissions_graph":
        return await update_permissions_graph(
            client,
            graph=data,
            dry_run=dry_run,
            confirm=confirm,
        )
    raise RegistryError(f"Unsupported restore entity_type: {entity_type}")
