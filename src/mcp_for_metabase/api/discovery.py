# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from mcp_for_metabase.registry import ApiRegistry
from mcp_for_metabase.safety import SafetyTier


def operation_to_dict(operation: Any) -> dict[str, Any]:
    return {
        "operation_id": operation.operation_id,
        "source_operation_id": operation.source_operation_id,
        "method": operation.method,
        "path": operation.path,
        "safety_tier": operation.safety_tier.value,
        "summary": operation.summary,
        "description": operation.description,
        "tags": list(operation.tags),
        "parameters": list(operation.parameters),
        "required_path_parameters": list(operation.required_path_parameters),
        "required_query_parameters": list(operation.required_query_parameters),
        "required_body_fields": list(operation.required_body_fields),
        "request_body_required": operation.request_body_required,
        "deprecated": operation.deprecated,
    }


async def discover_operations(
    *,
    text: str | None = None,
    method: str | None = None,
    safety_tier: str | None = None,
    tag: str | None = None,
    limit: int = 50,
    registry: ApiRegistry | None = None,
) -> dict[str, Any]:
    registry = registry or ApiRegistry.load_default()
    tier = SafetyTier(safety_tier) if safety_tier else None
    operations = registry.search(
        text=text,
        method=method,
        safety_tier=tier,
        tag=tag,
        limit=limit,
    )
    return {
        "operation_count": len(registry.operations),
        "returned_count": len(operations),
        "filters": {
            "text": text,
            "method": method,
            "safety_tier": safety_tier,
            "tag": tag,
            "limit": limit,
        },
        "operations": [operation_to_dict(operation) for operation in operations],
    }


async def get_operation(
    *,
    operation_id: str,
    registry: ApiRegistry | None = None,
) -> dict[str, Any]:
    operation = (registry or ApiRegistry.load_default()).get(operation_id)
    return operation_to_dict(operation)
