"""Monitoring Phase 3 SLO/SLI · dashboard · bindings · correlation routers."""

from fastapi import APIRouter

from modules.monitoring.routers._common import register_lifecycle_route, register_standard_crud
from modules.monitoring.schemas import (
    DashboardDefinitionCreate,
    DashboardDefinitionResponse,
    DashboardDefinitionUpdate,
    ExternalPlatformBindingCreate,
    ExternalPlatformBindingResponse,
    ExternalPlatformBindingUpdate,
    LifecycleReason,
    ServicePlatformAssignmentCreate,
    ServicePlatformAssignmentResponse,
    ServicePlatformAssignmentUpdate,
    SignalCorrelationCreate,
    SignalCorrelationResponse,
    SignalCorrelationUpdate,
    SliDefinitionCreate,
    SliDefinitionResponse,
    SliDefinitionUpdate,
    SloDefinitionCreate,
    SloDefinitionResponse,
    SloDefinitionUpdate,
)

slo_definitions_router = APIRouter(
    prefix="/slo-definitions",
    tags=["Monitoring — SLO Definition"],
)
sli_definitions_router = APIRouter(
    prefix="/sli-definitions",
    tags=["Monitoring — SLI Definition"],
)
dashboard_definitions_router = APIRouter(
    prefix="/dashboard-definitions",
    tags=["Monitoring — Dashboard Definition"],
)
external_platform_bindings_router = APIRouter(
    prefix="/external-platform-bindings",
    tags=["Monitoring — External Platform Binding"],
)
service_platform_assignments_router = APIRouter(
    prefix="/service-platform-assignments",
    tags=["Monitoring — Service Platform Assignment"],
)
signal_correlations_router = APIRouter(
    prefix="/signal-correlations",
    tags=["Monitoring — Signal Correlation"],
)

