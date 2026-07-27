"""AI assistant routers."""

from fastapi import APIRouter

from modules.ai.routers._common import register_lifecycle_route, register_standard_crud
from modules.ai.schemas import (
    AssistantCreate,
    AssistantResponse,
    AssistantUpdate,
    PublishBody,
    RetireBody,
)

assistants_router = APIRouter(prefix="/assistants", tags=["AI — Assistant"])

register_standard_crud(
    assistants_router,
    resource="assistant",
    service_attr="assistants",
    create_schema=AssistantCreate,
    update_schema=AssistantUpdate,
    response_schema=AssistantResponse,
    default_sort="assistant_name",
    tag="AI — Assistant",
)
register_lifecycle_route(
    assistants_router,
    path="/{row_id}/publish",
    resource="assistant",
    action="publish",
    service_attr="assistants",
    method_name="publish",
    response_schema=AssistantResponse,
    tag="AI — Assistant",
    body_schema=PublishBody,
    message="Published",
)
register_lifecycle_route(
    assistants_router,
    path="/{row_id}/retire",
    resource="assistant",
    action="retire",
    service_attr="assistants",
    method_name="retire",
    response_schema=AssistantResponse,
    tag="AI — Assistant",
    body_schema=RetireBody,
    message="Retired",
)
