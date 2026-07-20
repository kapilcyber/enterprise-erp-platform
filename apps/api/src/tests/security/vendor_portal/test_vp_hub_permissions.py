"""Vendor Portal permission security tests."""

from modules.vendor_portal.permissions import (
    PROCUREMENT_MANAGER_PERMISSIONS,
    QUALITY_COORDINATOR_PERMISSIONS,
    SUPPLIER_USER_PERMISSIONS,
    VENDOR_PORTAL_ADMIN_PERMISSIONS,
    VENDOR_PORTAL_PERMISSIONS,
)


def test_permission_namespace():
    assert all(p[0].startswith("vendor_portal.") for p in VENDOR_PORTAL_PERMISSIONS)
    assert all(p[3] == "vendor_portal" for p in VENDOR_PORTAL_PERMISSIONS)


def test_admin_has_all():
    assert set(VENDOR_PORTAL_ADMIN_PERMISSIONS) == {p[0] for p in VENDOR_PORTAL_PERMISSIONS}


def test_role_slices_nonempty():
    assert PROCUREMENT_MANAGER_PERMISSIONS
    assert SUPPLIER_USER_PERMISSIONS
    assert QUALITY_COORDINATOR_PERMISSIONS
