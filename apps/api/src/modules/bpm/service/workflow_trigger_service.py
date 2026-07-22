"""WorkflowTriggerService — Phase 3B (definition capability + optional version binding)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, TriggerStatus
from modules.bpm.domain.exceptions import InvalidWorkflowTriggerState
from modules.bpm.models import BpmWorkflowTrigger
from modules.bpm.repository.workflow_definition_repository import WorkflowDefinitionRepository
from modules.bpm.repository.workflow_trigger_repository import WorkflowTriggerRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import WorkflowTriggerEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class WorkflowTriggerService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowTriggerRepository(db)
        self._definitions = WorkflowDefinitionRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = WorkflowTriggerEngine()
        self._version_engine = WorkflowVersionEngine()
        self._audit = AuditService(db)

    def _require_definition(self, ctx: TenantContext, definition_id: UUID):
        definition = self._definitions.get(ctx, definition_id)
        if definition is None:
            raise NotFoundException("Workflow definition not found")
        return definition

    def _assert_optional_version(
        self, ctx: TenantContext, definition_id: UUID, version_id: UUID | None, *, mutate: bool
    ):
        if version_id is None:
            return None
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        if version.definition_id != definition_id:
            raise InvalidWorkflowTriggerState(
                "Trigger version must belong to the same workflow definition"
            )
        if mutate:
            self._version_engine.assert_editable(version)
        return version

    def _assert_mutable(self, ctx: TenantContext, row: BpmWorkflowTrigger) -> None:
        """Mutations blocked when bound to a published/retired version."""
        if row.version_id is not None:
            self._assert_optional_version(
                ctx, row.definition_id, row.version_id, mutate=True
            )

    def list_by_definition(self, ctx: TenantContext, definition_id: UUID):
        self._require_definition(ctx, definition_id)
        return self._repo.list_by_definition(ctx, definition_id)

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowTrigger:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow trigger not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        definition_id: UUID,
        *,
        company_id: UUID | None = None,
        version_id: UUID | None = None,
        **fields,
    ):
        definition = self._require_definition(ctx, definition_id)
        self._assert_optional_version(ctx, definition_id, version_id, mutate=True)
        trigger_type = fields.get("trigger_type")
        self._engine.assert_valid_type(trigger_type)
        self._engine.assert_type_payload(
            trigger_type,
            event_name=fields.get("event_name"),
            execution_mode_metadata_json=fields.get("execution_mode_metadata_json"),
        )
        cid = self._scope.resolve_company_id(ctx, company_id or definition.company_id)
        code = fields.pop("trigger_code", None) or self._numbers.generate(
            BpmEntityType.WORKFLOW_TRIGGER, cid, BpmWorkflowTrigger, "trigger_code"
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = TriggerStatus.ENABLED.value
        # Prefer definition module/entity when not supplied
        fields.setdefault("module_code", definition.module_code)
        fields.setdefault("entity_type", definition.entity_type)
        row = self._repo.create(
            ctx,
            company_id=cid,
            definition_id=definition_id,
            version_id=version_id,
            trigger_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_trigger",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._assert_mutable(ctx, row)
        definition_id = row.definition_id
        if "version_id" in fields:
            self._assert_optional_version(ctx, definition_id, fields["version_id"], mutate=True)
        trigger_type = fields.get("trigger_type", row.trigger_type)
        if "trigger_type" in fields and fields["trigger_type"] is not None:
            self._engine.assert_valid_type(fields["trigger_type"])
        self._engine.assert_type_payload(
            trigger_type,
            event_name=fields.get("event_name", row.event_name),
            execution_mode_metadata_json=fields.get(
                "execution_mode_metadata_json", row.execution_mode_metadata_json
            ),
        )
        if "status" in fields and fields["status"] is not None:
            allowed = {s.value for s in TriggerStatus}
            if fields["status"] not in allowed:
                raise InvalidWorkflowTriggerState(f"Unsupported status: {fields['status']}")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Workflow trigger not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_trigger",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def enable(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._assert_mutable(ctx, row)
        self._engine.enable(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def disable(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._assert_mutable(ctx, row)
        self._engine.disable(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._assert_mutable(ctx, row)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Workflow trigger not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_trigger",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
