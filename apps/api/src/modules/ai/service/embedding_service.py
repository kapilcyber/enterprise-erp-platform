"""EmbeddingService — Phase 2 CRUD + rebuild / invalidate (metadata only)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, EmbeddingStatus, ModelStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.embedding import AiEmbedding
from modules.ai.repository.embedding_repository import EmbeddingRepository
from modules.ai.repository.model_repository import ModelRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import EmbeddingEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class EmbeddingService:
    def __init__(self, db: Session) -> None:
        self._repo = EmbeddingRepository(db)
        self._models = ModelRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = EmbeddingEngine()
        self._audit = AuditService(db)

    def _validate_model(self, ctx: TenantContext, model_id: UUID) -> None:
        model = self._models.get(ctx, model_id)
        if model is None:
            raise NotFoundException("AI model not found for embedding")
        if model.status not in {ModelStatus.APPROVED.value, ModelStatus.DEPRECATED.value}:
            raise NotFoundException("Embedding model must reference an approved AI model")

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "embedding_code",
        sort_dir: str = "asc",
        knowledge_chunk_id: UUID | None = None,
        model_id: UUID | None = None,
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
            knowledge_chunk_id=knowledge_chunk_id,
            model_id=model_id,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiEmbedding:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Embedding not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        model_id = fields.get("model_id")
        if model_id is not None:
            self._validate_model(ctx, model_id)
        code = fields.pop("embedding_code", None) or self._numbers.generate(
            AiEntityType.EMBEDDING, cid, AiEmbedding, "embedding_code"
        )
        fields.setdefault("status", EmbeddingStatus.CREATED.value)
        row = self._repo.create(ctx, company_id=cid, embedding_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_embedding",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        fields.pop("status", None)
        if "model_id" in fields and fields["model_id"] is not None:
            self._validate_model(ctx, fields["model_id"])
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Embedding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_embedding",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Embedding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_embedding",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived embedding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_embedding",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def rebuild(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.mark_rebuilt(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_embedding",
            entity_id=row_id,
            operation="rebuild",
            performed_by=ctx.user_id,
        )
        return updated

    def invalidate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.invalidate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_embedding",
            entity_id=row_id,
            operation="invalidate",
            performed_by=ctx.user_id,
        )
        return updated
