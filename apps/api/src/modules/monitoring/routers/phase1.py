"""Monitoring Phase 1 policy / registry / signal / reliability routers."""

from fastapi import APIRouter

from modules.monitoring.routers._common import register_lifecycle_route, register_standard_crud
from modules.monitoring.schemas import (
    HealthCheckCreate,
    HealthCheckResponse,
    HealthCheckUpdate,
    LifecycleReason,
    MetricDefinitionCreate,
    MetricDefinitionResponse,
    MetricDefinitionUpdate,
    MonitoredComponentCreate,
    MonitoredComponentResponse,
    MonitoredComponentUpdate,
    MonitoredServiceCreate,
    MonitoredServiceResponse,
    MonitoredServiceUpdate,
    ObservabilityPolicyCreate,
    ObservabilityPolicyResponse,
    ObservabilityPolicyUpdate,
    ObservabilityPolicyVersionCreate,
    ObservabilityPolicyVersionResponse,
    ObservabilityPolicyVersionUpdate,
    ServicePolicyAssignmentCreate,
    ServicePolicyAssignmentResponse,
    ServicePolicyAssignmentUpdate,
)

policies_router = APIRouter(
    prefix="/policies",
    tags=["Monitoring — Observability Policy"],
)
policy_versions_router = APIRouter(
    prefix="/policy-versions",
    tags=["Monitoring — Observability Policy Version"],
)
services_router = APIRouter(
    prefix="/services",
    tags=["Monitoring — Monitored Service"],
)
components_router = APIRouter(
    prefix="/components",
    tags=["Monitoring — Monitored Component"],
)
metric_definitions_router = APIRouter(
    prefix="/metric-definitions",
    tags=["Monitoring — Metric Definition"],
)
health_checks_router = APIRouter(
    prefix="/health-checks",
    tags=["Monitoring — Health Check"],
)
service_policy_assignments_router = APIRouter(
    prefix="/service-policy-assignments",
    tags=["Monitoring — Service Policy Assignment"],
)

register_standard_crud(
    policies_router,
    resource="observability_policy",
    service_attr="observability_policies",
    create_schema=ObservabilityPolicyCreate,
    update_schema=ObservabilityPolicyUpdate,
    response_schema=ObservabilityPolicyResponse,
    default_sort="policy_name",
    tag="Monitoring — Observability Policy",
)

register_standard_crud(
    policy_versions_router,
    resource="observability_policy_version",
    service_attr="observability_policy_versions",
    create_schema=ObservabilityPolicyVersionCreate,
    update_schema=ObservabilityPolicyVersionUpdate,
    response_schema=ObservabilityPolicyVersionResponse,
    default_sort="version_label",
    tag="Monitoring — Observability Policy Version",
)
register_lifecycle_route(
    policy_versions_router,
    path="/{row_id}/publish",
    resource="observability_policy_version",
    action="publish",
    service_attr="observability_policy_versions",
    method_name="publish",
    response_schema=ObservabilityPolicyVersionResponse,
    tag="Monitoring — Observability Policy Version",
    message="Published",
)
register_lifecycle_route(
    policy_versions_router,
    path="/{row_id}/retire",
    resource="observability_policy_version",
    action="retire",
    service_attr="observability_policy_versions",
    method_name="retire",
    response_schema=ObservabilityPolicyVersionResponse,
    tag="Monitoring — Observability Policy Version",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    services_router,
    resource="monitored_service",
    service_attr="monitored_services",
    create_schema=MonitoredServiceCreate,
    update_schema=MonitoredServiceUpdate,
    response_schema=MonitoredServiceResponse,
    default_sort="service_name",
    tag="Monitoring — Monitored Service",
)

register_standard_crud(
    components_router,
    resource="monitored_component",
    service_attr="monitored_components",
    create_schema=MonitoredComponentCreate,
    update_schema=MonitoredComponentUpdate,
    response_schema=MonitoredComponentResponse,
    default_sort="component_name",
    tag="Monitoring — Monitored Component",
)

register_standard_crud(
    metric_definitions_router,
    resource="metric_definition",
    service_attr="metric_definitions",
    create_schema=MetricDefinitionCreate,
    update_schema=MetricDefinitionUpdate,
    response_schema=MetricDefinitionResponse,
    default_sort="metric_name",
    tag="Monitoring — Metric Definition",
)
register_lifecycle_route(
    metric_definitions_router,
    path="/{row_id}/publish",
    resource="metric_definition",
    action="publish",
    service_attr="metric_definitions",
    method_name="publish",
    response_schema=MetricDefinitionResponse,
    tag="Monitoring — Metric Definition",
    message="Published",
)
register_lifecycle_route(
    metric_definitions_router,
    path="/{row_id}/retire",
    resource="metric_definition",
    action="retire",
    service_attr="metric_definitions",
    method_name="retire",
    response_schema=MetricDefinitionResponse,
    tag="Monitoring — Metric Definition",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    health_checks_router,
    resource="health_check",
    service_attr="health_checks",
    create_schema=HealthCheckCreate,
    update_schema=HealthCheckUpdate,
    response_schema=HealthCheckResponse,
    default_sort="check_name",
    tag="Monitoring — Health Check",
)

register_standard_crud(
    service_policy_assignments_router,
    resource="service_policy_assignment",
    service_attr="service_policy_assignments",
    create_schema=ServicePolicyAssignmentCreate,
    update_schema=ServicePolicyAssignmentUpdate,
    response_schema=ServicePolicyAssignmentResponse,
    default_sort="created_at",
    tag="Monitoring — Service Policy Assignment",
)
for path, action, method, msg in (
    ("/{row_id}/activate", "activate", "activate", "Activated"),
    ("/{row_id}/deactivate", "deactivate", "deactivate", "Deactivated"),
):
    register_lifecycle_route(
        service_policy_assignments_router,
        path=path,
        resource="service_policy_assignment",
        action=action,
        service_attr="service_policy_assignments",
        method_name=method,
        response_schema=ServicePolicyAssignmentResponse,
        tag="Monitoring — Service Policy Assignment",
        message=msg,
    )
register_lifecycle_route(
    service_policy_assignments_router,
    path="/{row_id}/retire",
    resource="service_policy_assignment",
    action="retire",
    service_attr="service_policy_assignments",
    method_name="retire",
    response_schema=ServicePolicyAssignmentResponse,
    tag="Monitoring — Service Policy Assignment",
    body_schema=LifecycleReason,
    message="Retired",
)
