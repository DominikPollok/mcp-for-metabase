# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.application.common import omit_none, response_items
from mcp_for_metabase.application.query import search
from mcp_for_metabase.client import MetabaseClient


async def collection_tree(client: MetabaseClient) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/collection/tree",
        operation_id="get_api_collection_tree",
    )


async def create_collection(
    client: MetabaseClient,
    *,
    name: str,
    description: str | None = None,
    parent_id: int | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = {"name": name, "description": description, "parent_id": parent_id}
    return await client.request(
        "POST",
        "/api/collection",
        operation_id="post_api_collection",
        body=omit_none(body),
        dry_run=dry_run,
    )


async def update_collection(
    client: MetabaseClient,
    *,
    collection_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/collection/{id}",
        operation_id="put_api_collection_id",
        path_params={"id": collection_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def archive_collection(
    client: MetabaseClient,
    *,
    collection_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await update_collection(
        client,
        collection_id=collection_id,
        updates={"archived": True},
        dry_run=dry_run,
        confirm=confirm,
    )


async def create_or_update_collection(
    client: MetabaseClient,
    *,
    name: str,
    description: str | None = None,
    parent_id: int | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    existing = await search(client, query=name, models=["collection"], limit=10)
    items = response_items(existing)
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get("name") == name and item.get("id"):
                return await update_collection(
                    client,
                    collection_id=int(item["id"]),
                    updates=omit_none(
                        {
                            "name": name,
                            "description": description,
                            "parent_id": parent_id,
                        }
                    ),
                    dry_run=dry_run,
                )
    return await create_collection(
        client,
        name=name,
        description=description,
        parent_id=parent_id,
        dry_run=dry_run,
    )


async def create_card(
    client: MetabaseClient,
    *,
    name: str,
    dataset_query: dict[str, Any],
    display: str = "table",
    collection_id: int | None = None,
    visualization_settings: dict[str, Any] | None = None,
    description: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = {
        "name": name,
        "dataset_query": dataset_query,
        "display": display,
        "collection_id": collection_id,
        "visualization_settings": visualization_settings or {},
        "description": description,
        "type": "question",
    }
    return await client.request(
        "POST",
        "/api/card",
        operation_id="post_api_card",
        body=omit_none(body),
        dry_run=dry_run,
    )


async def create_or_update_card(
    client: MetabaseClient,
    *,
    name: str,
    dataset_query: dict[str, Any],
    display: str = "table",
    collection_id: int | None = None,
    visualization_settings: dict[str, Any] | None = None,
    description: str | None = None,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    existing = await search(client, query=name, models=["card"], limit=10)
    items = response_items(existing)
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get("name") == name and item.get("id"):
                return await update_card(
                    client,
                    card_id=int(item["id"]),
                    updates=omit_none(
                        {
                            "name": name,
                            "dataset_query": dataset_query,
                            "display": display,
                            "collection_id": collection_id,
                            "visualization_settings": visualization_settings or {},
                            "description": description,
                            "type": "question",
                        }
                    ),
                    dry_run=dry_run,
                    confirm=confirm,
                )
    return await create_card(
        client,
        name=name,
        dataset_query=dataset_query,
        display=display,
        collection_id=collection_id,
        visualization_settings=visualization_settings,
        description=description,
        dry_run=dry_run,
    )


async def get_card(client: MetabaseClient, *, card_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/card/{id}",
        operation_id="get_api_card_id",
        path_params={"id": card_id},
    )


async def update_card(
    client: MetabaseClient,
    *,
    card_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/card/{id}",
        operation_id="put_api_card_id",
        path_params={"id": card_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def archive_card(
    client: MetabaseClient,
    *,
    card_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await update_card(
        client,
        card_id=card_id,
        updates={"archived": True},
        dry_run=dry_run,
        confirm=confirm,
    )


async def delete_card(
    client: MetabaseClient,
    *,
    card_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/card/{id}",
        operation_id="delete_api_card_id",
        path_params={"id": card_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def create_dashboard(
    client: MetabaseClient,
    *,
    name: str,
    description: str | None = None,
    collection_id: int | None = None,
    parameters: list[dict[str, Any]] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = {
        "name": name,
        "description": description,
        "collection_id": collection_id,
        "parameters": parameters or [],
    }
    return await client.request(
        "POST",
        "/api/dashboard",
        operation_id="post_api_dashboard",
        body=omit_none(body),
        dry_run=dry_run,
    )


async def create_or_update_dashboard(
    client: MetabaseClient,
    *,
    name: str,
    description: str | None = None,
    collection_id: int | None = None,
    parameters: list[dict[str, Any]] | None = None,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    existing = await search(client, query=name, models=["dashboard"], limit=10)
    items = response_items(existing)
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get("name") == name and item.get("id"):
                return await update_dashboard(
                    client,
                    dashboard_id=int(item["id"]),
                    updates=omit_none(
                        {
                            "name": name,
                            "description": description,
                            "collection_id": collection_id,
                            "parameters": parameters or [],
                        }
                    ),
                    dry_run=dry_run,
                    confirm=confirm,
                )
    return await create_dashboard(
        client,
        name=name,
        description=description,
        collection_id=collection_id,
        parameters=parameters,
        dry_run=dry_run,
    )


async def get_dashboard(client: MetabaseClient, *, dashboard_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/dashboard/{id}",
        operation_id="get_api_dashboard_id",
        path_params={"id": dashboard_id},
    )


async def update_dashboard(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/dashboard/{id}",
        operation_id="put_api_dashboard_id",
        path_params={"id": dashboard_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def update_dashboard_parameters(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    parameters: list[dict[str, Any]],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await update_dashboard(
        client,
        dashboard_id=dashboard_id,
        updates={"parameters": parameters},
        dry_run=dry_run,
        confirm=confirm,
    )


async def get_dashboard_items(client: MetabaseClient, *, dashboard_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/dashboard/{id}/items",
        operation_id="get_api_dashboard_id_items",
        path_params={"id": dashboard_id},
    )


async def archive_dashboard(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await update_dashboard(
        client,
        dashboard_id=dashboard_id,
        updates={"archived": True},
        dry_run=dry_run,
        confirm=confirm,
    )


async def delete_dashboard(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/dashboard/{id}",
        operation_id="delete_api_dashboard_id",
        path_params={"id": dashboard_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def add_dashboard_card(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    card_id: int,
    row: int,
    col: int,
    size_x: int,
    size_y: int,
    parameter_mappings: list[dict[str, Any]] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    new_card = {
        "id": -1,
        "card_id": card_id,
        "row": row,
        "col": col,
        "size_x": size_x,
        "size_y": size_y,
        "parameter_mappings": parameter_mappings or [],
        "series": [],
    }
    cards = [new_card]
    if not dry_run:
        dashboard = await get_dashboard(client, dashboard_id=dashboard_id)
        existing_cards = dashboard.get("data", {}).get("dashcards", [])
        if isinstance(existing_cards, list):
            cards = []
            for card in existing_cards:
                if not isinstance(card, dict):
                    continue
                cards.append(
                    {
                        key: card[key]
                        for key in (
                            "id",
                            "card_id",
                            "row",
                            "col",
                            "size_x",
                            "size_y",
                            "parameter_mappings",
                            "series",
                            "inline_parameters",
                        )
                        if key in card
                    },
                )
            cards.append(new_card)
    return await client.request(
        "PUT",
        "/api/dashboard/{id}/cards",
        operation_id="put_api_dashboard_id_cards",
        path_params={"id": dashboard_id},
        body={"cards": cards},
        dry_run=dry_run,
    )


async def update_dashboard_cards(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    cards: list[dict[str, Any]],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/dashboard/{id}/cards",
        operation_id="put_api_dashboard_id_cards",
        path_params={"id": dashboard_id},
        body={"cards": cards},
        dry_run=dry_run,
        confirm=confirm,
    )


async def remove_dashboard_card(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    dashcard_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/dashboard/{id}/cards/{dashcard_id}",
        operation_id="delete_api_dashboard_id_cards_dashcard_id",
        path_params={"id": dashboard_id, "dashcard_id": dashcard_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def copy_dashboard(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    name: str | None = None,
    collection_id: int | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = omit_none({"name": name, "collection_id": collection_id})
    return await client.request(
        "POST",
        "/api/dashboard/{from-dashboard-id}/copy",
        operation_id="post_api_dashboard_from_dashboard_id_copy",
        path_params={"from_dashboard_id": dashboard_id},
        body=body,
        dry_run=dry_run,
    )


async def copy_card(
    client: MetabaseClient,
    *,
    card_id: int,
    name: str | None = None,
    collection_id: int | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = omit_none({"name": name, "collection_id": collection_id})
    return await client.request(
        "POST",
        "/api/card/{id}/copy",
        operation_id="post_api_card_id_copy",
        path_params={"id": card_id},
        body=body,
        dry_run=dry_run,
    )
