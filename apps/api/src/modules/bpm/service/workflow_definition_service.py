"""WorkflowDefinitionService — Phase 1.5."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, DefinitionStatus, VersionStatus
from modules.bpm.domain.value_objects import PageResult
from modules.bpm.models import BpmWorkflowDefinition, BpmWorkflowVersion
from modules.bpm.repository.workflow_definition_repository import WorkflowDefinitionRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import WorkflowDefinitionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class WorkflowDefinitionService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowDefinitionRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = WorkflowDefinitionEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        module_code: str | None = None,
        entity_type: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "definition_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            module_code=module_code,
            entity_type=entity_type,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowDefinition:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow definition not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("definition_code", None) or self._numbers.generate(
            BpmEntityType.WORKFLOW_DEFINITION, cid, BpmWorkflowDefinition, "definition_code"
        )
        row = self._repo.create(ctx, company_id=cid, definition_code=code, **fields)
        ver_code = self._numbers.generate(
            BpmEntityType.WORKFLOW_VERSION, cid, BpmWorkflowVersion, "version_code"
        )
        self._versions.create(
            ctx,
            company_id=cid,
            definition_id=row.id,
            version_code=ver_code,
            version_number=1,
            version_label="v1",
            status=VersionStatus.DRAFT.value,
            change_notes="Initial draft",
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_definition",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("Workflow definition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_definition",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow definition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_definition",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived workflow definition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_definition",
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

    def create_from_template(
        self,
        ctx: TenantContext,
        template,
        *,
        definition_name: str,
        module_code: str | None = None,
        entity_type: str | None = None,
        company_id: UUID | None = None,
    ):
        return self.create(
            ctx,
            company_id=company_id or template.company_id,
            definition_name=definition_name,
            template_id=template.id,
            module_code=module_code or template.module_code or "general",
            entity_type=entity_type or template.entity_type or "document",
            description=template.description,
            owner_employee_id=template.owner_employee_id,
            status=DefinitionStatus.DRAFT.value,
        )
