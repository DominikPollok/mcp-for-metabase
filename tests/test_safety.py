import pytest

from mcp_for_metabase.config import WriteMode
from mcp_for_metabase.errors import SafetyError
from mcp_for_metabase.safety import SafetyPolicy, SafetyTier


def test_read_requests_are_allowed_in_read_only() -> None:
    policy = SafetyPolicy(WriteMode.READ_ONLY)

    decision = policy.ensure_allowed("GET", "/api/dashboard/1")

    assert decision.tier == SafetyTier.READ


def test_safe_write_blocked_by_default() -> None:
    policy = SafetyPolicy(WriteMode.READ_ONLY)

    with pytest.raises(SafetyError):
        policy.ensure_allowed("POST", "/api/dashboard")


def test_dry_run_write_allowed_in_read_only() -> None:
    policy = SafetyPolicy(WriteMode.READ_ONLY)

    decision = policy.ensure_allowed("POST", "/api/dashboard", dry_run=True)

    assert decision.allowed is True
    assert decision.tier == SafetyTier.SAFE_WRITE


def test_dataset_query_post_is_read() -> None:
    policy = SafetyPolicy(WriteMode.READ_ONLY)

    decision = policy.ensure_allowed("POST", "/api/dataset")

    assert decision.tier == SafetyTier.READ


def test_action_execution_is_admin_even_when_get() -> None:
    policy = SafetyPolicy(WriteMode.ALL_WRITES)

    with pytest.raises(SafetyError):
        policy.ensure_allowed("GET", "/api/action/1/execute")

    decision = policy.ensure_allowed("GET", "/api/action/1/execute", confirm=True)

    assert decision.tier == SafetyTier.ADMIN


def test_dashboard_action_execution_is_admin_gated() -> None:
    policy = SafetyPolicy(WriteMode.ALL_WRITES)

    with pytest.raises(SafetyError):
        policy.ensure_allowed("POST", "/api/dashboard/1/dashcard/2/execute")

    decision = policy.ensure_allowed(
        "POST",
        "/api/dashboard/1/dashcard/2/execute",
        confirm=True,
    )

    assert decision.tier == SafetyTier.ADMIN


def test_public_link_creation_is_admin_gated() -> None:
    policy = SafetyPolicy(WriteMode.SAFE_WRITES)

    with pytest.raises(SafetyError):
        policy.ensure_allowed("POST", "/api/dashboard/1/public_link")


def test_admin_read_endpoints_remain_readable() -> None:
    policy = SafetyPolicy(WriteMode.READ_ONLY)

    decision = policy.ensure_allowed("GET", "/api/session/properties")

    assert decision.tier == SafetyTier.READ


def test_destructive_write_requires_all_writes_and_confirmation() -> None:
    policy = SafetyPolicy(WriteMode.ALL_WRITES)

    with pytest.raises(SafetyError):
        policy.ensure_allowed("DELETE", "/api/dashboard/1")

    decision = policy.ensure_allowed("DELETE", "/api/dashboard/1", confirm=True)
    assert decision.tier == SafetyTier.DESTRUCTIVE
