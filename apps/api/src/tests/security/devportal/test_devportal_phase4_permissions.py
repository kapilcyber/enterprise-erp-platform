"""Security tests — Developer Portal Phase 4 permissions."""

from modules.devportal.permissions import (
    DEVPORTAL_PERMISSIONS,
    DEVPORTAL_PHASE4_PERMISSIONS,
)


def test_phase4_permissions_namespaced():
    assert all(code.startswith("devportal.") for code, *_ in DEVPORTAL_PHASE4_PERMISSIONS)


def test_phase4_report_resource_and_export():
    resources = {p[1] for p in DEVPORTAL_PERMISSIONS}
    assert "devportal.report" in resources
    actions = {p[2] for p in DEVPORTAL_PERMISSIONS if p[1] == "devportal.report"}
    assert {"read", "create", "finalize", "export", "retire"} <= actions


def test_no_warehouse_or_billing_permissions():
    codes = " ".join(p[0] for p in DEVPORTAL_PERMISSIONS)
    assert "warehouse" not in codes
    assert "billing" not in codes
    assert "secret" not in codes
    assert "gateway" not in codes
