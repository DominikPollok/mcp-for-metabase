# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.api.validation import validate_api_request
from mcp_for_metabase.client import MetabaseClient
from mcp_for_metabase.errors import RegistryError
from mcp_for_metabase.registry import ApiRegistry


async def metabase_api_request(
    client: MetabaseClient,
    *,
    operation_id: str | None = None,
    path_params: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    body: Any | None = None,
    dry_run: bool = False,
    confirm: bool = False,
    registry: ApiRegistry | None = None,
) -> dict[str, Any]:
    if not operation_id:
        raise RegistryError(
            "operation_id is required; call metabase_discover_operations "
            "to find available operations",
            response_body={
                "hint": (
                    "Call metabase_discover_operations with text or method filters, "
                    "then pass its operation_id."
                ),
            },
        )
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
