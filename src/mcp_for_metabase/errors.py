# SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class MetabaseError(Exception):
    """Structured error returned for failed Metabase API calls."""

    message: str
    status_code: int | None = None
    response_body: Any | None = None
    request_id: str | None = None

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        if self.request_id:
            parts.append(f"request_id={self.request_id}")
        return " ".join(parts)


class SafetyError(MetabaseError):
    """Raised when a request violates configured write-safety policy."""


class RegistryError(MetabaseError):
    """Raised when an OpenAPI operation cannot be resolved."""
