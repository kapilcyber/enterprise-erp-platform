"""Low-Code Phase 3A permission security tests."""

from modules.lowcode.permissions import (
    FORM_DESIGNER_PERMISSIONS,
    LOWCODE_ADMIN_PERMISSIONS,
    LOWCODE_PERMISSIONS,
)


def test_phase3a_permissions_present():
    codes = {p[0] for p in LOWCODE_PERMISSIONS}
    assert "lowcode.event_handler:read" in codes
    assert "lowcode.event_handler:create" in codes
    assert "lowcode.event_handler:delete" in codes
    assert "lowcode.localization:read" in codes
    assert "lowcode.localization:publish" in codes
    assert "lowcode.localization:retire" in codes


def test_admin_includes_phase3a():
    assert "lowcode.event_handler:create" in LOWCODE_ADMIN_PERMISSIONS
    assert "lowcode.localization:publish" in LOWCODE_ADMIN_PERMISSIONS


def test_designer_cannot_publish_localization():
    assert "lowcode.event_handler:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.localization:create" in FORM_DESIGNER_PERMISSIONS
    assert all(":publish" not in p for p in FORM_DESIGNER_PERMISSIONS)
    assert all(":retire" not in p for p in FORM_DESIGNER_PERMISSIONS)
