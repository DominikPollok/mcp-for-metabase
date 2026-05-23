# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.application.common import omit_none
from mcp_for_metabase.client import MetabaseClient


async def update_permissions_graph(
    client: MetabaseClient,
    *,
    graph: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/permissions/graph",
        operation_id="put_api_permissions_graph",
        body=graph,
        dry_run=dry_run,
        confirm=confirm,
    )


async def get_permissions_graph(client: MetabaseClient) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/permissions/graph",
        operation_id="get_api_permissions_graph",
    )


async def list_permission_groups(client: MetabaseClient) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/permissions/group",
        operation_id="get_api_permissions_group",
    )


async def get_permission_group(client: MetabaseClient, *, group_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/permissions/group/{id}",
        operation_id="get_api_permissions_group_id",
        path_params={"id": group_id},
    )


async def list_users(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/user", operation_id="get_api_user")


async def get_user(client: MetabaseClient, *, user_id: int) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/user/{id}",
        operation_id="get_api_user_id",
        path_params={"id": user_id},
    )


async def create_user(
    client: MetabaseClient,
    *,
    email: str,
    first_name: str,
    last_name: str,
    password: str | None = None,
    user_group_memberships: list[dict[str, Any]] | None = None,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    body = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "user_group_memberships": user_group_memberships,
    }
    return await client.request(
        "POST",
        "/api/user",
        operation_id="post_api_user",
        body=omit_none(body),
        dry_run=dry_run,
        confirm=confirm,
    )


async def update_user(
    client: MetabaseClient,
    *,
    user_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/user/{id}",
        operation_id="put_api_user_id",
        path_params={"id": user_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def list_api_keys(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/api-key", operation_id="get_api_api_key")


async def get_settings(client: MetabaseClient) -> dict[str, Any]:
    return await client.request("GET", "/api/setting", operation_id="get_api_setting")


async def get_setting(client: MetabaseClient, *, key: str) -> dict[str, Any]:
    return await client.request(
        "GET",
        "/api/setting/{key}",
        operation_id="get_api_setting_key",
        path_params={"key": key},
    )


async def update_setting(
    client: MetabaseClient,
    *,
    key: str,
    value: Any,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/setting/{key}",
        operation_id="put_api_setting_key",
        path_params={"key": key},
        body={"value": value},
        dry_run=dry_run,
        confirm=confirm,
    )


async def update_database(
    client: MetabaseClient,
    *,
    database_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/database/{id}",
        operation_id="put_api_database_id",
        path_params={"id": database_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def sync_database_schema(
    client: MetabaseClient,
    *,
    database_id: int,
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/database/{id}/sync_schema",
        operation_id="post_api_database_id_sync_schema",
        path_params={"id": database_id},
        dry_run=dry_run,
    )


async def rescan_database_values(
    client: MetabaseClient,
    *,
    database_id: int,
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/database/{id}/rescan_values",
        operation_id="post_api_database_id_rescan_values",
        path_params={"id": database_id},
        dry_run=dry_run,
    )


async def create_api_key(
    client: MetabaseClient,
    *,
    name: str,
    group_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/api-key",
        operation_id="post_api_api_key",
        body={"name": name, "group_id": group_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def update_api_key(
    client: MetabaseClient,
    *,
    api_key_id: int,
    updates: dict[str, Any],
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "PUT",
        "/api/api-key/{id}",
        operation_id="put_api_api_key_id",
        path_params={"id": api_key_id},
        body=updates,
        dry_run=dry_run,
        confirm=confirm,
    )


async def delete_api_key(
    client: MetabaseClient,
    *,
    api_key_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/api-key/{id}",
        operation_id="delete_api_api_key_id",
        path_params={"id": api_key_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def create_card_public_link(
    client: MetabaseClient,
    *,
    card_id: int,
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/card/{card-id}/public_link",
        operation_id="post_api_card_card_id_public_link",
        path_params={"card_id": card_id},
        dry_run=dry_run,
    )


async def delete_card_public_link(
    client: MetabaseClient,
    *,
    card_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/card/{card-id}/public_link",
        operation_id="delete_api_card_card_id_public_link",
        path_params={"card_id": card_id},
        dry_run=dry_run,
        confirm=confirm,
    )


async def create_dashboard_public_link(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    dry_run: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "POST",
        "/api/dashboard/{dashboard-id}/public_link",
        operation_id="post_api_dashboard_dashboard_id_public_link",
        path_params={"dashboard_id": dashboard_id},
        dry_run=dry_run,
    )


async def delete_dashboard_public_link(
    client: MetabaseClient,
    *,
    dashboard_id: int,
    dry_run: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    return await client.request(
        "DELETE",
        "/api/dashboard/{dashboard-id}/public_link",
        operation_id="delete_api_dashboard_dashboard_id_public_link",
        path_params={"dashboard_id": dashboard_id},
        dry_run=dry_run,
        confirm=confirm,
    )
