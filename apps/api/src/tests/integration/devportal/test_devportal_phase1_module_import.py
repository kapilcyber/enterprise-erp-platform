"""API Developer Portal Phase 1 package smoke."""

from pathlib import Path


def test_phase1_models_export_10():
    from modules.devportal import models

    assert len(models.__all__) >= 10
    assert "DpDeveloperAccount" in models.__all__
    assert "DpApplication" in models.__all__
    assert "DpApiProductVersion" in models.__all__


def test_import_router_and_services():
    from modules.devportal.router import devportal_router
    from modules.devportal.service import DevportalApplicationService

    assert devportal_router.prefix == "/devportal"
    assert len(devportal_router.routes) > 0
    assert DevportalApplicationService is not None


def test_shared_router_includes_devportal():
    shared_router_path = Path(__file__).resolve().parents[3] / "shared" / "router.py"
    source = shared_router_path.read_text(encoding="utf-8")
    assert "from modules.devportal.router import devportal_router" in source
    assert "include_router(devportal_router)" in source


def test_alembic_phase1_chain():
    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    expected = [
        "0560_dp_developer_organization.py",
        "0561_dp_developer_team.py",
        "0562_dp_developer_account.py",
        "0563_dp_developer_membership.py",
        "0564_dp_developer_invite.py",
        "0565_dp_portal_session.py",
        "0566_dp_application.py",
        "0567_dp_api_product.py",
        "0568_dp_api_product_version.py",
        "0569_dp_api_product_environment.py",
        "0570_seed_devportal_phase1_permissions.py",
    ]
    for name in expected:
        assert (versions / name).exists(), name


def test_permissions_phase1_seeded_constants():
    from modules.devportal.permissions import (
        DEVPORTAL_ADMIN_PERMISSIONS,
        DEVPORTAL_PERMISSION_NAMESPACE,
        DEVPORTAL_PERMISSIONS,
    )

    assert DEVPORTAL_PERMISSION_NAMESPACE == "devportal"
    assert len(DEVPORTAL_PERMISSIONS) > 0
    assert all(p[0].startswith("devportal.") for p in DEVPORTAL_PERMISSIONS)
    assert set(DEVPORTAL_ADMIN_PERMISSIONS) == {p[0] for p in DEVPORTAL_PERMISSIONS}


def test_application_service_wires_phase1():
    import inspect

    from modules.devportal.service.application_service import DevportalApplicationService

    src = inspect.getsource(DevportalApplicationService.__init__)
    for attr in (
        "self.organizations",
        "self.teams",
        "self.accounts",
        "self.memberships",
        "self.invites",
        "self.sessions",
        "self.applications",
        "self.api_products",
        "self.api_product_versions",
        "self.api_product_environments",
        "self.publish_validation",
    ):
        assert attr in src


def test_no_peer_orm_in_hub_adapter():
    from pathlib import Path

    hub = Path(__file__).resolve().parents[3] / "modules" / "devportal" / "adapters" / "integration_hub_port.py"
    source = hub.read_text(encoding="utf-8")
    assert "modules.integration.models" not in source
    assert "IntOauthClient" not in source
    assert "IntApiCredential" not in source
