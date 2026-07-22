"""WorkflowCategoryService — Phase 1.5 archive / restore / pagination."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType
from modules.bpm.domain.value_objects import PageResult
from modules.bpm.models import BpmWorkflowCategory
from modules.bpm.repository.workflow_category_repository import WorkflowCategoryRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import WorkflowCategoryEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class WorkflowCategoryService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowCategoryRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = WorkflowCategoryEngine()
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
        sort_by: str | None = "sort_order",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowCategory:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow category not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("category_code", None) or self._numbers.generate(
            BpmEntityType.WORKFLOW_CATEGORY, cid, BpmWorkflowCategory, "category_code"
        )
        row = self._repo.create(ctx, company_id=cid, category_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_category",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("Workflow category not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_category",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        """Soft archive only — no hard delete."""
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow category not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_category",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        return self.archive(ctx, row_id)

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived workflow category not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_category",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def deactivate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.deactivate(row)
        return self._repo.update(ctx, row_id, status=row.status)
