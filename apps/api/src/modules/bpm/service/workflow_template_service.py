"""WorkflowTemplateService — Phase 1.5."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, TemplateStatus
from modules.bpm.domain.value_objects import PageResult
from modules.bpm.models import BpmWorkflowTemplate
from modules.bpm.repository.workflow_template_repository import WorkflowTemplateRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import WorkflowTemplateEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class WorkflowTemplateService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowTemplateRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = WorkflowTemplateEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        category_id: UUID | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "template_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            category_id=category_id,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def autocomplete(
        self, ctx: TenantContext, q: str, company_id: UUID | None = None, *, limit: int = 10
    ):
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.autocomplete(ctx, cid, q, limit=limit)

    def recent(self, ctx: TenantContext, company_id: UUID | None = None, *, limit: int = 10):
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.recent(ctx, cid, limit=limit)

    def popular(self, ctx: TenantContext, company_id: UUID | None = None, *, limit: int = 10):
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.popular(ctx, cid, limit=limit)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowTemplate:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow template not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("template_code", None) or self._numbers.generate(
            BpmEntityType.WORKFLOW_TEMPLATE, cid, BpmWorkflowTemplate, "template_code"
        )
        row = self._repo.create(ctx, company_id=cid, template_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_template",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("Workflow template not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_template",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow template not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_template",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived workflow template not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_template",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def retire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def copy_template(self, ctx: TenantContext, row_id: UUID, *, template_name: str | None = None):
        source = self.get(ctx, row_id)
        cid = source.company_id
        code = self._numbers.generate(
            BpmEntityType.WORKFLOW_TEMPLATE, cid, BpmWorkflowTemplate, "template_code"
        )
        name = template_name or f"{source.template_name} (Copy)"
        row = self._repo.create(
            ctx,
            company_id=cid,
            template_code=code,
            template_name=name,
            description=source.description,
            status=TemplateStatus.DRAFT.value,
            category_id=source.category_id,
            module_code=source.module_code,
            entity_type=source.entity_type,
            owner_employee_id=source.owner_employee_id,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_template",
            entity_id=row.id,
            operation="copy",
            performed_by=ctx.user_id,
            new_value={"source_id": str(source.id)},
        )
        return row
