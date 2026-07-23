"""Low-Code Phase 2B permission security tests."""

from modules.lowcode.permissions import (
    FORM_DESIGNER_PERMISSIONS,
    LOWCODE_ADMIN_PERMISSIONS,
    LOWCODE_PERMISSIONS,
)


def test_phase2b_permissions_present():
    codes = {p[0] for p in LOWCODE_PERMISSIONS}
    assert "lowcode.component:read" in codes
    assert "lowcode.component:create" in codes
    assert "lowcode.component_version:publish" in codes
    assert "lowcode.component_version:clone" in codes


def test_admin_includes_phase2b():
    assert "lowcode.component_version:publish" in LOWCODE_ADMIN_PERMISSIONS
    assert "lowcode.component:archive" in LOWCODE_ADMIN_PERMISSIONS


def test_designer_cannot_publish_component_version():
    assert "lowcode.component:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.component_version:create" in FORM_DESIGNER_PERMISSIONS
    assert all(":publish" not in p for p in FORM_DESIGNER_PERMISSIONS)
