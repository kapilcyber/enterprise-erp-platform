"""Monitoring module router aggregation — Phase 1–4."""

from fastapi import APIRouter

from modules.monitoring.routers import (
    alert_routing_policies_router,
    alert_rules_router,
    components_router,
    dashboard_definitions_router,
    external_platform_bindings_router,
    health_checks_router,
    log_trace_policies_router,
    metric_definitions_router,
    observability_reports_router,
    policies_router,
    policy_versions_router,
    service_platform_assignments_router,
    service_policy_assignments_router,
    services_router,
    signal_correlations_router,
    sli_definitions_router,
    slo_definitions_router,
)

monitoring_router = APIRouter(
    prefix="/monitoring",
)
monitoring_router.include_router(policies_router)
monitoring_router.include_router(policy_versions_router)
monitoring_router.include_router(services_router)
monitoring_router.include_router(components_router)
monitoring_router.include_router(metric_definitions_router)
monitoring_router.include_router(health_checks_router)
monitoring_router.include_router(service_policy_assignments_router)
monitoring_router.include_router(log_trace_policies_router)
monitoring_router.include_router(alert_rules_router)
monitoring_router.include_router(alert_routing_policies_router)
monitoring_router.include_router(slo_definitions_router)
monitoring_router.include_router(sli_definitions_router)
monitoring_router.include_router(dashboard_definitions_router)
monitoring_router.include_router(external_platform_bindings_router)
monitoring_router.include_router(service_platform_assignments_router)
monitoring_router.include_router(signal_correlations_router)
monitoring_router.include_router(observability_reports_router)
