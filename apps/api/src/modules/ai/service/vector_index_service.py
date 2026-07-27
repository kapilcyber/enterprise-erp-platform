"""VectorIndexService — Phase 2 CRUD + rebuild / activate / retire."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, ModelStatus, VectorIndexStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.vector_index import AiVectorIndex
from modules.ai.repository.model_repository import ModelRepository
from modules.ai.repository.vector_index_repository import VectorIndexRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import VectorIndexEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class VectorIndexService:
    def __init__(self, db: Session) -> None:
        self._repo = VectorIndexRepository(db)
        self._models = ModelRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = VectorIndexEngine()
        self._audit = AuditService(db)

    def _validate_model(self, ctx: TenantContext, model_id: UUID) -> None:
        model = self._models.get(ctx, model_id)
        if model is None:
            raise NotFoundException("AI model not found for vector index")
        if model.status not in {ModelStatus.APPROVED.value, ModelStatus.DEPRECATED.value}:
            raise NotFoundException("Vector index model must reference an approved AI model")

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "index_code",
        sort_dir: str = "asc",
        knowledge_base_id: UUID | None = None,
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
            knowledge_base_id=knowledge_base_id,
            model_id=model_id,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiVectorIndex:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Vector index not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        model_id = fields.get("model_id")
        if model_id is not None:
            self._validate_model(ctx, model_id)
        code = fields.pop("index_code", None) or self._numbers.generate(
            AiEntityType.VECTOR_INDEX, cid, AiVectorIndex, "index_code"
        )
        fields.setdefault("status", VectorIndexStatus.ACTIVE.value)
        row = self._repo.create(ctx, company_id=cid, index_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_vector_index",
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
            raise NotFoundException("Vector index not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_vector_index",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Vector index not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_vector_index",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived vector index not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_vector_index",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def rebuild(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.start_rebuild(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_vector_index",
            entity_id=row_id,
            operation="rebuild",
            performed_by=ctx.user_id,
        )
        return updated

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_vector_index",
            entity_id=row_id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_vector_index",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
