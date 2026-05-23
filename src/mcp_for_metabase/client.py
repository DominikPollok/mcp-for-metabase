# SPDX-License-Identifier: GPL-3.0-or-later
from collections.abc import Mapping
from typing import Any
from uuid import uuid4

import httpx
import structlog
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from mcp_for_metabase.audit import AuditLogger
from mcp_for_metabase.config import Settings
from mcp_for_metabase.errors import MetabaseError
from mcp_for_metabase.safety import READ_METHODS, SafetyPolicy
from mcp_for_metabase.sql_guard import enforce_sql_guard

logger = structlog.get_logger(__name__)


class MetabaseClient:
    """Async Metabase REST client with auth, safety, retries, and audit logging."""

    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.settings = settings
        self.safety = SafetyPolicy(settings.write_mode)
        self.audit_logger = audit_logger or AuditLogger(settings.metabase_mcp_audit_log)
        self._session_id: str | None = None
        self._client = httpx.AsyncClient(
            base_url=settings.base_url,
            timeout=settings.metabase_mcp_timeout,
            transport=transport,
        )

    async def __aenter__(self) -> "MetabaseClient":
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def authenticate(self) -> None:
        if self.settings.metabase_api_key:
            return
        if not self.settings.metabase_username or not self.settings.metabase_password:
            return
        response = await self._client.post(
            "/api/session",
            json={
                "username": self.settings.metabase_username,
                "password": self.settings.metabase_password.get_secret_value(),
            },
        )
        self._raise_for_response(response)
        body = response.json()
        self._session_id = body.get("id")

    def _headers(self, request_id: str) -> dict[str, str]:
        headers = {"X-Metabase-MCP-Request-ID": request_id}
        if self.settings.metabase_api_key and self.settings.metabase_api_key.get_secret_value():
            headers["X-API-Key"] = self.settings.metabase_api_key.get_secret_value()
        elif self._session_id:
            headers["X-Metabase-Session"] = self._session_id
        return headers

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.TransportError)),
        wait=wait_exponential(multiplier=0.25, min=0.25, max=2),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def request(
        self,
        method: str,
        path: str,
        *,
        operation_id: str | None = None,
        path_params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
        body: Any | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> dict[str, Any]:
        method = method.upper()
        resolved_path = self._resolve_path(path, path_params or {})
        decision = self.safety.ensure_allowed(
            method,
            resolved_path,
            operation_id=operation_id,
            dry_run=dry_run,
            confirm=confirm,
        )
        planned = {
            "method": method,
            "path": resolved_path,
            "query": dict(query or {}),
            "body": body,
            "operation_id": operation_id,
            "safety_tier": decision.tier.value,
        }
        enforce_sql_guard(
            mode=self.settings.sql_guard_mode,
            operation_id=operation_id,
            path=resolved_path,
            body=body,
        )
        if dry_run:
            return {"dry_run": True, "request": planned}

        request_id = str(uuid4())
        await self.authenticate()
        logger.debug("metabase_request", request_id=request_id, **planned)
        response = await self._client.request(
            method,
            resolved_path,
            params=query,
            json=body,
            headers=self._headers(request_id),
        )
        result = self._response_payload(response)
        self._raise_for_response(response, result)
        if method not in READ_METHODS:
            self.audit_logger.record(
                {
                    "request_id": request_id,
                    "operation_id": operation_id,
                    "method": method,
                    "path": resolved_path,
                    "query": dict(query or {}),
                    "body": body,
                    "status_code": response.status_code,
                    "result": result,
                },
            )
        return {"status_code": response.status_code, "data": result, "request_id": request_id}

    async def paginate(
        self,
        path: str,
        *,
        query: Mapping[str, Any] | None = None,
        limit: int = 100,
    ) -> list[Any]:
        offset = 0
        results: list[Any] = []
        while True:
            page_query = {**dict(query or {}), "limit": limit, "offset": offset}
            response = await self.request("GET", path, query=page_query)
            data = response["data"]
            items = data.get("data") if isinstance(data, dict) else data
            if not isinstance(items, list) or not items:
                break
            results.extend(items)
            if len(items) < limit:
                break
            offset += limit
        return results

    @staticmethod
    def _resolve_path(path: str, path_params: Mapping[str, Any]) -> str:
        resolved = path
        for key, value in path_params.items():
            resolved = resolved.replace("{" + key + "}", str(value))
            resolved = resolved.replace("{" + key.replace("_", "-") + "}", str(value))
            resolved = resolved.replace(":" + key, str(value))
            resolved = resolved.replace(":" + key.replace("_", "-"), str(value))
        return resolved

    @staticmethod
    def _response_payload(response: httpx.Response) -> Any:
        if not response.content:
            return None
        content_type = response.headers.get("content-type", "")
        if "json" in content_type:
            return response.json()
        return response.text

    @staticmethod
    def _raise_for_response(response: httpx.Response, body: Any | None = None) -> None:
        if response.status_code < 400:
            return
        raise MetabaseError(
            "Metabase API request failed",
            status_code=response.status_code,
            response_body=body,
            request_id=response.headers.get("X-Request-ID"),
        )
