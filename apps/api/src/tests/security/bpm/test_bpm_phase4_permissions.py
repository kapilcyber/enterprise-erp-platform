"""BPM Phase 4 permission security tests."""

from modules.bpm.permissions import (
    BPM_ADMIN_PERMISSIONS,
    BPM_PERMISSIONS,
    PROCESS_OWNER_PERMISSIONS,
    WORKFLOW_AUDITOR_PERMISSIONS,
)

PHASE4 = {
    "bpm.instance:read",
    "bpm.instance:create",
    "bpm.instance:start",
    "bpm.instance:cancel",
    "bpm.instance:suspend",
    "bpm.instance:resume",
    "bpm.instance:complete",
    "bpm.instance:fail",
    "bpm.task:read",
    "bpm.task:assign",
    "bpm.task:claim",
    "bpm.task:complete",
    "bpm.task:reject",
    "bpm.history:read",
    "bpm.history:append",
    "bpm.delegation:read",
    "bpm.delegation:create",
    "bpm.delegation:accept",
    "bpm.delegation:reject",
    "bpm.delegation:expire",
}


def test_phase4_permissions_present():
    codes = {p[0] for p in BPM_PERMISSIONS}
    assert PHASE4.issubset(codes)


def test_admin_includes_phase4():
    assert PHASE4.issubset(set(BPM_ADMIN_PERMISSIONS))


def test_owner_can_operate_runtime():
    assert "bpm.instance:start" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.task:claim" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.history:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.delegation:accept" in PROCESS_OWNER_PERMISSIONS


def test_auditor_read_runtime():
    assert "bpm.instance:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.task:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.history:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.instance:start" not in WORKFLOW_AUDITOR_PERMISSIONS
