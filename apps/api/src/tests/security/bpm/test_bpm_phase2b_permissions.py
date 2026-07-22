"""BPM Phase 2B permission security tests."""

from modules.bpm.permissions import (
    BPM_ADMIN_PERMISSIONS,
    BPM_PERMISSIONS,
    PROCESS_DESIGNER_PERMISSIONS,
    PROCESS_OWNER_PERMISSIONS,
    WORKFLOW_AUDITOR_PERMISSIONS,
)

PHASE2B = {
    "bpm.decision_table:read",
    "bpm.decision_table:create",
    "bpm.decision_table:update",
    "bpm.decision_table:delete",
    "bpm.decision_table:enable",
    "bpm.decision_table:disable",
    "bpm.business_rule:read",
    "bpm.business_rule:create",
    "bpm.business_rule:update",
    "bpm.business_rule:delete",
    "bpm.variable:read",
    "bpm.variable:create",
    "bpm.variable:update",
    "bpm.variable:delete",
    "bpm.form_reference:read",
    "bpm.form_reference:create",
    "bpm.form_reference:update",
    "bpm.form_reference:delete",
}


def test_phase2b_permissions_present():
    codes = {p[0] for p in BPM_PERMISSIONS}
    assert PHASE2B.issubset(codes)


def test_admin_includes_phase2b():
    assert PHASE2B.issubset(set(BPM_ADMIN_PERMISSIONS))


def test_designer_can_edit_intelligence():
    assert "bpm.decision_table:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.business_rule:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.variable:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.form_reference:create" in PROCESS_DESIGNER_PERMISSIONS
    assert "bpm.decision_table:enable" in PROCESS_DESIGNER_PERMISSIONS


def test_owner_reads_intelligence():
    assert "bpm.decision_table:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.business_rule:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.variable:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.form_reference:read" in PROCESS_OWNER_PERMISSIONS
    assert "bpm.decision_table:create" not in PROCESS_OWNER_PERMISSIONS


def test_auditor_read_only_intelligence():
    assert "bpm.decision_table:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.variable:read" in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.decision_table:create" not in WORKFLOW_AUDITOR_PERMISSIONS
    assert "bpm.form_reference:delete" not in WORKFLOW_AUDITOR_PERMISSIONS
