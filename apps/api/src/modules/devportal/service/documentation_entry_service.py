"""DocumentationEntryService — Phase 3 CRUD + publish/retire."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.documentation_entry import DpDocumentationEntry
from modules.devportal.repository.documentation_entry_repository import (
    DocumentationEntryRepository,
)
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.devportal.service.engines import DocumentationEntryEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class DocumentationEntryService:
    def __init__(self, db: Session) -> None:
        self._repo = DocumentationEntryRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = DocumentationEntryEngine()

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "title",
        sort_dir: str = "asc",
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
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> DpDocumentationEntry:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("DocumentationEntry not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        entry_type = fields.get("entry_type")
        if not isinstance(entry_type, str):
            raise ConflictException("entry_type is required")
        self._engine.assert_entry_type(entry_type)
        code = fields.pop("entry_code", None) or f"DOC-{uuid4().hex[:8].upper()}"
        fields.setdefault("entry_code", code)
        fields.setdefault("status", "draft")
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_documentation_entry",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        if "entry_type" in fields and fields["entry_type"] is not None:
            self._engine.assert_entry_type(fields["entry_type"])
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("DocumentationEntry not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_documentation_entry",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("DocumentationEntry not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_documentation_entry",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived DocumentationEntry not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_documentation_entry",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def publish(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.publish(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            published_at=row.published_at,
            published_by=row.published_by,
        )
        if updated is None:
            raise NotFoundException("DocumentationEntry not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_documentation_entry",
            entity_id=updated.id,
            operation="publish",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
            retired_by=row.retired_by,
        )
        if updated is None:
            raise NotFoundException("DocumentationEntry not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_documentation_entry",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
