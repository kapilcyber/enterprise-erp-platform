"""BPM Phase 3B permission security tests."""

from modules.bpm.permissions import (
    BPM_ADMIN_PERMISSIONS,
    BPM_PERMISSIONS,
    PROCESS_DESIGNER_PERMISSIONS,
    PROCESS_OWNER_PERMISSIONS,
    WORKFLOW_AUDITOR_PERMISSIONS,
)

PHASE3B = {
    "bpm.trigger:read",
    "bpm.trigger:create",
    "bpm.trigger:update",
    "bpm.trigger:delete",
    "bpm.trigger:enable",
    "bpm.trigger:disable",
    "bpm.notification_template:read",
    "bpm.notification_template:create",
    "bpm.notification_template:update",
    "bpm.notification_template:delete",
    "bpm.notification_template:enable",
    "bpm.notification_template:disable",
}


def test_phase3b_permissions_present():
    codes = {p[0] for p in BPM_PERMISSIONS}
    assert PHASE3B.issubset(codes)


def test_admin_includes_phase3b():
    assert PHASE3B.issubset(set(BPM_ADMIN_PERMISSIONS))


def test_designer_can_edit_comms():
    assert "bpm.trigger:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.notification_template:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.trigger:enable" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.notification_template:enable" in PROCESS_DESIGNER_PERMISSIONS


def test_owner_reads_comms():
    assert "bpm.trigger:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.notification_template:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.trigger:create" not in PROCESS_OWNER_PERMISSIONS


def test_auditor_read_only_comms():
    assert "bpm.trigger:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.notification_template:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.trigger:delete" not in WORKFLOW_AUDITOR_PERMISSIONS
