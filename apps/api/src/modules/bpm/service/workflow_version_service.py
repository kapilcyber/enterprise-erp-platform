"""WorkflowVersionService — Phase 1.5 publish validation + audit reasons."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.bpm.domain.enums import BpmEntityType, VersionStatus
from modules.bpm.models import BpmWorkflowVersion
from modules.bpm.repository.workflow_definition_repository import WorkflowDefinitionRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import WorkflowVersionEngine
from modules.bpm.service.publish_validation_service import PublishValidationService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class WorkflowVersionService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowVersionRepository(db)
        self._definitions = WorkflowDefinitionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = WorkflowVersionEngine()
        self._audit = AuditService(db)
        self._publish_validator = PublishValidationService(db)

    def list_by_definition(self, ctx: TenantContext, definition_id: UUID):
        definition = self._definitions.get(ctx, definition_id)
        if definition is None:
            raise NotFoundException("Workflow definition not found")
        return self._repo.list_by_definition(ctx, definition_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowVersion:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow version not found")
        return row

    def create_draft(
        self,
        ctx: TenantContext,
        definition_id: UUID,
        *,
        version_label: str | None = None,
        change_notes: str | None = None,
        company_id: UUID | None = None,
    ):
        definition = self._definitions.get(ctx, definition_id)
        if definition is None:
            raise NotFoundException("Workflow definition not found")
        cid = self._scope.resolve_company_id(ctx, company_id or definition.company_id)
        version_number = self._repo.next_version_number(ctx, definition_id)
        ver_code = self._numbers.generate(
            BpmEntityType.WORKFLOW_VERSION, cid, BpmWorkflowVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            definition_id=definition_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            change_notes=change_notes,
            status=VersionStatus.DRAFT.value,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_version",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        fields.pop("definition_id", None)
        fields.pop("version_number", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Workflow version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_version",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def validate_publish(self, ctx: TenantContext, row_id: UUID):
        return self._publish_validator.validate(ctx, row_id)

    def publish(self, ctx: TenantContext, row_id: UUID, *, publish_reason: str | None = None):
        result = self._publish_validator.validate(ctx, row_id)
        if not result.valid:
            raise ConflictException(
                f"Publish validation failed: {[i.code for i in result.issues]}"
            )
        row = self.get(ctx, row_id)
        prior = self._repo.get_published(ctx, row.definition_id)
        if prior is not None and prior.id != row.id:
            self._engine.retire_published(prior, user_id=ctx.user_id)
            self._repo.update(
                ctx,
                prior.id,
                status=prior.status,
                retired_at=prior.retired_at,
                retired_by=prior.retired_by,
                retire_reason="Auto-retired: superseded by publish",
            )
        self._engine.publish(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            published_at=row.published_at,
            published_by=row.published_by,
            publish_reason=publish_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_version",
            entity_id=row_id,
            operation="publish",
            performed_by=ctx.user_id,
            new_value={"publish_reason": publish_reason},
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, *, retire_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
            retired_by=row.retired_by,
            retire_reason=retire_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_version",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
            new_value={"retire_reason": retire_reason},
        )
        return updated

    def clone_version(
        self,
        ctx: TenantContext,
        row_id: UUID,
        *,
        version_label: str | None = None,
        change_notes: str | None = None,
        clone_reason: str | None = None,
    ):
        source = self.get(ctx, row_id)
        cid = source.company_id
        version_number = self._repo.next_version_number(ctx, source.definition_id)
        ver_code = self._numbers.generate(
            BpmEntityType.WORKFLOW_VERSION, cid, BpmWorkflowVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            definition_id=source.definition_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            change_notes=change_notes or f"Cloned from version {source.version_number}",
            status=VersionStatus.DRAFT.value,
            cloned_from_version_id=source.id,
            clone_reason=clone_reason or f"Cloned from {source.version_code}",
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_version",
            entity_id=row.id,
            operation="clone",
            performed_by=ctx.user_id,
            new_value={
                "source_id": str(source.id),
                "clone_reason": clone_reason,
            },
        )
        return row
