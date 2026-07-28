"""Developer Portal Phase 2 access-governance routers."""

from fastapi import APIRouter

from modules.devportal.routers._common import register_lifecycle_route, register_standard_crud
from modules.devportal.schemas import (
    EntitlementCreate,
    EntitlementResponse,
    EntitlementUpdate,
    LifecycleReason,
    PlanCreate,
    PlanResponse,
    PlanUpdate,
    PublishValidationResponse,
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionUpdate,
)

plans_router = APIRouter(prefix="/plans", tags=["DevPortal — Plan"])
subscriptions_router = APIRouter(prefix="/subscriptions", tags=["DevPortal — Subscription"])
entitlements_router = APIRouter(prefix="/entitlements", tags=["DevPortal — Entitlement"])

register_standard_crud(
    plans_router,
    resource="plan",
    service_attr="plans",
    create_schema=PlanCreate,
    update_schema=PlanUpdate,
    response_schema=PlanResponse,
    default_sort="plan_name",
    tag="DevPortal — Plan",
)
register_lifecycle_route(
    plans_router,
    path="/{row_id}/validate-publish",
    resource="plan",
    action="validate",
    service_attr="plans",
    method_name="validate_publish",
    response_schema=PublishValidationResponse,
    tag="DevPortal — Plan",
    message="Validated",
)
register_lifecycle_route(
    plans_router,
    path="/{row_id}/publish",
    resource="plan",
    action="publish",
    service_attr="plans",
    method_name="publish",
    response_schema=PlanResponse,
    tag="DevPortal — Plan",
    message="Published",
)
register_lifecycle_route(
    plans_router,
    path="/{row_id}/retire",
    resource="plan",
    action="retire",
    service_attr="plans",
    method_name="retire",
    response_schema=PlanResponse,
    tag="DevPortal — Plan",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    subscriptions_router,
    resource="subscription",
    service_attr="subscriptions",
    create_schema=SubscriptionCreate,
    update_schema=SubscriptionUpdate,
    response_schema=SubscriptionResponse,
    default_sort="created_at",
    tag="DevPortal — Subscription",
)
for path, action, method, msg in (
    ("/{row_id}/submit", "submit", "submit", "Submitted"),
    ("/{row_id}/approve", "approve", "approve", "Approved"),
    ("/{row_id}/activate", "activate", "activate", "Activated"),
    ("/{row_id}/suspend", "suspend", "suspend", "Suspended"),
):
    register_lifecycle_route(
        subscriptions_router,
        path=path,
        resource="subscription",
        action=action,
        service_attr="subscriptions",
        method_name=method,
        response_schema=SubscriptionResponse,
        tag="DevPortal — Subscription",
        message=msg,
    )
register_lifecycle_route(
    subscriptions_router,
    path="/{row_id}/retire",
    resource="subscription",
    action="retire",
    service_attr="subscriptions",
    method_name="retire",
    response_schema=SubscriptionResponse,
    tag="DevPortal — Subscription",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    entitlements_router,
    resource="entitlement",
    service_attr="entitlements",
    create_schema=EntitlementCreate,
    update_schema=EntitlementUpdate,
    response_schema=EntitlementResponse,
    default_sort="scope_code",
    tag="DevPortal — Entitlement",
)
for path, action, method, msg in (
    ("/{row_id}/activate", "activate", "activate", "Activated"),
    ("/{row_id}/suspend", "suspend", "suspend", "Suspended"),
):
    register_lifecycle_route(
        entitlements_router,
        path=path,
        resource="entitlement",
        action=action,
        service_attr="entitlements",
        method_name=method,
        response_schema=EntitlementResponse,
        tag="DevPortal — Entitlement",
        message=msg,
    )
register_lifecycle_route(
    entitlements_router,
    path="/{row_id}/retire",
    resource="entitlement",
    action="retire",
    service_attr="entitlements",
    method_name="retire",
    response_schema=EntitlementResponse,
    tag="DevPortal — Entitlement",
    body_schema=LifecycleReason,
    message="Retired",
)
