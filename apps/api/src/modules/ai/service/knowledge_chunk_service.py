"""KnowledgeChunkService — Phase 2 CRUD + invalidate."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, KnowledgeChunkStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.knowledge_chunk import AiKnowledgeChunk
from modules.ai.repository.knowledge_chunk_repository import KnowledgeChunkRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import KnowledgeChunkEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class KnowledgeChunkService:
    def __init__(self, db: Session) -> None:
        self._repo = KnowledgeChunkRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = KnowledgeChunkEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "sequence_no",
        sort_dir: str = "asc",
        knowledge_source_id: UUID | None = None,
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            knowledge_source_id=knowledge_source_id,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiKnowledgeChunk:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Knowledge chunk not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("chunk_code", None) or self._numbers.generate(
            AiEntityType.KNOWLEDGE_CHUNK, cid, AiKnowledgeChunk, "chunk_code"
        )
        fields.setdefault("status", KnowledgeChunkStatus.CREATED.value)
        row = self._repo.create(ctx, company_id=cid, chunk_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_chunk",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Knowledge chunk not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_chunk",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Knowledge chunk not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_chunk",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived knowledge chunk not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_chunk",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def invalidate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.invalidate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_chunk",
            entity_id=row_id,
            operation="invalidate",
            performed_by=ctx.user_id,
        )
        return updated
