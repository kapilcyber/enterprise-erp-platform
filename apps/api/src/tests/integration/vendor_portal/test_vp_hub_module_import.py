"""Vendor Portal module import smoke tests."""

def test_import_models():
    from modules.vendor_portal import models
    assert models.VpPortalAccount is not None
    assert models.VpReport is not None
    assert len(models.__all__) == 20


def test_import_router():
    from modules.vendor_portal.router import vendor_portal_router
    assert vendor_portal_router.prefix == "/vendor-portal"


def test_import_services():
    from modules.vendor_portal.service import VendorPortalApplicationService
    assert VendorPortalApplicationService is not None
