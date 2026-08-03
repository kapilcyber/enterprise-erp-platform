"""Monitoring routers — Phase 1–4."""

from modules.monitoring.routers.phase1 import (
    components_router,
    health_checks_router,
    metric_definitions_router,
    policies_router,
    policy_versions_router,
    service_policy_assignments_router,
    services_router,
)
from modules.monitoring.routers.phase2 import (
    alert_routing_policies_router,
    alert_rules_router,
    log_trace_policies_router,
)
from modules.monitoring.routers.phase3 import (
    dashboard_definitions_router,
    external_platform_bindings_router,
    service_platform_assignments_router,
    signal_correlations_router,
    sli_definitions_router,
    slo_definitions_router,
)
from modules.monitoring.routers.phase4 import observability_reports_router

__all__ = [
    "policies_router",
    "policy_versions_router",
    "services_router",
    "components_router",
    "metric_definitions_router",
    "health_checks_router",
    "service_policy_assignments_router",
    "log_trace_policies_router",
    "alert_rules_router",
    "alert_routing_policies_router",
    "slo_definitions_router",
    "sli_definitions_router",
    "dashboard_definitions_router",
    "external_platform_bindings_router",
    "service_platform_assignments_router",
    "signal_correlations_router",
    "observability_reports_router",
]
