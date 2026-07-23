"""Low-Code Phase 2A permission security tests."""

from modules.lowcode.permissions import (
    FORM_DESIGNER_PERMISSIONS,
    LOWCODE_ADMIN_PERMISSIONS,
    LOWCODE_PERMISSIONS,
)


def test_phase2a_permissions_present():
    codes = {p[0] for p in LOWCODE_PERMISSIONS}
    assert "lowcode.section:read" in codes
    assert "lowcode.section:create" in codes
    assert "lowcode.field:read" in codes
    assert "lowcode.field:create" in codes
    assert "lowcode.structure:validate" in codes


def test_admin_includes_phase2a():
    assert "lowcode.section:delete" in LOWCODE_ADMIN_PERMISSIONS
    assert "lowcode.field:delete" in LOWCODE_ADMIN_PERMISSIONS


def test_designer_has_structure_without_delete():
    assert "lowcode.section:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.field:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.structure:validate" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.section:delete" not in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.field:delete" not in FORM_DESIGNER_PERMISSIONS
