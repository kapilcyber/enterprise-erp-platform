"""Developer Portal Phase 1 application + catalog routers."""

from fastapi import APIRouter

from modules.devportal.routers._common import register_lifecycle_route, register_standard_crud
from modules.devportal.schemas import (
    ApiProductCreate,
    ApiProductEnvironmentCreate,
    ApiProductEnvironmentResponse,
    ApiProductEnvironmentUpdate,
    ApiProductResponse,
    ApiProductUpdate,
    ApiProductVersionCreate,
    ApiProductVersionResponse,
    ApiProductVersionUpdate,
    ApplicationBindHub,
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
    LifecycleReason,
    PublishValidationResponse,
)

applications_router = APIRouter(prefix="/applications", tags=["DevPortal — Application"])
api_products_router = APIRouter(prefix="/api-products", tags=["DevPortal — API Product"])
api_product_versions_router = APIRouter(
    prefix="/api-product-versions", tags=["DevPortal — API Product Version"]
)
api_product_environments_router = APIRouter(
    prefix="/api-product-environments", tags=["DevPortal — API Product Environment"]
)

register_standard_crud(
    applications_router,
    resource="application",
    service_attr="applications",
    create_schema=ApplicationCreate,
    update_schema=ApplicationUpdate,
    response_schema=ApplicationResponse,
    default_sort="application_name",
    tag="DevPortal — Application",
)
for path, action, method, msg in (
    ("/{row_id}/submit", "submit", "submit", "Submitted"),
    ("/{row_id}/approve", "approve", "approve", "Approved"),
    ("/{row_id}/activate", "activate", "activate", "Activated"),
    ("/{row_id}/suspend", "suspend", "suspend", "Suspended"),
):
    register_lifecycle_route(
        applications_router,
        path=path,
        resource="application",
        action=action,
        service_attr="applications",
        method_name=method,
        response_schema=ApplicationResponse,
        tag="DevPortal — Application",
        message=msg,
    )
register_lifecycle_route(
    applications_router,
    path="/{row_id}/retire",
    resource="application",
    action="retire",
    service_attr="applications",
    method_name="retire",
    response_schema=ApplicationResponse,
    tag="DevPortal — Application",
    body_schema=LifecycleReason,
    message="Retired",
)
register_lifecycle_route(
    applications_router,
    path="/{row_id}/bind-hub",
    resource="application",
    action="bind",
    service_attr="applications",
    method_name="bind_hub_refs",
    response_schema=ApplicationResponse,
    tag="DevPortal — Application",
    body_schema=ApplicationBindHub,
    message="Hub Bound",
)

register_standard_crud(
    api_products_router,
    resource="api_product",
    service_attr="api_products",
    create_schema=ApiProductCreate,
    update_schema=ApiProductUpdate,
    response_schema=ApiProductResponse,
    default_sort="product_name",
    tag="DevPortal — API Product",
)

register_standard_crud(
    api_product_versions_router,
    resource="api_product_version",
    service_attr="api_product_versions",
    create_schema=ApiProductVersionCreate,
    update_schema=ApiProductVersionUpdate,
    response_schema=ApiProductVersionResponse,
    default_sort="version_label",
    tag="DevPortal — API Product Version",
)
register_lifecycle_route(
    api_product_versions_router,
    path="/{row_id}/validate-publish",
    resource="api_product_version",
    action="validate",
    service_attr="api_product_versions",
    method_name="validate_publish",
    response_schema=PublishValidationResponse,
    tag="DevPortal — API Product Version",
    message="Validated",
)
register_lifecycle_route(
    api_product_versions_router,
    path="/{row_id}/publish",
    resource="api_product_version",
    action="publish",
    service_attr="api_product_versions",
    method_name="publish",
    response_schema=ApiProductVersionResponse,
    tag="DevPortal — API Product Version",
    message="Published",
)
register_lifecycle_route(
    api_product_versions_router,
    path="/{row_id}/retire",
    resource="api_product_version",
    action="retire",
    service_attr="api_product_versions",
    method_name="retire",
    response_schema=ApiProductVersionResponse,
    tag="DevPortal — API Product Version",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    api_product_environments_router,
    resource="api_product_environment",
    service_attr="api_product_environments",
    create_schema=ApiProductEnvironmentCreate,
    update_schema=ApiProductEnvironmentUpdate,
    response_schema=ApiProductEnvironmentResponse,
    default_sort="environment_name",
    tag="DevPortal — API Product Environment",
)
