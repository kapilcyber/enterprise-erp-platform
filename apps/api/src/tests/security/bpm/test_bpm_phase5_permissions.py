"""BPM Phase 5 permission security tests."""

from modules.bpm.permissions import (
    BPM_ADMIN_PERMISSIONS,
    BPM_PERMISSIONS,
    PROCESS_OWNER_PERMISSIONS,
    WORKFLOW_AUDITOR_PERMISSIONS,
)

PHASE5 = {
    "bpm.simulation:read",
    "bpm.simulation:create",
    "bpm.simulation:update",
    "bpm.simulation:delete",
    "bpm.simulation:run",
    "bpm.simulation:validate",
    "bpm.simulation:cancel",
}


def test_phase5_permissions_present():
    codes = {p[0] for p in BPM_PERMISSIONS}
    assert PHASE5.issubset(codes)


def test_admin_includes_phase5():
    assert PHASE5.issubset(set(BPM_ADMIN_PERMISSIONS))


def test_owner_can_run_and_validate_simulation():
    assert "bpm.simulation:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.simulation:run" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.simulation:validate" in PROCESS_OWNER_PERMISSIONS


def test_auditor_read_simulation_only():
    assert "bpm.simulation:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.simulation:run" not in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.simulation:create" not in WORKFLOW_AUDITOR_PERMISSIONS
