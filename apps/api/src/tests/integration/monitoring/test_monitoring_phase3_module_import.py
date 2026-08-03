"""Monitoring Phase 3 package smoke — 16 / 17 entities."""

from pathlib import Path

EXPECTED_PHASE3_MODELS = {
    "MonSloDefinition",
    "MonSliDefinition",
    "MonDashboardDefinition",
    "MonExternalPlatformBinding",
    "MonServicePlatformAssignment",
    "MonSignalCorrelation",
}

PHASE3_MIGRATIONS = (
    "0593_mon_slo_definition.py",
    "0594_mon_sli_definition.py",
    "0595_mon_dashboard_definition.py",
    "0596_mon_external_platform_binding.py",
    "0597_mon_service_platform_assignment.py",
    "0598_mon_signal_correlation.py",
)


def test_phase3_models_exported():
    from modules.monitoring import models

    exported = set(models.__all__)
    assert EXPECTED_PHASE3_MODELS.issubset(exported)
    assert len(exported) >= 16


def test_phase3_router_groups():
    from modules.monitoring.router import monitoring_router

    paths = {getattr(r, "path", None) for r in monitoring_router.routes}
    assert any(p and "/slo-definitions" in p for p in paths)
    assert any(p and "/sli-definitions" in p for p in paths)
    assert any(p and "/dashboard-definitions" in p for p in paths)
    assert any(p and "/external-platform-bindings" in p for p in paths)
    assert any(p and "/service-platform-assignments" in p for p in paths)
    assert any(p and "/signal-correlations" in p for p in paths)


def test_phase3_application_service_wiring():
    src = (
        Path(__file__).resolve().parents[3]
        / "modules"
        / "monitoring"
        / "service"
        / "application_service.py"
    )
    text = src.read_text(encoding="utf-8")
    for attr in (
        "slo_definitions",
        "sli_definitions",
        "dashboard_definitions",
        "external_platform_bindings",
        "service_platform_assignments",
        "signal_correlations",
    ):
        assert attr in text


def test_phase3_permissions_constants_no_seed():
    from modules.monitoring.permissions import (
        MONITORING_PERMISSIONS,
        MONITORING_PHASE3_PERMISSIONS,
        PHASE3_PERMISSION_RESOURCES,
    )

    assert len(MONITORING_PHASE3_PERMISSIONS) > 0
    assert all(
        p[1].split(".")[-1] in PHASE3_PERMISSION_RESOURCES
        for p in MONITORING_PHASE3_PERMISSIONS
    )
    assert len(MONITORING_PERMISSIONS) >= len(MONITORING_PHASE3_PERMISSIONS)
    alembic = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    assert list(alembic.glob("*seed_monitoring*")) == []


def test_phase3_migrations_present():
    alembic = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    for name in PHASE3_MIGRATIONS:
        assert (alembic / name).is_file(), name
    forbidden = ("mon_observability_report",)
    for fname in PHASE3_MIGRATIONS:
        text = (alembic / fname).read_text(encoding="utf-8")
        for bad in forbidden:
            assert bad not in text


def test_phase3_engines_present():
    from modules.monitoring.service.engines import (
        DashboardDefinitionLifecycleEngine,
        ExternalPlatformBindingLifecycleEngine,
        ServicePlatformAssignmentLifecycleEngine,
        SignalCorrelationLifecycleEngine,
        SliDefinitionLifecycleEngine,
        SloDefinitionLifecycleEngine,
    )

    assert SloDefinitionLifecycleEngine is not None
    assert SliDefinitionLifecycleEngine is not None
    assert DashboardDefinitionLifecycleEngine is not None
    assert ExternalPlatformBindingLifecycleEngine is not None
    assert ServicePlatformAssignmentLifecycleEngine is not None
    assert SignalCorrelationLifecycleEngine is not None


def test_slo_service_id_has_set_null_fk():
    from modules.monitoring.models.slo_definition import MonSloDefinition

    col = MonSloDefinition.__table__.c.service_id
    assert len(col.foreign_keys) == 1
    fk = next(iter(col.foreign_keys))
    assert fk.ondelete == "SET NULL"


def test_hub_projection_ref_is_uuid_attribute_not_fk():
    from modules.monitoring.models.service_platform_assignment import (
        MonServicePlatformAssignment,
    )

    col = MonServicePlatformAssignment.__table__.c.hub_projection_ref
    assert col.foreign_keys == set()
