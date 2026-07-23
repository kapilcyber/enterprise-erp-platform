"""Low-Code permission security tests — Phase 1."""

from modules.lowcode.permissions import (
    FORM_DESIGNER_PERMISSIONS,
    FORM_PUBLISHER_PERMISSIONS,
    LOWCODE_ADMIN_PERMISSIONS,
    LOWCODE_AUDITOR_PERMISSIONS,
    LOWCODE_PERMISSIONS,
)


def test_permission_namespace():
    assert all(p[0].startswith("lowcode.") for p in LOWCODE_PERMISSIONS)
    assert all(p[3] == "lowcode" for p in LOWCODE_PERMISSIONS)


def test_admin_has_all():
    assert set(LOWCODE_ADMIN_PERMISSIONS) == {p[0] for p in LOWCODE_PERMISSIONS}


def test_role_slices_nonempty():
    assert FORM_DESIGNER_PERMISSIONS
    assert FORM_PUBLISHER_PERMISSIONS
    assert LOWCODE_AUDITOR_PERMISSIONS


def test_designer_cannot_publish():
    assert all(":publish" not in p for p in FORM_DESIGNER_PERMISSIONS)


def test_auditor_read_only():
    assert all(":read" in p for p in LOWCODE_AUDITOR_PERMISSIONS)
    assert all(
        x not in p
        for p in LOWCODE_AUDITOR_PERMISSIONS
        for x in (":create", ":update", ":publish", ":delete")
    )
