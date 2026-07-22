"""BPM Phase 3A permission security tests."""

from modules.bpm.permissions import (
    BPM_ADMIN_PERMISSIONS,
    BPM_PERMISSIONS,
    PROCESS_DESIGNER_PERMISSIONS,
    PROCESS_OWNER_PERMISSIONS,
    WORKFLOW_AUDITOR_PERMISSIONS,
)

PHASE3A = {
    "bpm.assignment_rule:read",
    "bpm.assignment_rule:create",
    "bpm.assignment_rule:update",
    "bpm.assignment_rule:delete",
    "bpm.escalation_policy:read",
    "bpm.escalation_policy:create",
    "bpm.escalation_policy:update",
    "bpm.escalation_policy:delete",
    "bpm.sla_policy:read",
    "bpm.sla_policy:create",
    "bpm.sla_policy:update",
    "bpm.sla_policy:delete",
}


def test_phase3a_permissions_present():
    codes = {p[0] for p in BPM_PERMISSIONS}
    assert PHASE3A.issubset(codes)


def test_admin_includes_phase3a():
    assert PHASE3A.issubset(set(BPM_ADMIN_PERMISSIONS))


def test_designer_can_edit_governance():
    assert "bpm.assignment_rule:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.escalation_policy:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.sla_policy:create" in PROCESS_DESIGNER_PERMISSIONS


def test_owner_reads_governance():
    assert "bpm.assignment_rule:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.escalation_policy:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.sla_policy:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.assignment_rule:create" not in PROCESS_OWNER_PERMISSIONS


def test_auditor_read_only_governance():
    assert "bpm.assignment_rule:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.sla_policy:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.escalation_policy:delete" not in WORKFLOW_AUDITOR_PERMISSIONS
