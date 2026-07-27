"""KnowledgeSourceService — Phase 2 CRUD + activate / suspend / retire."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.adapters.document_port import AiDocumentAdapter
from modules.ai.domain.enums import AiEntityType, KnowledgeSourceStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.knowledge_source import AiKnowledgeSource
from modules.ai.repository.knowledge_source_repository import KnowledgeSourceRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import KnowledgeSourceEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class KnowledgeSourceService:
    def __init__(self, db: Session) -> None:
        self._repo = KnowledgeSourceRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = KnowledgeSourceEngine()
        self._audit = AuditService(db)
        self._document = AiDocumentAdapter(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "source_code",
        sort_dir: str = "asc",
        knowledge_base_id: UUID | None = None,
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
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiKnowledgeSource:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Knowledge source not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        document_id = fields.get("document_id")
        if document_id is not None:
            fields["document_id"] = self._document.resolve_document_ref(ctx, document_id)
        code = fields.pop("source_code", None) or self._numbers.generate(
            AiEntityType.KNOWLEDGE_SOURCE, cid, AiKnowledgeSource, "source_code"
        )
        fields.setdefault("status", KnowledgeSourceStatus.ACTIVE.value)
        row = self._repo.create(ctx, company_id=cid, source_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_source",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        fields.pop("status", None)
        if "document_id" in fields and fields["document_id"] is not None:
            fields["document_id"] = self._document.resolve_document_ref(
                ctx, fields["document_id"]
            )
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Knowledge source not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_source",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Knowledge source not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_source",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived knowledge source not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_source",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_source",
            entity_id=row_id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def suspend(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.suspend(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_source",
            entity_id=row_id,
            operation="suspend",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_knowledge_source",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
