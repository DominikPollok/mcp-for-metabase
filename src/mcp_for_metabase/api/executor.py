# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.api.validation import validate_api_request
from mcp_for_metabase.client import MetabaseClient
from mcp_for_metabase.registry import ApiRegistry


async def metabase_api_request(
    client: MetabaseClient,
    *,
    operation_id: str,
    path_params: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    body: Any | None = None,
    dry_run: bool = False,
    confirm: bool = False,
    registry: ApiRegistry | None = None,
) -> dict[str, Any]:
    operation = (registry or ApiRegistry.load_default()).get(operation_id)
    validate_api_request(
        operation=operation,
        path_params=path_params,
        query=query,
        body=body,
    )
    return await client.request(
        operation.method,
        operation.path,
        operation_id=operation.operation_id,
        path_params=path_params,
        query=query,
        body=body,
        dry_run=dry_run,
        confirm=confirm,
    )
