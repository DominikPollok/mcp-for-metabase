# SPDX-License-Identifier: GPL-3.0-or-later
import json
from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
from typing import Any

from mcp_for_metabase.config import WriteMode
from mcp_for_metabase.errors import RegistryError
from mcp_for_metabase.safety import SafetyPolicy, SafetyTier


@dataclass(frozen=True, slots=True)
class ApiOperation:
    operation_id: str
    method: str
    path: str
    safety_tier: SafetyTier
    summary: str = ""
    source_operation_id: str | None = None
    description: str = ""
    tags: tuple[str, ...] = ()
    parameters: tuple[str, ...] = ()
    required_path_parameters: tuple[str, ...] = ()
    required_query_parameters: tuple[str, ...] = ()
    required_body_fields: tuple[str, ...] = ()
    request_body_required: bool = False
    deprecated: bool = False


class ApiRegistry:
    def __init__(self, operations: dict[str, ApiOperation]) -> None:
        self.operations = operations

    @classmethod
    def from_entries(cls, entries: list[dict[str, Any]]) -> "ApiRegistry":
        operations = {}
        for entry in entries:
            operation = ApiOperation(
                operation_id=entry["operation_id"],
                method=entry["method"].upper(),
                path=entry["path"],
                safety_tier=SafetyTier(entry["safety_tier"]),
                summary=entry.get("summary", ""),
                source_operation_id=entry.get("source_operation_id"),
                description=entry.get("description", ""),
                tags=tuple(entry.get("tags", ())),
                parameters=tuple(entry.get("parameters", ())),
                required_path_parameters=tuple(entry.get("required_path_parameters", ())),
                required_query_parameters=tuple(entry.get("required_query_parameters", ())),
                required_body_fields=tuple(entry.get("required_body_fields", ())),
                request_body_required=bool(entry.get("request_body_required", False)),
                deprecated=bool(entry.get("deprecated", False)),
            )
            operations[operation.operation_id] = operation
        return cls(operations)

    @classmethod
    def load_default(cls) -> "ApiRegistry":
        data_path = files("mcp_for_metabase").joinpath("api_registry.json")
        return cls.from_entries(json.loads(data_path.read_text(encoding="utf-8")))

    def get(self, operation_id: str) -> ApiOperation:
        try:
            return self.operations[operation_id]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown Metabase API operation_id: {operation_id}",
                response_body={"known_operation_count": len(self.operations)},
            ) from exc

    def search(
        self,
        *,
        text: str | None = None,
        method: str | None = None,
        safety_tier: SafetyTier | None = None,
        tag: str | None = None,
        limit: int = 50,
    ) -> list[ApiOperation]:
        method_filter = method.upper() if method else None
        text_filter = text.lower() if text else None
        tag_filter = tag.lower() if tag else None
        matches: list[ApiOperation] = []
        for operation in self.operations.values():
            haystack = " ".join(
                [
                    operation.operation_id,
                    operation.source_operation_id or "",
                    operation.method,
                    operation.path,
                    operation.summary,
                    operation.description,
                    " ".join(operation.tags),
                ],
            ).lower()
            if method_filter and operation.method != method_filter:
                continue
            if safety_tier and operation.safety_tier != safety_tier:
                continue
            if tag_filter and tag_filter not in {item.lower() for item in operation.tags}:
                continue
            if text_filter and text_filter not in haystack:
                continue
            matches.append(operation)
            if len(matches) >= limit:
                break
        return matches


