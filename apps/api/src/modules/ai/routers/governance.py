"""AI governance routers — gateway, routing, guardrail, moderation, rate-limit policies."""

from fastapi import APIRouter

from modules.ai.routers._common import register_lifecycle_route, register_standard_crud
from modules.ai.schemas import (
    GatewayPolicyCreate,
    GatewayPolicyResponse,
    GatewayPolicyUpdate,
    GuardrailPolicyCreate,
    GuardrailPolicyResponse,
    GuardrailPolicyUpdate,
    ModerationPolicyCreate,
    ModerationPolicyResponse,
    ModerationPolicyUpdate,
    PublishBody,
    RateLimitPolicyCreate,
    RateLimitPolicyResponse,
    RateLimitPolicyUpdate,
    RetireBody,
    RoutingRuleCreate,
    RoutingRuleResponse,
    RoutingRuleUpdate,
)

gateway_policies_router = APIRouter(prefix="/gateway-policies", tags=["AI — Gateway Policy"])
routing_rules_router = APIRouter(prefix="/routing-rules", tags=["AI — Routing Rule"])
guardrail_policies_router = APIRouter(prefix="/guardrail-policies", tags=["AI — Guardrail Policy"])
moderation_policies_router = APIRouter(
    prefix="/moderation-policies", tags=["AI — Moderation Policy"]
)
rate_limit_policies_router = APIRouter(
    prefix="/rate-limit-policies", tags=["AI — Rate Limit Policy"]
)

_POLICY_ENTITIES = (
    (
        gateway_policies_router,
        "gateway_policy",
        "gateway_policies",
        GatewayPolicyCreate,
        GatewayPolicyUpdate,
        GatewayPolicyResponse,
        "policy_name",
    ),
    (
        routing_rules_router,
        "routing_rule",
        "routing_rules",
        RoutingRuleCreate,
        RoutingRuleUpdate,
        RoutingRuleResponse,
        "priority",
    ),
    (
        guardrail_policies_router,
        "guardrail_policy",
        "guardrail_policies",
        GuardrailPolicyCreate,
        GuardrailPolicyUpdate,
        GuardrailPolicyResponse,
        "policy_name",
    ),
    (
        moderation_policies_router,
        "moderation_policy",
        "moderation_policies",
        ModerationPolicyCreate,
        ModerationPolicyUpdate,
        ModerationPolicyResponse,
        "policy_name",
    ),
    (
        rate_limit_policies_router,
        "rate_limit_policy",
        "rate_limit_policies",
        RateLimitPolicyCreate,
        RateLimitPolicyUpdate,
        RateLimitPolicyResponse,
        "policy_name",
    ),
)

for router, resource, service_attr, create_s, update_s, response_s, default_sort in _POLICY_ENTITIES:
    register_standard_crud(
        router,
        resource=resource,
        service_attr=service_attr,
        create_schema=create_s,
        update_schema=update_s,
        response_schema=response_s,
        default_sort=default_sort,
        tag=str(router.tags[0]),
    )
    register_lifecycle_route(
        router,
        path="/{row_id}/publish",
        resource=resource,
        action="publish",
        service_attr=service_attr,
        method_name="publish",
        response_schema=response_s,
        tag=str(router.tags[0]),
        body_schema=PublishBody,
        message="Published",
    )
    register_lifecycle_route(
        router,
        path="/{row_id}/retire",
        resource=resource,
        action="retire",
        service_attr=service_attr,
        method_name="retire",
        response_schema=response_s,
        tag=str(router.tags[0]),
        body_schema=RetireBody,
        message="Retired",
    )
