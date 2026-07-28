"""Security tests — Developer Portal Phase 3 permissions."""

from modules.devportal.permissions import (
    DEVPORTAL_PERMISSIONS,
    DEVPORTAL_PHASE3_PERMISSIONS,
)


def test_phase3_permissions_namespaced():
    assert all(code.startswith("devportal.") for code, *_ in DEVPORTAL_PHASE3_PERMISSIONS)


def test_phase3_resources_present():
    resources = {p[1] for p in DEVPORTAL_PERMISSIONS}
    for expected in (
        "devportal.documentation_entry",
        "devportal.openapi_artifact_reference",
        "devportal.sandbox_environment",
        "devportal.tryit_session",
    ):
        assert expected in resources


def test_no_openapi_generation_or_gateway_permissions():
    codes = " ".join(p[0] for p in DEVPORTAL_PERMISSIONS)
    assert "openapi:generate" not in codes
    assert "gateway" not in codes
    assert "secret" not in codes
    assert "billing" not in codes


def test_documentation_has_publish():
    actions = {p[2] for p in DEVPORTAL_PERMISSIONS if p[1] == "devportal.documentation_entry"}
    assert {"publish", "retire", "read", "create"} <= actions


def test_tryit_has_close_expire_not_invoke():
    actions = {p[2] for p in DEVPORTAL_PERMISSIONS if p[1] == "devportal.tryit_session"}
    assert {"close", "expire", "read", "create"} <= actions
    assert "invoke" not in actions
