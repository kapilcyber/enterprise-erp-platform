"""AI runtime routers — session, conversation, messages, memory, context, invoke."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.ai.dependencies import get_db, require_permission
from modules.ai.routers._common import _app, register_lifecycle_route, register_standard_crud
from modules.ai.schemas import (
    ContextPackageCreate,
    ContextPackageResponse,
    ContextPackageUpdate,
    ConversationCreate,
    ConversationMemoryCreate,
    ConversationMemoryResponse,
    ConversationMemoryUpdate,
    ConversationMessageCreate,
    ConversationMessageResponse,
    ConversationMessageUpdate,
    ConversationResponse,
    ConversationUpdate,
    InvokeRequest,
    InvokeResponse,
    RuntimeResolveRequest,
    RuntimeResolveResponse,
    SessionCreate,
    SessionResponse,
    SessionUpdate,
)
from modules.foundation.domain.value_objects import TenantContext
from shared.schemas import APIResponse

sessions_router = APIRouter(prefix="/sessions", tags=["AI — Session"])
conversations_router = APIRouter(prefix="/conversations", tags=["AI — Conversation"])
conversation_messages_router = APIRouter(
    prefix="/conversation-messages", tags=["AI — Conversation Message"]
)
conversation_memories_router = APIRouter(
    prefix="/conversation-memories", tags=["AI — Conversation Memory"]
)
context_packages_router = APIRouter(prefix="/context-packages", tags=["AI — Context Package"])
runtime_router = APIRouter(prefix="/runtime", tags=["AI — Runtime"])
invoke_router = APIRouter(prefix="/invoke", tags=["AI — Invoke"])

register_standard_crud(
    sessions_router,
    resource="session",
    service_attr="sessions",
    create_schema=SessionCreate,
    update_schema=SessionUpdate,
    response_schema=SessionResponse,
    default_sort="opened_at",
    tag="AI — Session",
)
register_lifecycle_route(
    sessions_router,
    path="/{row_id}/close",
    resource="session",
    action="update",
    service_attr="sessions",
    method_name="close",
    response_schema=SessionResponse,
    tag="AI — Session",
    message="Closed",
)
register_lifecycle_route(
    sessions_router,
    path="/{row_id}/expire",
    resource="session",
    action="update",
    service_attr="sessions",
    method_name="expire",
    response_schema=SessionResponse,
    tag="AI — Session",
    message="Expired",
)

register_standard_crud(
    conversations_router,
    resource="conversation",
    service_attr="conversations",
    create_schema=ConversationCreate,
    update_schema=ConversationUpdate,
    response_schema=ConversationResponse,
    default_sort="conversation_code",
    tag="AI — Conversation",
)
register_lifecycle_route(
    conversations_router,
    path="/{row_id}/archive",
    resource="conversation",
    action="archive",
    service_attr="conversations",
    method_name="archive",
    response_schema=ConversationResponse,
    tag="AI — Conversation",
    message="Archived",
)

register_standard_crud(
    conversation_messages_router,
    resource="conversation_message",
    service_attr="conversation_messages",
    create_schema=ConversationMessageCreate,
    update_schema=ConversationMessageUpdate,
    response_schema=ConversationMessageResponse,
    default_sort="sequence_no",
    tag="AI — Conversation Message",
)

register_standard_crud(
    conversation_memories_router,
    resource="conversation_memory",
    service_attr="conversation_memories",
    create_schema=ConversationMemoryCreate,
    update_schema=ConversationMemoryUpdate,
    response_schema=ConversationMemoryResponse,
    default_sort="memory_code",
    tag="AI — Conversation Memory",
)
register_lifecycle_route(
    conversation_memories_router,
    path="/{row_id}/expire",
    resource="conversation_memory",
    action="update",
    service_attr="conversation_memories",
    method_name="expire",
    response_schema=ConversationMemoryResponse,
    tag="AI — Conversation Memory",
    message="Expired",
)
register_lifecycle_route(
    conversation_memories_router,
    path="/{row_id}/purge",
    resource="conversation_memory",
    action="delete",
    service_attr="conversation_memories",
    method_name="purge",
    response_schema=ConversationMemoryResponse,
    tag="AI — Conversation Memory",
    message="Purged",
)

register_standard_crud(
    context_packages_router,
    resource="context_package",
    service_attr="context_packages",
    create_schema=ContextPackageCreate,
    update_schema=ContextPackageUpdate,
    response_schema=ContextPackageResponse,
    default_sort="package_code",
    tag="AI — Context Package",
)


@runtime_router.post("/resolve", response_model=APIResponse[RuntimeResolveResponse])
def resolve_runtime(
    body: RuntimeResolveRequest,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.session:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=_app(db).runtime_resolve.resolve(ctx, **body.model_dump(exclude_none=True)),
    )


@invoke_router.post("", response_model=APIResponse[InvokeResponse])
def invoke_ai(
    body: InvokeRequest,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.invoke:invoke"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=_app(db).invoke.invoke(ctx, **body.model_dump(exclude_none=True)),
    )
