"""Developer Portal Phase 4 portal operations routers."""

from fastapi import APIRouter

from modules.devportal.routers._common import register_lifecycle_route, register_standard_crud
from modules.devportal.schemas import (
    LifecycleReason,
    PortalReportCreate,
    PortalReportResponse,
    PortalReportUpdate,
)

reports_router = APIRouter(prefix="/reports", tags=["DevPortal — Reports"])

register_standard_crud(
    reports_router,
    resource="report",
    service_attr="reports",
    create_schema=PortalReportCreate,
    update_schema=PortalReportUpdate,
    response_schema=PortalReportResponse,
    default_sort="report_name",
    tag="DevPortal — Reports",
)
register_lifecycle_route(
    reports_router,
    path="/{row_id}/finalize",
    resource="report",
    action="finalize",
    service_attr="reports",
    method_name="finalize",
    response_schema=PortalReportResponse,
    tag="DevPortal — Reports",
    message="Finalized",
)
register_lifecycle_route(
    reports_router,
    path="/{row_id}/export",
    resource="report",
    action="export",
    service_attr="reports",
    method_name="export",
    response_schema=PortalReportResponse,
    tag="DevPortal — Reports",
    message="Exported",
)
register_lifecycle_route(
    reports_router,
    path="/{row_id}/retire",
    resource="report",
    action="retire",
    service_attr="reports",
    method_name="retire",
    response_schema=PortalReportResponse,
    tag="DevPortal — Reports",
    body_schema=LifecycleReason,
    message="Retired",
)
