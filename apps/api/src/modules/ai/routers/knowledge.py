"""AI knowledge & RAG metadata routers — Phase 2."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.ai.dependencies import get_db, require_permission
from modules.ai.routers._common import register_lifecycle_route, register_standard_crud
from modules.ai.schemas import (
    EmbeddingCreate,
    EmbeddingResponse,
    EmbeddingUpdate,
    IngestionEnqueueBody,
    KnowledgeBaseCreate,
    KnowledgeBaseResponse,
    KnowledgeBaseUpdate,
    KnowledgeChunkCreate,
    KnowledgeChunkResponse,
    KnowledgeChunkUpdate,
    KnowledgeSourceCreate,
    KnowledgeSourceResponse,
    KnowledgeSourceUpdate,
    PublishBody,
    RetireBody,
    VectorIndexCreate,
    VectorIndexResponse,
    VectorIndexUpdate,
)
from modules.ai.service.application_service import AiApplicationService
from modules.foundation.domain.value_objects import TenantContext
from shared.schemas import APIResponse

knowledge_bases_router = APIRouter(prefix="/knowledge-bases", tags=["AI — Knowledge Base"])
knowledge_sources_router = APIRouter(prefix="/knowledge-sources", tags=["AI — Knowledge Source"])
knowledge_chunks_router = APIRouter(prefix="/knowledge-chunks", tags=["AI — Knowledge Chunk"])
embeddings_router = APIRouter(prefix="/embeddings", tags=["AI — Embedding"])
vector_indexes_router = APIRouter(prefix="/vector-indexes", tags=["AI — Vector Index"])


def _app(db: Session) -> AiApplicationService:
    return AiApplicationService(db)


register_standard_crud(
    knowledge_bases_router,
    resource="knowledge_base",
    service_attr="knowledge_bases",
    create_schema=KnowledgeBaseCreate,
    update_schema=KnowledgeBaseUpdate,
    response_schema=KnowledgeBaseResponse,
    default_sort="knowledge_base_name",
    tag="AI — Knowledge Base",
)
register_lifecycle_route(
    knowledge_bases_router,
    path="/{row_id}/publish",
    resource="knowledge_base",
    action="publish",
    service_attr="knowledge_bases",
    method_name="publish",
    response_schema=KnowledgeBaseResponse,
    tag="AI — Knowledge Base",
    body_schema=PublishBody,
    message="Published",
)
register_lifecycle_route(
    knowledge_bases_router,
    path="/{row_id}/retire",
    resource="knowledge_base",
    action="retire",
    service_attr="knowledge_bases",
    method_name="retire",
    response_schema=KnowledgeBaseResponse,
    tag="AI — Knowledge Base",
    body_schema=RetireBody,
    message="Retired",
)


@knowledge_bases_router.post(
    "/{row_id}/ingestion/enqueue",
    response_model=APIResponse[dict],
    tags=["AI — Knowledge Base"],
)
def enqueue_ingestion(
    row_id: UUID,
    body: IngestionEnqueueBody,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.knowledge_base:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    svc = _app(db).knowledge_ingestion
    return APIResponse(
        message="Ingestion enqueued",
        data=svc.enqueue_metadata_ingestion(ctx, row_id, model_id=body.model_id),
    )


register_standard_crud(
    knowledge_sources_router,
    resource="knowledge_source",
    service_attr="knowledge_sources",
    create_schema=KnowledgeSourceCreate,
    update_schema=KnowledgeSourceUpdate,
    response_schema=KnowledgeSourceResponse,
    default_sort="source_code",
    tag="AI — Knowledge Source",
)
register_lifecycle_route(
    knowledge_sources_router,
    path="/{row_id}/activate",
    resource="knowledge_source",
    action="update",
    service_attr="knowledge_sources",
    method_name="activate",
    response_schema=KnowledgeSourceResponse,
    tag="AI — Knowledge Source",
    message="Activated",
)
register_lifecycle_route(
    knowledge_sources_router,
    path="/{row_id}/suspend",
    resource="knowledge_source",
    action="suspend",
    service_attr="knowledge_sources",
    method_name="suspend",
    response_schema=KnowledgeSourceResponse,
    tag="AI — Knowledge Source",
    message="Suspended",
)
register_lifecycle_route(
    knowledge_sources_router,
    path="/{row_id}/retire",
    resource="knowledge_source",
    action="update",
    service_attr="knowledge_sources",
    method_name="retire",
    response_schema=KnowledgeSourceResponse,
    tag="AI — Knowledge Source",
    message="Retired",
)

register_standard_crud(
    knowledge_chunks_router,
    resource="knowledge_chunk",
    service_attr="knowledge_chunks",
    create_schema=KnowledgeChunkCreate,
    update_schema=KnowledgeChunkUpdate,
    response_schema=KnowledgeChunkResponse,
    default_sort="sequence_no",
    tag="AI — Knowledge Chunk",
)
register_lifecycle_route(
    knowledge_chunks_router,
    path="/{row_id}/invalidate",
    resource="knowledge_chunk",
    action="invalidate",
    service_attr="knowledge_chunks",
    method_name="invalidate",
    response_schema=KnowledgeChunkResponse,
    tag="AI — Knowledge Chunk",
    message="Invalidated",
)

register_standard_crud(
    embeddings_router,
    resource="embedding",
    service_attr="embeddings",
    create_schema=EmbeddingCreate,
    update_schema=EmbeddingUpdate,
    response_schema=EmbeddingResponse,
    default_sort="embedding_code",
    tag="AI — Embedding",
)
register_lifecycle_route(
    embeddings_router,
    path="/{row_id}/rebuild",
    resource="embedding",
    action="rebuild",
    service_attr="embeddings",
    method_name="rebuild",
    response_schema=EmbeddingResponse,
    tag="AI — Embedding",
    message="Rebuilt",
)
register_lifecycle_route(
    embeddings_router,
    path="/{row_id}/invalidate",
    resource="embedding",
    action="invalidate",
    service_attr="embeddings",
    method_name="invalidate",
    response_schema=EmbeddingResponse,
    tag="AI — Embedding",
    message="Invalidated",
)

register_standard_crud(
    vector_indexes_router,
    resource="vector_index",
    service_attr="vector_indexes",
    create_schema=VectorIndexCreate,
    update_schema=VectorIndexUpdate,
    response_schema=VectorIndexResponse,
    default_sort="index_code",
    tag="AI — Vector Index",
)
register_lifecycle_route(
    vector_indexes_router,
    path="/{row_id}/rebuild",
    resource="vector_index",
    action="rebuild",
    service_attr="vector_indexes",
    method_name="rebuild",
    response_schema=VectorIndexResponse,
    tag="AI — Vector Index",
    message="Rebuild started",
)
register_lifecycle_route(
    vector_indexes_router,
    path="/{row_id}/activate",
    resource="vector_index",
    action="update",
    service_attr="vector_indexes",
    method_name="activate",
    response_schema=VectorIndexResponse,
    tag="AI — Vector Index",
    message="Activated",
)
register_lifecycle_route(
    vector_indexes_router,
    path="/{row_id}/retire",
    resource="vector_index",
    action="retire",
    service_attr="vector_indexes",
    method_name="retire",
    response_schema=VectorIndexResponse,
    tag="AI — Vector Index",
    message="Retired",
)
