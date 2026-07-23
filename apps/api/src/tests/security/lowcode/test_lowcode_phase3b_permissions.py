"""Low-Code Phase 3B permission security tests."""

from modules.lowcode.permissions import (
    FORM_DESIGNER_PERMISSIONS,
    LOWCODE_ADMIN_PERMISSIONS,
    LOWCODE_PERMISSIONS,
)


def test_phase3b_permissions_present():
    codes = {p[0] for p in LOWCODE_PERMISSIONS}
    assert "lowcode.page:read" in codes
    assert "lowcode.page:create" in codes
    assert "lowcode.page_version:publish" in codes
    assert "lowcode.page_version:clone" in codes
    assert "lowcode.page_region:create" in codes
    assert "lowcode.page_region:delete" in codes


def test_admin_includes_phase3b():
    assert "lowcode.page_version:publish" in LOWCODE_ADMIN_PERMISSIONS
    assert "lowcode.page:archive" in LOWCODE_ADMIN_PERMISSIONS


def test_designer_cannot_publish_page_version():
    assert "lowcode.page:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.page_version:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.page_region:create" in FORM_DESIGNER_PERMISSIONS
    assert all(":publish" not in p for p in FORM_DESIGNER_PERMISSIONS)
    assert all(":retire" not in p for p in FORM_DESIGNER_PERMISSIONS)
