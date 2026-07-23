"""Low-Code Phase 4 permission security tests."""

from modules.lowcode.permissions import (
    FORM_DESIGNER_PERMISSIONS,
    FORM_PUBLISHER_PERMISSIONS,
    LOWCODE_ADMIN_PERMISSIONS,
    LOWCODE_AUDITOR_PERMISSIONS,
    LOWCODE_PERMISSIONS,
)


def test_phase4_permissions_present():
    codes = {p[0] for p in LOWCODE_PERMISSIONS}
    assert "lowcode.publish_history:read" in codes
    assert "lowcode.runtime_submission:read" in codes
    assert "lowcode.runtime_submission:create" in codes
    assert "lowcode.runtime_submission:update" in codes
    assert "lowcode.preview_session:read" in codes
    assert "lowcode.preview_session:create" in codes
    assert "lowcode.preview_session:close" in codes
    assert "lowcode.preview_session:expire" in codes


def test_admin_includes_phase4():
    assert "lowcode.publish_history:read" in LOWCODE_ADMIN_PERMISSIONS
    assert "lowcode.runtime_submission:create" in LOWCODE_ADMIN_PERMISSIONS
    assert "lowcode.preview_session:expire" in LOWCODE_ADMIN_PERMISSIONS


def test_designer_preview_but_not_delete_history():
    assert "lowcode.preview_session:create" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.preview_session:close" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.publish_history:read" in FORM_DESIGNER_PERMISSIONS
    assert "lowcode.runtime_submission:create" in FORM_DESIGNER_PERMISSIONS
    assert all(":publish" not in p for p in FORM_DESIGNER_PERMISSIONS)
    assert all(":retire" not in p for p in FORM_DESIGNER_PERMISSIONS)


def test_publisher_and_auditor_read_phase4():
    assert "lowcode.publish_history:read" in FORM_PUBLISHER_PERMISSIONS
    assert "lowcode.runtime_submission:read" in FORM_PUBLISHER_PERMISSIONS
    assert "lowcode.preview_session:read" in FORM_PUBLISHER_PERMISSIONS
    assert "lowcode.runtime_submission:create" not in FORM_PUBLISHER_PERMISSIONS
    assert all(":read" in p for p in LOWCODE_AUDITOR_PERMISSIONS)
    assert "lowcode.publish_history:read" in LOWCODE_AUDITOR_PERMISSIONS
