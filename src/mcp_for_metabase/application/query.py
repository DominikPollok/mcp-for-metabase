# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.client import MetabaseClient


async def connection_test(client: MetabaseClient) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/session/properties",
        operation_id="get_api_session_properties",
    )


async def search(
    client: MetabaseClient,
    *,
    query: str,
    models: list[str] | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {"q": query, "limit": limit}
    if models:
        params["models"] = ",".join(models)
    return await client.request("GET", "/api/search", operation_id="get_api_search", query=params)


async def list_databases(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/database", operation_id="get_api_database")


async def get_database_metadata(client: MetabaseClient, *, database_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/database/{id}/metadata",
        operation_id="get_api_database_id_metadata",
        path_params={"id": database_id},
    )


async def get_table_metadata(client: MetabaseClient, *, table_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/table/{id}/query_metadata",
        operation_id="get_api_table_id_query_metadata",
        path_params={"id": table_id},
    )


async def run_query(
    client: MetabaseClient,
    *,
    database_id: int,
    query: dict[str, Any],
    query_type: str = "query",
    dry_run: bool = False,
) -> dict[str, Any]:
    query_key = "native" if query_type == "native" else "query"
    body = {"database": database_id, "type": query_type, query_key: query}
    return await client.request(
        "POST",
        "/api/dataset",
        operation_id="post_api_dataset",
        body=body,
        dry_run=dry_run,
    )


async def get_card_series(client: MetabaseClient, *, card_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/card/{id}/series",
        operation_id="get_api_card_id_series",
        path_params={"id": card_id},
    )


async def run_card_query(
    client: MetabaseClient,
    *,
    card_id: int,
    parameters: list[dict[str, Any]] | None = None,
    ignore_cache: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/card/{card-id}/query",
        operation_id="post_api_card_card_id_query",
        path_params={"card_id": card_id},
        body={"parameters": parameters or [], "ignore_cache": ignore_cache},
        dry_run=dry_run,
    )


async def export_card_query(
    client: MetabaseClient,
    *,
    card_id: int,
    export_format: str,
    parameters: list[dict[str, Any]] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/card/{card-id}/query/{export-format}",
        operation_id="post_api_card_card_id_query_export_format",
        path_params={"card_id": card_id, "export_format": export_format},
        body={"parameters": parameters or []},
        dry_run=dry_run,
    )
