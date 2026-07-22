"""BPM permission security tests — Phase 1."""

from modules.bpm.permissions import (
    BPM_ADMIN_PERMISSIONS,
    BPM_PERMISSIONS,
    PROCESS_DESIGNER_PERMISSIONS,
    PROCESS_OWNER_PERMISSIONS,
    WORKFLOW_AUDITOR_PERMISSIONS,
    WORKFLOW_OPERATOR_PERMISSIONS,
)


def test_permission_namespace():
    assert all(p[0].startswith("bpm.") for p in BPM_PERMISSIONS)
    assert all(p[3] == "bpm" for p in BPM_PERMISSIONS)


def test_admin_has_all():
    assert set(BPM_ADMIN_PERMISSIONS) == {p[0] for p in BPM_PERMISSIONS}


def test_role_slices_nonempty():
    assert PROCESS_DESIGNER_PERMISSIONS
    assert PROCESS_OWNER_PERMISSIONS
    assert WORKFLOW_OPERATOR_PERMISSIONS
    assert WORKFLOW_AUDITOR_PERMISSIONS


def test_designer_cannot_publish():
    assert all(":publish" not in p for p in PROCESS_DESIGNER_PERMISSIONS)


def test_auditor_read_only():
    assert all(":read" in p for p in WORKFLOW_AUDITOR_PERMISSIONS)
    assert all(
        x not in p
        for p in WORKFLOW_AUDITOR_PERMISSIONS
        for x in (":create", ":update", ":publish", ":delete")
    )
