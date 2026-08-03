"""Monitoring Phase 4 observability report router."""

from fastapi import APIRouter

from modules.monitoring.routers._common import register_lifecycle_route, register_standard_crud
from modules.monitoring.schemas import (
    LifecycleReason,
    ObservabilityReportCreate,
    ObservabilityReportResponse,
    ObservabilityReportUpdate,
)

observability_reports_router = APIRouter(
    prefix="/observability-reports",
    tags=["Monitoring — Observability Report"],
)

register_standard_crud(
    observability_reports_router,
    resource="observability_report",
    service_attr="observability_reports",
    create_schema=ObservabilityReportCreate,
    update_schema=ObservabilityReportUpdate,
    response_schema=ObservabilityReportResponse,
    default_sort="report_name",
    tag="Monitoring — Observability Report",
)
register_lifecycle_route(
    observability_reports_router,
    path="/{row_id}/activate",
    resource="observability_report",
    action="activate",
    service_attr="observability_reports",
    method_name="activate",
    response_schema=ObservabilityReportResponse,
    tag="Monitoring — Observability Report",
    message="Activated",
)
register_lifecycle_route(
    observability_reports_router,
    path="/{row_id}/mark-archived",
    resource="observability_report",
    action="mark_archived",
    service_attr="observability_reports",
    method_name="mark_archived",
    response_schema=ObservabilityReportResponse,
    tag="Monitoring — Observability Report",
    body_schema=LifecycleReason,
    message="Marked archived",
)