class OpenApiSpec:
    def __init__(self, spec: dict[str, Any]) -> None:
        self.spec = spec

    @classmethod
    def load_default(cls) -> "OpenApiSpec":
        return _load_default_openapi_spec()

    def get_operation(self, operation: ApiOperation) -> dict[str, Any] | None:
        path_item = self.spec.get("paths", {}).get(operation.path)
        if not isinstance(path_item, dict):
            return None
        spec_operation = path_item.get(operation.method.lower())
        return spec_operation if isinstance(spec_operation, dict) else None

    def get_request_body_schema(self, operation: ApiOperation) -> dict[str, Any] | None:
        spec_operation = self.get_operation(operation)
        if spec_operation is None:
            return None
        request_body = spec_operation.get("requestBody")
        if not isinstance(request_body, dict):
            return None
        content = request_body.get("content")
        if not isinstance(content, dict):
            return None
        json_content = content.get("application/json")
        if not isinstance(json_content, dict):
            return None
        schema = json_content.get("schema")
        return schema if isinstance(schema, dict) else None


@lru_cache(maxsize=1)
def _load_default_openapi_spec() -> OpenApiSpec:
    data_path = files("mcp_for_metabase").joinpath("openapi.json")
    return OpenApiSpec(json.loads(data_path.read_text(encoding="utf-8")))


def operation_id_for(method: str, path: str) -> str:
    clean = path.strip("/").replace("{", "").replace("}", "")
    tokens = [method.lower(), *clean.split("/")]
    return normalize_operation_id("_".join(tokens))


def normalize_operation_id(operation_id: str) -> str:
    return (
        operation_id.replace("-", "_")
        .replace("/", "_")
        .replace("{", "")
        .replace("}", "")
        .replace(":", "")
    )


def entries_from_openapi(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    policy = SafetyPolicy(write_mode=WriteMode.ALL_WRITES)
    entries: list[dict[str, Any]] = []
    for path, path_item in sorted(openapi.get("paths", {}).items()):
        if not isinstance(path_item, dict):
            continue
        for method, operation in sorted(path_item.items()):
            if method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
                continue
            if not isinstance(operation, dict):
                continue
            source_operation_id = operation.get("operationId")
            operation_id = normalize_operation_id(
                source_operation_id or operation_id_for(method, path)
            )
            tier = policy.classify(method, path, operation_id)
            parameters = [
                parameter.get("name")
                for parameter in operation.get("parameters", [])
                if isinstance(parameter, dict) and parameter.get("name")
            ]
            required_path_parameters = [
                parameter.get("name")
                for parameter in operation.get("parameters", [])
                if (
                    isinstance(parameter, dict)
                    and parameter.get("name")
                    and parameter.get("in") == "path"
                    and parameter.get("required", False)
                )
            ]
            required_query_parameters = [
                parameter.get("name")
                for parameter in operation.get("parameters", [])
                if (
                    isinstance(parameter, dict)
                    and parameter.get("name")
                    and parameter.get("in") == "query"
                    and parameter.get("required", False)
                )
            ]
            request_body = operation.get("requestBody", {})
            request_body_schema: dict[str, Any] = {}
            if isinstance(request_body, dict):
                content = request_body.get("content", {})
                if isinstance(content, dict):
                    json_content = content.get("application/json", {})
                    if isinstance(json_content, dict):
                        schema = json_content.get("schema", {})
                        if isinstance(schema, dict):
                            request_body_schema = schema
            required_body_fields = request_body_schema.get("required", [])
            if not isinstance(required_body_fields, list):
                required_body_fields = []
            entries.append(
                {
                    "operation_id": operation_id,
                    "source_operation_id": source_operation_id,
                    "method": method.upper(),
                    "path": path,
                    "safety_tier": tier.value,
                    "summary": operation.get("summary", ""),
                    "description": operation.get("description", ""),
                    "tags": operation.get("tags", []),
                    "parameters": parameters,
                    "required_path_parameters": required_path_parameters,
                    "required_query_parameters": required_query_parameters,
                    "required_body_fields": required_body_fields,
                    "request_body_required": (
                        bool(request_body.get("required", False) or required_body_fields)
                        if isinstance(request_body, dict)
                        else False
                    ),
                    "deprecated": bool(operation.get("deprecated", False)),
                },
            )
    return entries
