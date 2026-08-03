"""Monitoring Phase 2 package smoke — 10 / 17 entities."""

from pathlib import Path

EXPECTED_PHASE2_MODELS = {
    "MonLogTracePolicy",
    "MonAlertRule",
    "MonAlertRoutingPolicy",
}

PHASE2_MIGRATIONS = (
    "0590_mon_log_trace_policy.py",
    "0591_mon_alert_rule.py",
    "0592_mon_alert_routing_policy.py",
)


def test_phase2_models_exported():
    from modules.monitoring import models

    exported = set(models.__all__)
    assert EXPECTED_PHASE2_MODELS.issubset(exported)
    assert len(exported) >= 10


def test_phase2_router_groups():
    from modules.monitoring.router import monitoring_router

    paths = {getattr(r, "path", None) for r in monitoring_router.routes}
    assert any(p and "/log-trace-policies" in p for p in paths)
    assert any(p and "/alert-rules" in p for p in paths)
    assert any(p and "/alert-routing-policies" in p for p in paths)


def test_phase2_application_service_wiring():
    src = (
        Path(__file__).resolve().parents[3]
        / "modules"
        / "monitoring"
        / "service"
        / "application_service.py"
    )
    text = src.read_text(encoding="utf-8")
    for attr in ("log_trace_policies", "alert_rules", "alert_routing_policies"):
        assert attr in text


def test_phase2_permissions_constants_no_seed():
    from modules.monitoring.permissions import (
        MONITORING_PERMISSIONS,
        MONITORING_PHASE2_PERMISSIONS,
    )

    assert len(MONITORING_PHASE2_PERMISSIONS) > 0
    assert all(
        p[1].split(".")[-1]
        in {"log_trace_policy", "alert_rule", "alert_routing_policy"}
        for p in MONITORING_PHASE2_PERMISSIONS
    )
    assert len(MONITORING_PERMISSIONS) >= len(MONITORING_PHASE2_PERMISSIONS)
    alembic = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    assert list(alembic.glob("*seed_monitoring*")) == []


def test_phase2_migrations_present():
    alembic = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    for name in PHASE2_MIGRATIONS:
        assert (alembic / name).is_file(), name
    forbidden = (
        "mon_slo_definition",
        "mon_sli_definition",
        "mon_dashboard_definition",
        "mon_external_platform_binding",
        "mon_signal_correlation",
        "mon_observability_report",
    )
    for fname in PHASE2_MIGRATIONS:
        text = (alembic / fname).read_text(encoding="utf-8")
        for bad in forbidden:
            assert bad not in text


def test_phase2_engines_present():
    from modules.monitoring.service.engines import (
        AlertRoutingPolicyLifecycleEngine,
        AlertRuleLifecycleEngine,
        LogTracePolicyLifecycleEngine,
    )

    assert LogTracePolicyLifecycleEngine is not None
    assert AlertRuleLifecycleEngine is not None
    assert AlertRoutingPolicyLifecycleEngine is not None


def test_alert_rule_slo_id_is_uuid_attribute_not_fk():
    from modules.monitoring.models.alert_rule import MonAlertRule

    col = MonAlertRule.__table__.c.slo_id
    assert col.foreign_keys == set()
