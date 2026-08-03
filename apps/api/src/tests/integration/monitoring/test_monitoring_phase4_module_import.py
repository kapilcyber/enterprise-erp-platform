"""Monitoring Phase 4 package smoke — 17 / 17 entities."""

from pathlib import Path

EXPECTED_PHASE4_MODELS = {"MonObservabilityReport"}

PHASE4_MIGRATIONS = ("0599_mon_observability_report.py",)


def test_phase4_models_exported():
    from modules.monitoring import models

    exported = set(models.__all__)
    assert EXPECTED_PHASE4_MODELS.issubset(exported)
    assert len(exported) == 17


def test_phase4_router_groups():
    from modules.monitoring.router import monitoring_router

    paths = {getattr(r, "path", None) for r in monitoring_router.routes}
    assert any(p and "/observability-reports" in p for p in paths)


def test_phase4_application_service_wiring():
    src = (
        Path(__file__).resolve().parents[3]
        / "modules"
        / "monitoring"
        / "service"
        / "application_service.py"
    )
    text = src.read_text(encoding="utf-8")
    assert "observability_reports" in text


def test_phase4_permissions_constants_no_seed():
    from modules.monitoring.permissions import (
        MONITORING_PERMISSIONS,
        MONITORING_PHASE4_PERMISSIONS,
        PHASE4_PERMISSION_RESOURCES,
    )

    assert len(MONITORING_PHASE4_PERMISSIONS) > 0
    assert all(
        p[1].split(".")[-1] in PHASE4_PERMISSION_RESOURCES
        for p in MONITORING_PHASE4_PERMISSIONS
    )
    assert len(MONITORING_PERMISSIONS) >= len(MONITORING_PHASE4_PERMISSIONS)
    alembic = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    assert list(alembic.glob("*seed_monitoring*")) == []


def test_phase4_migration_present():
    alembic = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    for name in PHASE4_MIGRATIONS:
        assert (alembic / name).is_file(), name
    text = (alembic / "0599_mon_observability_report.py").read_text(encoding="utf-8")
    assert "seed_monitoring" not in text


def test_phase4_engine_present():
    from modules.monitoring.service.engines import ObservabilityReportLifecycleEngine

    assert ObservabilityReportLifecycleEngine is not None


def test_observability_report_has_no_peer_fk():
    from modules.monitoring.models.observability_report import MonObservabilityReport

    # Standalone ops entity — only org_branch optional FK among non-mixin columns
    peer_fks = [
        fk
        for col in MonObservabilityReport.__table__.columns
        for fk in col.foreign_keys
        if not str(fk.target_fullname).startswith("organization.")
        and not str(fk.target_fullname).startswith("foundation.")
    ]
    assert peer_fks == []
