"""Monitoring Pydantic schemas — Phase 1."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


class LifecycleReason(BaseModel):
    reason: str | None = None


# --- Observability Policy ---


class ObservabilityPolicyCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    policy_code: str | None = None
    policy_name: str
    description: str | None = None
    scope_level: str | None = "platform"
    status: str | None = "draft"
    metadata_json: dict | None = None


class ObservabilityPolicyUpdate(BaseModel):
    policy_name: str | None = None
    description: str | None = None
    scope_level: str | None = None
    metadata_json: dict | None = None
    version: int | None = None


class ObservabilityPolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    policy_code: str
    policy_name: str
    description: str | None = None
    scope_level: str
    status: str
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Observability Policy Version ---


class ObservabilityPolicyVersionCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    policy_id: UUID
    version_label: str
    version_number: int | None = 1
    retention_intent_json: dict | None = None
    sampling_intent_json: dict | None = None
    redaction_policy_json: dict | None = None
    content_json: dict | None = None
    change_summary: str | None = None
    workflow_instance_id: UUID | None = None
    status: str | None = "draft"


class ObservabilityPolicyVersionUpdate(BaseModel):
    version_label: str | None = None
    version_number: int | None = None
    retention_intent_json: dict | None = None
    sampling_intent_json: dict | None = None
    redaction_policy_json: dict | None = None
    content_json: dict | None = None
    change_summary: str | None = None
    workflow_instance_id: UUID | None = None
    version: int | None = None


class ObservabilityPolicyVersionResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    policy_id: UUID
    version_label: str
    version_number: int
    retention_intent_json: dict | None = None
    sampling_intent_json: dict | None = None
    redaction_policy_json: dict | None = None
    content_json: dict | None = None
    status: str
    published_at: datetime | None = None
    retired_at: datetime | None = None
    workflow_instance_id: UUID | None = None
    change_summary: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Monitored Service ---


class MonitoredServiceCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    service_code: str | None = None
    service_name: str
    description: str | None = None
    module_code: str | None = None
    peer_module_ref: UUID | None = None
    environment_class: str | None = "production"
    owner_ref: UUID | None = None
    status: str | None = "draft"
    metadata_json: dict | None = None


class MonitoredServiceUpdate(BaseModel):
    service_name: str | None = None
    description: str | None = None
    module_code: str | None = None
    peer_module_ref: UUID | None = None
    environment_class: str | None = None
    owner_ref: UUID | None = None
    metadata_json: dict | None = None
    version: int | None = None


class MonitoredServiceResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    service_code: str
    service_name: str
    description: str | None = None
    module_code: str | None = None
    peer_module_ref: UUID | None = None
    environment_class: str
    owner_ref: UUID | None = None
    status: str
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Monitored Component ---


class MonitoredComponentCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    service_id: UUID
    component_code: str | None = None
    component_name: str
    description: str | None = None
    component_kind: str | None = None
    status: str | None = "draft"
    metadata_json: dict | None = None


class MonitoredComponentUpdate(BaseModel):
    component_name: str | None = None
    description: str | None = None
    component_kind: str | None = None
    metadata_json: dict | None = None
    version: int | None = None


class MonitoredComponentResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    service_id: UUID
    component_code: str
    component_name: str
    description: str | None = None
    component_kind: str | None = None
    status: str
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Metric Definition ---


class MetricDefinitionCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    metric_code: str | None = None
    metric_name: str
    description: str | None = None
    metric_type: str
    unit: str | None = None
    label_schema_json: dict | None = None
    definition_version: int | None = 1
    status: str | None = "draft"
    metadata_json: dict | None = None


class MetricDefinitionUpdate(BaseModel):
    metric_name: str | None = None
    description: str | None = None
    metric_type: str | None = None
    unit: str | None = None
    label_schema_json: dict | None = None
    definition_version: int | None = None
    metadata_json: dict | None = None
    version: int | None = None


class MetricDefinitionResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    metric_code: str
    metric_name: str
    description: str | None = None
    metric_type: str
    unit: str | None = None
    label_schema_json: dict | None = None
    definition_version: int
    status: str
    published_at: datetime | None = None
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Health Check ---


class HealthCheckCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    service_id: UUID
    component_id: UUID | None = None
    check_code: str | None = None
    check_name: str
    check_kind: str | None = "http"
    endpoint_ref: str | None = None
    interval_seconds: int | None = None
    timeout_seconds: int | None = None
    definition_json: dict | None = None
    status: str | None = "draft"
    metadata_json: dict | None = None


class HealthCheckUpdate(BaseModel):
    check_name: str | None = None
    check_kind: str | None = None
    endpoint_ref: str | None = None
    interval_seconds: int | None = None
    timeout_seconds: int | None = None
    definition_json: dict | None = None
    component_id: UUID | None = None
    metadata_json: dict | None = None
    version: int | None = None


class HealthCheckResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    service_id: UUID
    component_id: UUID | None = None
    check_code: str
    check_name: str
    check_kind: str
    endpoint_ref: str | None = None
    interval_seconds: int | None = None
    timeout_seconds: int | None = None
    definition_json: dict | None = None
    status: str
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Service Policy Assignment ---


class ServicePolicyAssignmentCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    service_id: UUID
    component_id: UUID | None = None
    policy_version_id: UUID
    assignment_code: str | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    status: str | None = "active"
    metadata_json: dict | None = None


class ServicePolicyAssignmentUpdate(BaseModel):
    assignment_code: str | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    component_id: UUID | None = None
    metadata_json: dict | None = None
    version: int | None = None


class ServicePolicyAssignmentResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    service_id: UUID
    component_id: UUID | None = None
    policy_version_id: UUID
    assignment_code: str | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    status: str
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Log Trace Policy (Phase 2) ---


class LogTracePolicyCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    policy_code: str | None = None
    policy_name: str
    signal_kind: str
    policy_version_id: UUID | None = None
    classification_json: dict | None = None
    sampling_json: dict | None = None
    redaction_json: dict | None = None
    retention_intent_json: dict | None = None
    definition_version: int | None = 1
    status: str | None = "draft"
    metadata_json: dict | None = None


class LogTracePolicyUpdate(BaseModel):
    policy_name: str | None = None
    signal_kind: str | None = None
    policy_version_id: UUID | None = None
    classification_json: dict | None = None
    sampling_json: dict | None = None
    redaction_json: dict | None = None
    retention_intent_json: dict | None = None
    definition_version: int | None = None
    metadata_json: dict | None = None
    version: int | None = None


class LogTracePolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    policy_code: str
    policy_name: str
    signal_kind: str
    policy_version_id: UUID | None = None
    classification_json: dict | None = None
    sampling_json: dict | None = None
    redaction_json: dict | None = None
    retention_intent_json: dict | None = None
    definition_version: int
    status: str
    published_at: datetime | None = None
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Alert Rule (Phase 2) ---


class AlertRuleCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    rule_code: str | None = None
    rule_name: str
    description: str | None = None
    severity: str | None = "warning"
    metric_definition_id: UUID | None = None
    slo_id: UUID | None = None
    condition_json: dict | None = None
    definition_version: int | None = 1
    status: str | None = "draft"
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None


class AlertRuleUpdate(BaseModel):
    rule_name: str | None = None
    description: str | None = None
    severity: str | None = None
    metric_definition_id: UUID | None = None
    slo_id: UUID | None = None
    condition_json: dict | None = None
    definition_version: int | None = None
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None
    version: int | None = None


class AlertRuleResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    rule_code: str
    rule_name: str
    description: str | None = None
    severity: str
    metric_definition_id: UUID | None = None
    slo_id: UUID | None = None
    condition_json: dict | None = None
    definition_version: int
    status: str
    published_at: datetime | None = None
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Alert Routing Policy (Phase 2) ---


class AlertRoutingPolicyCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    alert_rule_id: UUID
    routing_code: str | None = None
    routing_name: str
    notification_channel_ref: UUID
    channel_kind: str | None = None
    routing_json: dict | None = None
    is_critical_route: bool | None = False
    definition_version: int | None = 1
    status: str | None = "draft"
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None


class AlertRoutingPolicyUpdate(BaseModel):
    routing_name: str | None = None
    notification_channel_ref: UUID | None = None
    channel_kind: str | None = None
    routing_json: dict | None = None
    is_critical_route: bool | None = None
    definition_version: int | None = None
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None
    version: int | None = None


class AlertRoutingPolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    alert_rule_id: UUID
    routing_code: str
    routing_name: str
    notification_channel_ref: UUID
    channel_kind: str | None = None
    routing_json: dict | None = None
    is_critical_route: bool
    definition_version: int
    status: str
    published_at: datetime | None = None
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- SLO Definition (Phase 3) ---


class SloDefinitionCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    service_id: UUID | None = None
    slo_code: str | None = None
    slo_name: str
    description: str | None = None
    objective_json: dict | None = None
    definition_version: int | None = 1
    status: str | None = "draft"
    metadata_json: dict | None = None


class SloDefinitionUpdate(BaseModel):
    service_id: UUID | None = None
    slo_name: str | None = None
    description: str | None = None
    objective_json: dict | None = None
    definition_version: int | None = None
    metadata_json: dict | None = None
    version: int | None = None


class SloDefinitionResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    service_id: UUID | None = None
    slo_code: str
    slo_name: str
    description: str | None = None
    objective_json: dict | None = None
    definition_version: int
    status: str
    published_at: datetime | None = None
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- SLI Definition (Phase 3) ---


class SliDefinitionCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    slo_id: UUID
    sli_code: str | None = None
    sli_name: str
    description: str | None = None
    indicator_json: dict | None = None
    metric_definition_id: UUID | None = None
    definition_version: int | None = 1
    status: str | None = "draft"
    metadata_json: dict | None = None


class SliDefinitionUpdate(BaseModel):
    sli_name: str | None = None
    description: str | None = None
    indicator_json: dict | None = None
    metric_definition_id: UUID | None = None
    definition_version: int | None = None
    metadata_json: dict | None = None
    version: int | None = None


class SliDefinitionResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    slo_id: UUID
    sli_code: str
    sli_name: str
    description: str | None = None
    indicator_json: dict | None = None
    metric_definition_id: UUID | None = None
    definition_version: int
    status: str
    published_at: datetime | None = None
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Dashboard Definition (Phase 3) ---


class DashboardDefinitionCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    dashboard_code: str | None = None
    dashboard_name: str
    description: str | None = None
    policy_version_id: UUID | None = None
    layout_json: dict | None = None
    definition_version: int | None = 1
    status: str | None = "draft"
    metadata_json: dict | None = None


class DashboardDefinitionUpdate(BaseModel):
    dashboard_name: str | None = None
    description: str | None = None
    policy_version_id: UUID | None = None
    layout_json: dict | None = None
    definition_version: int | None = None
    metadata_json: dict | None = None
    version: int | None = None


class DashboardDefinitionResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    dashboard_code: str
    dashboard_name: str
    description: str | None = None
    policy_version_id: UUID | None = None
    layout_json: dict | None = None
    definition_version: int
    status: str
    published_at: datetime | None = None
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- External Platform Binding (Phase 3) ---


class ExternalPlatformBindingCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    binding_code: str | None = None
    binding_name: str
    platform_type: str
    external_ref: str | None = None
    adapter_key: str | None = None
    secret_ref: str | None = None
    endpoint_ref: str | None = None
    binding_json: dict | None = None
    definition_version: int | None = 1
    status: str | None = "draft"
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None


class ExternalPlatformBindingUpdate(BaseModel):
    binding_name: str | None = None
    platform_type: str | None = None
    external_ref: str | None = None
    adapter_key: str | None = None
    secret_ref: str | None = None
    endpoint_ref: str | None = None
    binding_json: dict | None = None
    definition_version: int | None = None
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None
    version: int | None = None


class ExternalPlatformBindingResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    binding_code: str
    binding_name: str
    platform_type: str
    external_ref: str | None = None
    adapter_key: str | None = None
    secret_ref: str | None = None
    endpoint_ref: str | None = None
    binding_json: dict | None = None
    definition_version: int
    status: str
    activated_at: datetime | None = None
    workflow_instance_id: UUID | None = None
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Service Platform Assignment (Phase 3) ---


class ServicePlatformAssignmentCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    service_id: UUID
    component_id: UUID | None = None
    platform_binding_id: UUID
    assignment_code: str | None = None
    hub_projection_ref: UUID | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    status: str | None = "active"
    metadata_json: dict | None = None


class ServicePlatformAssignmentUpdate(BaseModel):
    component_id: UUID | None = None
    assignment_code: str | None = None
    hub_projection_ref: UUID | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    metadata_json: dict | None = None
    version: int | None = None


class ServicePlatformAssignmentResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    service_id: UUID
    component_id: UUID | None = None
    platform_binding_id: UUID
    assignment_code: str | None = None
    hub_projection_ref: UUID | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    status: str
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Signal Correlation (Phase 3) ---


class SignalCorrelationCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    correlation_code: str | None = None
    correlation_name: str
    description: str | None = None
    alert_rule_id: UUID | None = None
    metric_definition_id: UUID | None = None
    correlation_json: dict | None = None
    status: str | None = "draft"
    metadata_json: dict | None = None


class SignalCorrelationUpdate(BaseModel):
    correlation_name: str | None = None
    description: str | None = None
    alert_rule_id: UUID | None = None
    metric_definition_id: UUID | None = None
    correlation_json: dict | None = None
    metadata_json: dict | None = None
    version: int | None = None


class SignalCorrelationResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    correlation_code: str
    correlation_name: str
    description: str | None = None
    alert_rule_id: UUID | None = None
    metric_definition_id: UUID | None = None
    correlation_json: dict | None = None
    status: str
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None


# --- Observability Report (Phase 4) ---


class ObservabilityReportCreate(BaseModel):
    company_id: UUID | None = None
    branch_id: UUID | None = None
    report_code: str | None = None
    report_name: str
    description: str | None = None
    report_kind: str | None = "operational"
    definition_json: dict | None = None
    last_generated_at: datetime | None = None
    export_format: str | None = None
    status: str | None = "draft"
    metadata_json: dict | None = None


class ObservabilityReportUpdate(BaseModel):
    report_name: str | None = None
    description: str | None = None
    report_kind: str | None = None
    definition_json: dict | None = None
    last_generated_at: datetime | None = None
    export_format: str | None = None
    metadata_json: dict | None = None
    version: int | None = None


class ObservabilityReportResponse(OrmModel):
    id: UUID
    company_id: UUID
    branch_id: UUID | None = None
    report_code: str
    report_name: str
    description: str | None = None
    report_kind: str
    definition_json: dict | None = None
    last_generated_at: datetime | None = None
    export_format: str | None = None
    status: str
    metadata_json: dict | None = None
    version: int
    is_deleted: bool | None = None
