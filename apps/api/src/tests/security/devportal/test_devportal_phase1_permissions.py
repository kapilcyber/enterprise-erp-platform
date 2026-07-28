"""Security tests — Developer Portal Phase 1 permissions."""

from modules.devportal.permissions import (
    API_AUDITOR_PERMISSIONS,
    DEVPORTAL_ADMIN_PERMISSIONS,
    DEVPORTAL_PERMISSIONS,
)


def test_all_permissions_use_devportal_namespace():
    assert all(code.startswith("devportal.") for code, *_ in DEVPORTAL_PERMISSIONS)


def test_admin_has_all_permissions():
    codes = {p[0] for p in DEVPORTAL_PERMISSIONS}
    assert set(DEVPORTAL_ADMIN_PERMISSIONS) == codes


def test_auditor_is_read_mostly():
    assert all(
        p.endswith(":read") or p.endswith(":validate") or p.endswith(":export")
        for p in API_AUDITOR_PERMISSIONS
    )


def test_phase1_resources_present():
    resources = {p[1] for p in DEVPORTAL_PERMISSIONS}
    for expected in (
        "devportal.developer_account",
        "devportal.application",
        "devportal.api_product_version",
        "devportal.developer_invite",
        "devportal.portal_session",
    ):
        assert expected in resources


def test_no_secret_or_gateway_permissions():
    codes = " ".join(p[0] for p in DEVPORTAL_PERMISSIONS)
    assert "secret" not in codes
    assert "gateway" not in codes
    assert "oauth_secret" not in codes
