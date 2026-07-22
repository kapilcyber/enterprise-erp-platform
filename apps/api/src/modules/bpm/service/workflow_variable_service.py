"""WorkflowVariableService — Phase 2B."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import VariableStatus
from modules.bpm.domain.exceptions import InvalidWorkflowVariableState
from modules.bpm.models import BpmWorkflowVariable
from modules.bpm.repository.workflow_variable_repository import WorkflowVariableRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import WorkflowVariableEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class WorkflowVariableService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowVariableRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._engine = WorkflowVariableEngine()
        self._version_engine = WorkflowVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        self._version_engine.assert_editable(version)
        return version

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowVariable:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow variable not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        version_id: UUID,
        *,
        company_id: UUID | None = None,
        **fields,
    ):
        version = self._require_editable_version(ctx, version_id)
        self._engine.assert_key(fields.get("variable_key"))
        self._engine.assert_valid_type(fields.get("variable_type"))
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        if "status" not in fields or fields["status"] is None:
            fields["status"] = VariableStatus.ACTIVE.value
        fields.setdefault("is_required", False)
        fields.setdefault("is_encrypted", False)
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_variable",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        if "variable_key" in fields and fields["variable_key"] is not None:
            self._engine.assert_key(fields["variable_key"])
        if "variable_type" in fields and fields["variable_type"] is not None:
            self._engine.assert_valid_type(fields["variable_type"])
        if "status" in fields and fields["status"] is not None:
            allowed = {s.value for s in VariableStatus}
            if fields["status"] not in allowed:
                raise InvalidWorkflowVariableState(f"Unsupported status: {fields['status']}")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Workflow variable not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_variable",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Workflow variable not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_variable",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
