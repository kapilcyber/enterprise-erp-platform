"""BPM Phase 1.5 permission security tests."""

from modules.bpm.permissions import (
    BPM_ADMIN_PERMISSIONS,
    BPM_PERMISSIONS,
    PROCESS_DESIGNER_PERMISSIONS,
    PROCESS_OWNER_PERMISSIONS,
    WORKFLOW_AUDITOR_PERMISSIONS,
)

PHASE15 = {
    "bpm.category:archive",
    "bpm.category:restore",
    "bpm.template:archive",
    "bpm.template:restore",
    "bpm.template:export",
    "bpm.template:import",
    "bpm.definition:archive",
    "bpm.definition:restore",
    "bpm.version:compare",
    "bpm.version:validate",
    "bpm.dashboard:read",
}


def test_phase15_permissions_present():
    codes = {p[0] for p in BPM_PERMISSIONS}
    assert PHASE15.issubset(codes)


def test_admin_includes_phase15():
    assert PHASE15.issubset(set(BPM_ADMIN_PERMISSIONS))


def test_designer_has_validate_not_publish():
    assert "bpm.version:validate" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.version:publish" not in PROCESS_DESIGNER_PERMISSIONS


def test_owner_has_publish_and_validate():
    assert "bpm.version:publish" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.version:validate" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.dashboard:read" in PROCESS_OWNER_PERMISSIONS


def test_auditor_read_only_includes_dashboard():
    assert "bpm.dashboard:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert all(":archive" not in p for p in WORKFLOW_AUDITOR_PERMISSIONS)
