"""Low-Code Phase 2C permission security tests."""

from modules.lowcode.permissions import (
    FORM_DESIGNER_PERMISSIONS,
    LOWCODE_ADMIN_PERMISSIONS,
    LOWCODE_PERMISSIONS,
)


def test_phase2c_permissions_present():
    codes = {p[0] for p in LOWCODE_PERMISSIONS}
    assert "lowcode.data_source:read" in codes
    assert "lowcode.data_source:create" in codes
    assert "lowcode.data_source:activate" in codes
    assert "lowcode.expression:publish" in codes
    assert "lowcode.expression_binding:create" in codes
    assert "lowcode.expression_binding:delete" in codes


def test_admin_includes_phase2c():
    assert "lowcode.expression:publish" in LOWCODE_ADMIN_PERMISSIONS
    assert "lowcode.data_source:retire" in LOWCODE_ADMIN_PERMISSIONS
    assert "lowcode.expression_binding:delete" in LOWCODE_ADMIN_PERMISSIONS


def test_designer_cannot_publish_expression():
    assert "lowcode.data_source:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.expression:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.expression_binding:create" in FORM_DESIGNER_PERMISSIONS
    assert all(":publish" not in p for p in FORM_DESIGNER_PERMISSIONS)
    assert all(":retire" not in p for p in FORM_DESIGNER_PERMISSIONS)
