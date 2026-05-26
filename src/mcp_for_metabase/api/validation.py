# SPDX-License-Identifier: GPL-3.0-or-later
from copy import deepcopy
from typing import Any

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validator_for

from mcp_for_metabase.errors import RegistryError
from mcp_for_metabase.registry import OpenApiSpec


def _compatible_request_schema(operation_id: str, schema: dict[str, Any]) -> dict[str, Any]:
    """Allow dashboard card payload shapes accepted by Metabase but absent from OpenAPI."""
    field = {
        "put_api_dashboard_id": "dashcards",
        "put_api_dashboard_id_cards": "cards",
    }.get(operation_id)
    if field is None:
        return schema
    compatible = deepcopy(schema)
    properties = compatible.get("properties")
    if not isinstance(properties, dict) or field not in properties:
        return schema
    array_schema: dict[str, Any] = {"type": "array", "items": {"type": "object"}}
    properties[field] = (
        {"oneOf": [array_schema, {"type": "null"}]} if field == "dashcards" else array_schema
    )
    return compatible


def _has_param(params: dict[str, Any] | None, name: str) -> bool:
    if not params:
        return False
    return name in params or name.replace("-", "_") in params


def _get_param(params: dict[str, Any] | None, name: str) -> Any:
    if not params:
        return None
    if name in params:
        return params[name]
    return params.get(name.replace("-", "_"))


def _validate_schema(
    *,
    schema: dict[str, Any],
    value: Any,
    operation_id: str,
    location: str,
    name: str,
) -> None:
    validation_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "components": OpenApiSpec.load_default().spec.get("components", {}),
        "allOf": [schema],
    }
    validator_cls = validator_for(validation_schema)
    validator_cls.check_schema(validation_schema)
    validator = validator_cls(validation_schema)
    try:
        validator.validate(value)
    except ValidationError as exc:
        raise RegistryError(
            f"{location} parameter {name!r} does not match OpenAPI schema for {operation_id}",
            response_body={
                "operation_id": operation_id,
                "location": location,
                "parameter": name,
                "validation_error": exc.message,
                "json_path": list(exc.path),
                "schema_path": list(exc.schema_path),
            },
        ) from exc


def validate_api_request(
    *,
    operation: Any,
    path_params: dict[str, Any] | None,
    query: dict[str, Any] | None,
    body: Any | None,
) -> None:
    missing_path = [
        name for name in operation.required_path_parameters if not _has_param(path_params, name)
    ]
    missing_query = [
        name for name in operation.required_query_parameters if not _has_param(query, name)
    ]
    missing_body = []
    if operation.request_body_required and body is None:
        missing_body = list(operation.required_body_fields) or ["<body>"]
    elif operation.required_body_fields:
        if not isinstance(body, dict):
            missing_body = list(operation.required_body_fields)
        else:
            missing_body = [name for name in operation.required_body_fields if name not in body]

    if missing_path or missing_query or missing_body:
        raise RegistryError(
            f"Missing required parameters for {operation.operation_id}",
            response_body={
                "operation_id": operation.operation_id,
                "missing_path_parameters": missing_path,
                "missing_query_parameters": missing_query,
                "missing_body_fields": missing_body,
            },
        )

    spec_operation = OpenApiSpec.load_default().get_operation(operation)
    if spec_operation:
        for parameter in spec_operation.get("parameters", []):
            if not isinstance(parameter, dict):
                continue
            location = parameter.get("in")
            if location not in {"path", "query"}:
                continue
            name = parameter.get("name")
            schema = parameter.get("schema")
            if not isinstance(name, str) or not isinstance(schema, dict):
                continue
            params = path_params if location == "path" else query
            if not _has_param(params, name):
                continue
            _validate_schema(
                schema=schema,
                value=_get_param(params, name),
                operation_id=operation.operation_id,
                location=location,
                name=name,
            )

    schema = OpenApiSpec.load_default().get_request_body_schema(operation)
    if schema is None or body is None:
        return

    _validate_schema(
        schema=_compatible_request_schema(operation.operation_id, schema),
        value=body,
        operation_id=operation.operation_id,
        location="body",
        name="<body>",
    )
