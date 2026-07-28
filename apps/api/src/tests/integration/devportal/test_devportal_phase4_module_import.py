"""API Developer Portal Phase 4 package smoke."""

from pathlib import Path


def test_phase4_models_export_18():
    from modules.devportal import models

    assert len(models.__all__) == 18
    assert "DpPortalReport" in models.__all__


def test_phase4_routes_registered():
    from modules.devportal.router import devportal_router

    paths = [getattr(r, "path", "") for r in devportal_router.routes]
    assert any("/reports" in p for p in paths)
    assert any("finalize" in p for p in paths)
    assert any("export" in p for p in paths)


def test_alembic_phase4_chain():
    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    for name in (
        "0580_dp_portal_report.py",
        "0581_seed_devportal_phase4_permissions.py",
    ):
        assert (versions / name).exists(), name


def test_permissions_phase4_resources():
    from modules.devportal.permissions import (
        DEVPORTAL_PERMISSIONS,
        DEVPORTAL_PHASE4_PERMISSIONS,
    )

    resources = {p[1] for p in DEVPORTAL_PERMISSIONS}
    assert "devportal.report" in resources
    assert len(DEVPORTAL_PHASE4_PERMISSIONS) > 0
    codes = {p[0] for p in DEVPORTAL_PHASE4_PERMISSIONS}
    assert "devportal.report:read" in codes
    assert "devportal.report:export" in codes


def test_application_service_wires_phase4():
    import inspect

    from modules.devportal.service.application_service import DevportalApplicationService

    src = inspect.getsource(DevportalApplicationService.__init__)
    assert "self.reports" in src


def test_no_analytics_warehouse_or_hub_orm():
    from pathlib import Path

    service = (
        Path(__file__).resolve().parents[3]
        / "modules"
        / "devportal"
        / "service"
        / "portal_report_service.py"
    )
    source = service.read_text(encoding="utf-8").lower()
    assert "modules.analytics.models" not in source
    assert "modules.integration.models" not in source
    assert "warehouse" not in source
    assert "etl" not in source