register_standard_crud(
    slo_definitions_router,
    resource="slo_definition",
    service_attr="slo_definitions",
    create_schema=SloDefinitionCreate,
    update_schema=SloDefinitionUpdate,
    response_schema=SloDefinitionResponse,
    default_sort="slo_name",
    tag="Monitoring — SLO Definition",
)
register_lifecycle_route(
    slo_definitions_router,
    path="/{row_id}/publish",
    resource="slo_definition",
    action="publish",
    service_attr="slo_definitions",
    method_name="publish",
    response_schema=SloDefinitionResponse,
    tag="Monitoring — SLO Definition",
    message="Published",
)
register_lifecycle_route(
    slo_definitions_router,
    path="/{row_id}/retire",
    resource="slo_definition",
    action="retire",
    service_attr="slo_definitions",
    method_name="retire",
    response_schema=SloDefinitionResponse,
    tag="Monitoring — SLO Definition",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    sli_definitions_router,
    resource="sli_definition",
    service_attr="sli_definitions",
    create_schema=SliDefinitionCreate,
    update_schema=SliDefinitionUpdate,
    response_schema=SliDefinitionResponse,
    default_sort="sli_name",
    tag="Monitoring — SLI Definition",
)
register_lifecycle_route(
    sli_definitions_router,
    path="/{row_id}/publish",
    resource="sli_definition",
    action="publish",
    service_attr="sli_definitions",
    method_name="publish",
    response_schema=SliDefinitionResponse,
    tag="Monitoring — SLI Definition",
    message="Published",
)
register_lifecycle_route(
    sli_definitions_router,
    path="/{row_id}/retire",
    resource="sli_definition",
    action="retire",
    service_attr="sli_definitions",
    method_name="retire",
    response_schema=SliDefinitionResponse,
    tag="Monitoring — SLI Definition",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    dashboard_definitions_router,
    resource="dashboard_definition",
    service_attr="dashboard_definitions",
    create_schema=DashboardDefinitionCreate,
    update_schema=DashboardDefinitionUpdate,
    response_schema=DashboardDefinitionResponse,
    default_sort="dashboard_name",
    tag="Monitoring — Dashboard Definition",
)
register_lifecycle_route(
    dashboard_definitions_router,
    path="/{row_id}/publish",
    resource="dashboard_definition",
    action="publish",
    service_attr="dashboard_definitions",
    method_name="publish",
    response_schema=DashboardDefinitionResponse,
    tag="Monitoring — Dashboard Definition",
    message="Published",
)
register_lifecycle_route(
    dashboard_definitions_router,
    path="/{row_id}/retire",
    resource="dashboard_definition",
    action="retire",
    service_attr="dashboard_definitions",
    method_name="retire",
    response_schema=DashboardDefinitionResponse,
    tag="Monitoring — Dashboard Definition",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    external_platform_bindings_router,
    resource="external_platform_binding",
    service_attr="external_platform_bindings",
    create_schema=ExternalPlatformBindingCreate,
    update_schema=ExternalPlatformBindingUpdate,
    response_schema=ExternalPlatformBindingResponse,
    default_sort="binding_name",
    tag="Monitoring — External Platform Binding",
)
register_lifecycle_route(
    external_platform_bindings_router,
    path="/{row_id}/activate",
    resource="external_platform_binding",
    action="activate",
    service_attr="external_platform_bindings",
    method_name="activate",
    response_schema=ExternalPlatformBindingResponse,
    tag="Monitoring — External Platform Binding",
    message="Activated",
)
register_lifecycle_route(
    external_platform_bindings_router,
    path="/{row_id}/retire",
    resource="external_platform_binding",
    action="retire",
    service_attr="external_platform_bindings",
    method_name="retire",
    response_schema=ExternalPlatformBindingResponse,
    tag="Monitoring — External Platform Binding",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    service_platform_assignments_router,
    resource="service_platform_assignment",
    service_attr="service_platform_assignments",
    create_schema=ServicePlatformAssignmentCreate,
    update_schema=ServicePlatformAssignmentUpdate,
    response_schema=ServicePlatformAssignmentResponse,
    default_sort="created_at",
    tag="Monitoring — Service Platform Assignment",
)
for path, action, method_name, message in (
    ("/{row_id}/activate", "activate", "activate", "Activated"),
    ("/{row_id}/deactivate", "deactivate", "deactivate", "Deactivated"),
):
    register_lifecycle_route(
        service_platform_assignments_router,
        path=path,
        resource="service_platform_assignment",
        action=action,
        service_attr="service_platform_assignments",
        method_name=method_name,
        response_schema=ServicePlatformAssignmentResponse,
        tag="Monitoring — Service Platform Assignment",
        message=message,
    )
register_lifecycle_route(
    service_platform_assignments_router,
    path="/{row_id}/retire",
    resource="service_platform_assignment",
    action="retire",
    service_attr="service_platform_assignments",
    method_name="retire",
    response_schema=ServicePlatformAssignmentResponse,
    tag="Monitoring — Service Platform Assignment",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    signal_correlations_router,
    resource="signal_correlation",
    service_attr="signal_correlations",
    create_schema=SignalCorrelationCreate,
    update_schema=SignalCorrelationUpdate,
    response_schema=SignalCorrelationResponse,
    default_sort="correlation_name",
    tag="Monitoring — Signal Correlation",
)
register_lifecycle_route(
    signal_correlations_router,
    path="/{row_id}/activate",
    resource="signal_correlation",
    action="activate",
    service_attr="signal_correlations",
    method_name="activate",
    response_schema=SignalCorrelationResponse,
    tag="Monitoring — Signal Correlation",
    message="Activated",
)
register_lifecycle_route(
    signal_correlations_router,
    path="/{row_id}/retire",
    resource="signal_correlation",
    action="retire",
    service_attr="signal_correlations",
    method_name="retire",
    response_schema=SignalCorrelationResponse,
    tag="Monitoring — Signal Correlation",
    body_schema=LifecycleReason,
    message="Retired",
)
