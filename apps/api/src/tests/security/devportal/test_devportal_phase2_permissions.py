"""Security tests — Developer Portal Phase 2 permissions."""

from modules.devportal.permissions import (
    DEVPORTAL_PERMISSIONS,
    DEVPORTAL_PHASE2_PERMISSIONS,
)


def test_phase2_permissions_namespaced():
    assert all(code.startswith("devportal.") for code, *_ in DEVPORTAL_PHASE2_PERMISSIONS)


def test_phase2_resources_present():
    resources = {p[1] for p in DEVPORTAL_PERMISSIONS}
    for expected in ("devportal.plan", "devportal.subscription", "devportal.entitlement"):
        assert expected in resources


def test_no_gateway_billing_permission_codes():
    codes = " ".join(p[0] for p in DEVPORTAL_PERMISSIONS)
    assert "gateway" not in codes
    assert "billing" not in codes
    assert "payment" not in codes
    assert "rate_limit" not in codes
    assert "oauth_secret" not in codes


def test_plan_has_publish_actions():
    plan_actions = {p[2] for p in DEVPORTAL_PERMISSIONS if p[1] == "devportal.plan"}
    assert {"publish", "retire", "validate", "read", "create"} <= plan_actions


def test_subscription_has_approval_actions():
    sub_actions = {p[2] for p in DEVPORTAL_PERMISSIONS if p[1] == "devportal.subscription"}
    assert {"submit", "approve", "activate", "suspend", "retire"} <= sub_actions
