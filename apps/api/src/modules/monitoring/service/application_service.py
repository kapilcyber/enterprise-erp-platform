"""Monitoring application façade — Phase 1–4."""

from sqlalchemy.orm import Session

from modules.monitoring.service.alert_routing_policy_service import AlertRoutingPolicyService
from modules.monitoring.service.alert_rule_service import AlertRuleService
from modules.monitoring.service.dashboard_definition_service import DashboardDefinitionService
from modules.monitoring.service.external_platform_binding_service import (
    ExternalPlatformBindingService,
)
from modules.monitoring.service.health_check_service import HealthCheckService
from modules.monitoring.service.log_trace_policy_service import LogTracePolicyService
from modules.monitoring.service.metric_definition_service import MetricDefinitionService
from modules.monitoring.service.monitored_component_service import MonitoredComponentService
from modules.monitoring.service.monitored_service_service import MonitoredServiceService
from modules.monitoring.service.observability_policy_service import ObservabilityPolicyService
from modules.monitoring.service.observability_policy_version_service import (
    ObservabilityPolicyVersionService,
)
from modules.monitoring.service.observability_report_service import ObservabilityReportService
from modules.monitoring.service.service_platform_assignment_service import (
    ServicePlatformAssignmentService,
)
from modules.monitoring.service.service_policy_assignment_service import (
    ServicePolicyAssignmentService,
)
from modules.monitoring.service.signal_correlation_service import SignalCorrelationService
from modules.monitoring.service.sli_definition_service import SliDefinitionService
from modules.monitoring.service.slo_definition_service import SloDefinitionService


class MonitoringApplicationService:
    """Phase 1–4 façade — wires entity services for routers."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self.observability_policies = ObservabilityPolicyService(db)
        self.observability_policy_versions = ObservabilityPolicyVersionService(db)
        self.monitored_services = MonitoredServiceService(db)
        self.monitored_components = MonitoredComponentService(db)
        self.metric_definitions = MetricDefinitionService(db)
        self.health_checks = HealthCheckService(db)
        self.service_policy_assignments = ServicePolicyAssignmentService(db)
        self.log_trace_policies = LogTracePolicyService(db)
        self.alert_rules = AlertRuleService(db)
        self.alert_routing_policies = AlertRoutingPolicyService(db)
        self.slo_definitions = SloDefinitionService(db)
        self.sli_definitions = SliDefinitionService(db)
        self.dashboard_definitions = DashboardDefinitionService(db)
        self.external_platform_bindings = ExternalPlatformBindingService(db)
        self.service_platform_assignments = ServicePlatformAssignmentService(db)
        self.signal_correlations = SignalCorrelationService(db)
        self.observability_reports = ObservabilityReportService(db)
