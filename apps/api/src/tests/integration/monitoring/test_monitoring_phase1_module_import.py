"""Monitoring Phase 1 package smoke — 7 / 17 entities."""

from pathlib import Path

EXPECTED_MODELS = {
    "MonObservabilityPolicy",
    "MonObservabilityPolicyVersion",
    "MonMonitoredService",
    "MonMonitoredComponent",
    "MonMetricDefinition",
    "MonHealthCheck",
    "MonServicePolicyAssignment",
}

PHASE1_MIGRATIONS = (
    "0583_mon_observability_policy.py",
    "0584_mon_observability_policy_version.py",
    "0585_mon_monitored_service.py",
    "0586_mon_monitored_component.py",
    "0587_mon_metric_definition.py",
    "0588_mon_health_check.py",
    "0589_mon_service_policy_assignment.py",
)


def test_phase1_models_exported():
    from modules.monitoring import models

    exported = set(models.__all__)
    assert EXPECTED_MODELS.issubset(exported)
    for name in EXPECTED_MODELS:
        assert getattr(models, name) is not None


def test_phase1_router_has_business_routes():
    from modules.monitoring.router import monitoring_router

    assert monitoring_router.prefix == "/monitoring"
    paths = {getattr(r, "path", None) for r in monitoring_router.routes}
    assert any(p and "/policies" in p for p in paths)
    assert any(p and "/policy-versions" in p for p in paths)
    assert any(p and "/services" in p for p in paths)
    assert any(p and "/components" in p for p in paths)
    assert any(p and "/metric-definitions" in p for p in paths)
    assert any(p and "/health-checks" in p for p in paths)
    assert any(p and "/service-policy-assignments" in p for p in paths)


def test_phase1_application_service_wiring():
    from modules.monitoring.service import MonitoringApplicationService

    assert hasattr(MonitoringApplicationService, "__init__")
    # Instantiate shape check without DB: inspect annotations via unbound attrs on class
    src = Path(__file__).resolve().parents[3] / "modules" / "monitoring" / "service" / "application_service.py"
    text = src.read_text(encoding="utf-8")
    for attr in (
        "observability_policies",
        "observability_policy_versions",
        "monitored_services",
        "monitored_components",
        "metric_definitions",
        "health_checks",
        "service_policy_assignments",
    ):
        assert attr in text


def test_phase1_permissions_constants_no_seed():
    from modules.monitoring.permissions import (
        MONITORING_PERMISSION_NAMESPACE,
        MONITORING_PERMISSIONS,
        MONITORING_PHASE1_PERMISSIONS,
        PHASE1_PERMISSION_RESOURCES,
    )

    assert MONITORING_PERMISSION_NAMESPACE == "monitoring"
    assert len(MONITORING_PERMISSIONS) > 0
    assert len(MONITORING_PHASE1_PERMISSIONS) > 0
    assert all(
        p[1].split(".")[-1] in PHASE1_PERMISSION_RESOURCES for p in MONITORING_PHASE1_PERMISSIONS
    )
    assert set(MONITORING_PHASE1_PERMISSIONS).issubset(set(MONITORING_PERMISSIONS))
    alembic = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    seed_files = list(alembic.glob("*seed_monitoring*"))
    assert seed_files == []


def test_phase1_migrations_present():
    alembic = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    for name in PHASE1_MIGRATIONS:
        assert (alembic / name).is_file(), name
    # No Phase 2+ tables in Phase 1
    forbidden = (
        "mon_log_trace_policy",
        "mon_alert_rule",
        "mon_slo_definition",
        "mon_dashboard_definition",
        "mon_external_platform_binding",
    )
    for fname in PHASE1_MIGRATIONS:
        text = (alembic / fname).read_text(encoding="utf-8")
        for bad in forbidden:
            assert bad not in text


def test_phase1_engines_present():
    from modules.monitoring.service.engines import (
        AssignmentLifecycleEngine,
        MetricDefinitionLifecycleEngine,
        PolicyVersionLifecycleEngine,
    )

    assert PolicyVersionLifecycleEngine is not None
    assert MetricDefinitionLifecycleEngine is not None
    assert AssignmentLifecycleEngine is not None
