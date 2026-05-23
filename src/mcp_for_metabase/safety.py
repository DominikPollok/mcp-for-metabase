# SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import dataclass
from enum import StrEnum

from mcp_for_metabase.config import WriteMode
from mcp_for_metabase.errors import SafetyError
from mcp_for_metabase.safety_rules import (
    READ_METHODS,
    classify_special_risk,
    classify_write_risk,
)

__all__ = ["READ_METHODS", "SafetyDecision", "SafetyPolicy", "SafetyTier"]


class SafetyTier(StrEnum):
    READ = "read"
    SAFE_WRITE = "safe-write"
    DESTRUCTIVE = "destructive"
    ADMIN = "admin"


@dataclass(frozen=True, slots=True)
class SafetyDecision:
    allowed: bool
    tier: SafetyTier
    reason: str
    requires_confirmation: bool = False


class SafetyPolicy:
    """Central write gate for every Metabase API call."""

    def __init__(self, write_mode: WriteMode) -> None:
        self.write_mode = write_mode

    def classify(self, method: str, path: str, operation_id: str | None = None) -> SafetyTier:
        special_tier = classify_special_risk(method, path, operation_id)
        if special_tier is not None:
            return SafetyTier(special_tier)
        return SafetyTier(classify_write_risk(method, path, operation_id))

    def decide(
        self,
        method: str,
        path: str,
        *,
        operation_id: str | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> SafetyDecision:
        tier = self.classify(method, path, operation_id)

        if dry_run:
            return SafetyDecision(True, tier, "dry-run request is allowed")

        if tier == SafetyTier.READ:
            return SafetyDecision(True, tier, "read request is allowed")

        if self.write_mode == WriteMode.READ_ONLY:
            return SafetyDecision(False, tier, "write mode is read-only")

        if tier == SafetyTier.SAFE_WRITE and self.write_mode in {
            WriteMode.SAFE_WRITES,
            WriteMode.ALL_WRITES,
        }:
            return SafetyDecision(True, tier, "safe write is allowed")

        if tier in {SafetyTier.DESTRUCTIVE, SafetyTier.ADMIN}:
            if self.write_mode != WriteMode.ALL_WRITES:
                return SafetyDecision(False, tier, "all-writes mode is required")
            if not confirm:
                return SafetyDecision(False, tier, "confirm=true is required", True)
            return SafetyDecision(True, tier, "confirmed high-risk write is allowed", True)

        return SafetyDecision(False, tier, "request is not allowed")

    def ensure_allowed(
        self,
        method: str,
        path: str,
        *,
        operation_id: str | None = None,
        dry_run: bool = False,
        confirm: bool = False,
    ) -> SafetyDecision:
        decision = self.decide(
            method,
            path,
            operation_id=operation_id,
            dry_run=dry_run,
            confirm=confirm,
        )
        if not decision.allowed:
            raise SafetyError(
                f"Metabase request blocked: {decision.reason}",
                response_body={
                    "tier": decision.tier,
                    "requires_confirmation": decision.requires_confirmation,
                },
            )
        return decision
