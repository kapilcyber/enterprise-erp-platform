"""Monitoring Phase 2 log/trace · alert · routing routers."""

from fastapi import APIRouter

from modules.monitoring.routers._common import register_lifecycle_route, register_standard_crud
from modules.monitoring.schemas import (
    AlertRoutingPolicyCreate,
    AlertRoutingPolicyResponse,
    AlertRoutingPolicyUpdate,
    AlertRuleCreate,
    AlertRuleResponse,
    AlertRuleUpdate,
    LifecycleReason,
    LogTracePolicyCreate,
    LogTracePolicyResponse,
    LogTracePolicyUpdate,
)

log_trace_policies_router = APIRouter(
    prefix="/log-trace-policies",
    tags=["Monitoring — Log Trace Policy"],
)
alert_rules_router = APIRouter(
    prefix="/alert-rules",
    tags=["Monitoring — Alert Rule"],
)
alert_routing_policies_router = APIRouter(
    prefix="/alert-routing-policies",
    tags=["Monitoring — Alert Routing Policy"],
)

register_standard_crud(
    log_trace_policies_router,
    resource="log_trace_policy",
    service_attr="log_trace_policies",
    create_schema=LogTracePolicyCreate,
    update_schema=LogTracePolicyUpdate,
    response_schema=LogTracePolicyResponse,
    default_sort="policy_name",
    tag="Monitoring — Log Trace Policy",
)
register_lifecycle_route(
    log_trace_policies_router,
    path="/{row_id}/publish",
    resource="log_trace_policy",
    action="publish",
    service_attr="log_trace_policies",
    method_name="publish",
    response_schema=LogTracePolicyResponse,
    tag="Monitoring — Log Trace Policy",
    message="Published",
)
register_lifecycle_route(
    log_trace_policies_router,
    path="/{row_id}/retire",
    resource="log_trace_policy",
    action="retire",
    service_attr="log_trace_policies",
    method_name="retire",
    response_schema=LogTracePolicyResponse,
    tag="Monitoring — Log Trace Policy",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    alert_rules_router,
    resource="alert_rule",
    service_attr="alert_rules",
    create_schema=AlertRuleCreate,
    update_schema=AlertRuleUpdate,
    response_schema=AlertRuleResponse,
    default_sort="rule_name",
    tag="Monitoring — Alert Rule",
)
register_lifecycle_route(
    alert_rules_router,
    path="/{row_id}/publish",
    resource="alert_rule",
    action="publish",
    service_attr="alert_rules",
    method_name="publish",
    response_schema=AlertRuleResponse,
    tag="Monitoring — Alert Rule",
    message="Published",
)
register_lifecycle_route(
    alert_rules_router,
    path="/{row_id}/retire",
    resource="alert_rule",
    action="retire",
    service_attr="alert_rules",
    method_name="retire",
    response_schema=AlertRuleResponse,
    tag="Monitoring — Alert Rule",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    alert_routing_policies_router,
    resource="alert_routing_policy",
    service_attr="alert_routing_policies",
    create_schema=AlertRoutingPolicyCreate,
    update_schema=AlertRoutingPolicyUpdate,
    response_schema=AlertRoutingPolicyResponse,
    default_sort="routing_name",
    tag="Monitoring — Alert Routing Policy",
)
register_lifecycle_route(
    alert_routing_policies_router,
    path="/{row_id}/publish",
    resource="alert_routing_policy",
    action="publish",
    service_attr="alert_routing_policies",
    method_name="publish",
    response_schema=AlertRoutingPolicyResponse,
    tag="Monitoring — Alert Routing Policy",
    message="Published",
)
register_lifecycle_route(
    alert_routing_policies_router,
    path="/{row_id}/retire",
    resource="alert_routing_policy",
    action="retire",
    service_attr="alert_routing_policies",
    method_name="retire",
    response_schema=AlertRoutingPolicyResponse,
    tag="Monitoring — Alert Routing Policy",
    body_schema=LifecycleReason,
    message="Retired",
)
