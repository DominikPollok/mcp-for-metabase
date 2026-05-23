# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.application.common import omit_none, response_items
from mcp_for_metabase.client import MetabaseClient


async def create_native_query_snippet(
    client: MetabaseClient,
    *,
    name: str,
    content: str,
    description: str | None = None,
    collection_id: int | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    body = {
        "name": name,
        "content": content,
        "description": description,
        "collection_id": collection_id,
    }
    return await client.request(
        "POST",
        "/api/native-query-snippet",
        operation_id="post_api_native_query_snippet",
        body=omit_none(body),
        dry_run=dry_run,
    )


async def list_native_query_snippets(client: MetabaseClient) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/native-query-snippet",
        operation_id="get_api_native_query_snippet",
    )


async def get_native_query_snippet(client: MetabaseClient, *, snippet_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/native-query-snippet/{id}",
        operation_id="get_api_native_query_snippet_id",
        path_params={"id": snippet_id},
    )


async def update_native_query_snippet(
    client: MetabaseClient,
    *,
    snippet_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/native-query-snippet/{id}",
        operation_id="put_api_native_query_snippet_id",
        path_params={"id": snippet_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def create_or_update_native_query_snippet(
    client: MetabaseClient,
    *,
    name: str,
    content: str,
    description: str | None = None,
    collection_id: int | None = None,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    existing = await list_native_query_snippets(client)
    items = response_items(existing)
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get("name") == name and item.get("id"):
                return await update_native_query_snippet(
                    client,
                    snippet_id=int(item["id"]),
                    updates=omit_none(
                        {
                            "name": name,
                            "content": content,
                            "description": description,
                            "collection_id": collection_id,
                        }
                    ),
                    dry_run=dry_run,
                    confirm=confirm,
                )
    return await create_native_query_snippet(
        client,
        name=name,
        content=content,
        description=description,
        collection_id=collection_id,
        dry_run=dry_run,
    )
