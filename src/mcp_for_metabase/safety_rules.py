# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Literal

SafetyTierValue = Literal["read", "safe-write", "destructive", "admin"]

READ_METHODS = {"GET", "HEAD", "OPTIONS"}

ADMIN_PATH_PREFIXES = (
    "/api/api-key",
    "/api/ee/advanced-permissions",
    "/api/ee/ai-controls/permissions",
    "/api/group",
    "/api/permissions",
    "/api/setting",
    "/api/session",
    "/api/user",
)
ADMIN_OPERATION_MARKERS = (
    "admin",
    "api_key",
    "audit",
    "permission",
    "setting",
    "user",
)
DESTRUCTIVE_OPERATION_MARKERS = (
    "archive",
    "delete",
    "trash",
)
SAFE_WRITE_PATH_PREFIXES = (
    "/api/card",
    "/api/collection",
    "/api/dashboard",
    "/api/database",
    "/api/native-query-snippet",
    "/api/pulse",
    "/api/timeline",
)
ACTION_EXECUTE_PREFIXES = (
    "/api/action",
    "/api/ee/action",
    "/api/dashboard",
)


def classify_special_risk(
    method: str,
    path: str,
    operation_id: str | None = None,
) -> SafetyTierValue | None:
    method = method.upper()
    normalized = path.lower()

    if "/execute" in normalized and normalized.startswith(ACTION_EXECUTE_PREFIXES):
        return "admin"

    if normalized == "/api/dataset" or normalized.startswith("/api/dataset/"):
        return "read"

    if normalized.endswith("/query") or "/query/" in normalized:
        return "read"

    if method in READ_METHODS:
        return "read"

    if (
        normalized.endswith("/public_link")
        or normalized.endswith("/public-link")
        or "/public_link/" in normalized
        or "/public-link/" in normalized
    ):
        return "admin"

    return None


def classify_write_risk(
    method: str,
    path: str,
    operation_id: str | None = None,
) -> SafetyTierValue:
    method = method.upper()
    normalized = path.lower()
    operation = (operation_id or "").lower()

    if any(normalized.startswith(prefix) for prefix in ADMIN_PATH_PREFIXES) or any(
        marker in operation for marker in ADMIN_OPERATION_MARKERS
    ):
        return "admin"

    if (
        method == "DELETE"
        or any(marker in operation for marker in DESTRUCTIVE_OPERATION_MARKERS)
        or normalized.endswith("/delete")
    ):
        return "destructive"

    if any(normalized.startswith(prefix) for prefix in SAFE_WRITE_PATH_PREFIXES):
        return "safe-write"

    return "safe-write"
