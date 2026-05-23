# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any
from urllib.parse import SplitResult, urlsplit, urlunsplit

SENSITIVE_HEADER_NAMES = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-metabase-session",
}


def redact_url(value: str) -> str:
    parsed = urlsplit(value)
    if not parsed.username and not parsed.password:
        return value
    host = parsed.hostname or ""
    if parsed.port:
        host = f"{host}:{parsed.port}"
    redacted = SplitResult(parsed.scheme, host, parsed.path, parsed.query, parsed.fragment)
    return urlunsplit(redacted)


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    return {
        key: "[REDACTED]" if key.lower() in SENSITIVE_HEADER_NAMES else value
        for key, value in headers.items()
    }


def redact_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if str(key).lower() in SENSITIVE_HEADER_NAMES else redact_value(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, str) and "://" in value:
        return redact_url(value)
    return value
