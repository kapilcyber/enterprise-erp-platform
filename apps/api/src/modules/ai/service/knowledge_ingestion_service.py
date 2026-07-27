"""Knowledge ingestion orchestration — metadata stubs only, no provider SDK."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import (
    EmbeddingStatus,
    KnowledgeChunkStatus,
    KnowledgeSourceStatus,
    VectorIndexStatus,
)
from modules.ai.repository.embedding_repository import EmbeddingRepository
from modules.ai.repository.knowledge_base_repository import KnowledgeBaseRepository
from modules.ai.repository.knowledge_chunk_repository import KnowledgeChunkRepository
from modules.ai.repository.knowledge_source_repository import KnowledgeSourceRepository
from modules.ai.repository.vector_index_repository import VectorIndexRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import VectorIndexEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class KnowledgeIngestionService:
    """Orchestrates metadata ingestion: source → chunk stubs → embedding stubs → index status."""

    def __init__(self, db: Session) -> None:
        self._bases = KnowledgeBaseRepository(db)
        self._sources = KnowledgeSourceRepository(db)
        self._chunks = KnowledgeChunkRepository(db)
        self._embeddings = EmbeddingRepository(db)
        self._indexes = VectorIndexRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._index_engine = VectorIndexEngine()
        self._audit = AuditService(db)
        self._db = db

    def enqueue_metadata_ingestion(
        self,
        ctx: TenantContext,
        knowledge_base_id: UUID,
        *,
        model_id: UUID | None = None,
    ) -> dict:
        """Enqueue Celery metadata ingestion sweep — stub delay only."""
        from modules.ai.tasks import knowledge_ingestion_metadata_sweep

        kb = self._bases.get(ctx, knowledge_base_id)
        if kb is None:
            raise NotFoundException("Knowledge base not found")
        task = knowledge_ingestion_metadata_sweep.delay(str(knowledge_base_id))
        return {
            "status": "enqueued",
            "knowledge_base_id": str(knowledge_base_id),
            "task_id": task.id,
            "model_id": str(model_id) if model_id else None,
        }

    def run_metadata_ingestion(
        self,
        ctx: TenantContext,
        knowledge_base_id: UUID,
        *,
        model_id: UUID | None = None,
    ) -> dict:
        """Synchronous metadata orchestration — no provider SDK calls."""
        kb = self._bases.get(ctx, knowledge_base_id)
        if kb is None:
            raise NotFoundException("Knowledge base not found")

        sources = self._sources.list_by_knowledge_base(ctx, knowledge_base_id)
        active_sources = [s for s in sources if s.status == KnowledgeSourceStatus.ACTIVE.value]
        chunks_created = 0
        embeddings_created = 0

        for source in active_sources:
            existing = self._chunks.list_by_source(ctx, source.id)
            if not existing:
                chunk = self._chunks.create(
                    ctx,
                    company_id=source.company_id,
                    knowledge_source_id=source.id,
                    chunk_code=f"{source.source_code}-001",
                    sequence_no=1,
                    content_preview="[metadata stub]",
                    status=KnowledgeChunkStatus.CREATED.value,
                )
                chunks_created += 1
                if model_id:
                    self._embeddings.create(
                        ctx,
                        company_id=source.company_id,
                        knowledge_chunk_id=chunk.id,
                        model_id=model_id,
                        embedding_code=f"{chunk.chunk_code}-EMB",
                        status=EmbeddingStatus.CREATED.value,
                    )
                    embeddings_created += 1

        indexes = self._indexes.list_by_knowledge_base(ctx, knowledge_base_id)
        indexes_updated = 0
        for index in indexes:
            if index.status == VectorIndexStatus.ACTIVE.value:
                self._index_engine.start_rebuild(index)
                self._indexes.update(ctx, index.id, status=index.status)
                indexes_updated += 1
            elif index.status == VectorIndexStatus.REBUILDING.value:
                self._index_engine.activate(index)
                self._indexes.update(ctx, index.id, status=index.status)
                indexes_updated += 1

        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_base",
            entity_id=knowledge_base_id,
            operation="ingestion_metadata",
            performed_by=ctx.user_id,
        )
        return {
            "status": "ok",
            "knowledge_base_id": str(knowledge_base_id),
            "sources_processed": len(active_sources),
            "chunks_created": chunks_created,
            "embeddings_created": embeddings_created,
            "indexes_updated": indexes_updated,
        }
