"""BPM Phase 2A permission security tests."""

from modules.bpm.permissions import (
    BPM_ADMIN_PERMISSIONS,
    BPM_PERMISSIONS,
    PROCESS_DESIGNER_PERMISSIONS,
    PROCESS_OWNER_PERMISSIONS,
    WORKFLOW_AUDITOR_PERMISSIONS,
)

PHASE2A = {
    "bpm.node:read",
    "bpm.node:create",
    "bpm.node:update",
    "bpm.node:delete",
    "bpm.transition:read",
    "bpm.transition:create",
    "bpm.transition:update",
    "bpm.transition:delete",
    "bpm.graph:validate",
}


def test_phase2a_permissions_present():
    codes = {p[0] for p in BPM_PERMISSIONS}
    assert PHASE2A.issubset(codes)


def test_admin_includes_phase2a():
    assert PHASE2A.issubset(set(BPM_ADMIN_PERMISSIONS))


def test_designer_can_edit_graph():
    assert "bpm.node:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.transition:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.graph:validate" in PROCESS_DESIGNER_PERMISSIONS


def test_owner_can_validate_graph_read():
    assert "bpm.node:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.transition:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.graph:validate" in PROCESS_OWNER_PERMISSIONS


def test_auditor_read_nodes():
    assert "bpm.node:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.transition:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.node:create" not in WORKFLOW_AUDITOR_PERMISSIONS
