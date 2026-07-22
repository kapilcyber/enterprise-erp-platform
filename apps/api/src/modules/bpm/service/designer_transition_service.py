"""DesignerTransitionService — Phase 2A."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType
from modules.bpm.domain.exceptions import DuplicateTransitionForbidden
from modules.bpm.models import BpmDesignerTransition
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.designer_transition_repository import DesignerTransitionRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import DesignerTransitionEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class DesignerTransitionService:
    def __init__(self, db: Session) -> None:
        self._repo = DesignerTransitionRepository(db)
        self._nodes = DesignerNodeRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = DesignerTransitionEngine()
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

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmDesignerTransition:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Designer transition not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        version_id: UUID,
        *,
        from_node_id: UUID,
        to_node_id: UUID,
        company_id: UUID | None = None,
        **fields,
    ):
        version = self._require_editable_version(ctx, version_id)
        transition_type = fields.get("transition_type", "sequential")
        self._engine.assert_valid_type(transition_type)
        self._engine.assert_conditional_payload(
            transition_type,
            condition_expression=fields.get("condition_expression"),
            decision_table_id=fields.get("decision_table_id"),
        )

        from_node = self._nodes.get(ctx, from_node_id)
        to_node = self._nodes.get(ctx, to_node_id)
        if from_node is None or to_node is None:
            raise NotFoundException("Transition must reference existing nodes")
        if from_node.version_id != version_id or to_node.version_id != version_id:
            raise NotFoundException("Transition nodes must belong to the same version")

        if self._repo.find_edge(ctx, version_id, from_node_id, to_node_id):
            raise DuplicateTransitionForbidden()

        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("transition_code", None) or self._numbers.generate(
            BpmEntityType.DESIGNER_TRANSITION, cid, BpmDesignerTransition, "transition_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            transition_code=code,
            transition_type=transition_type,
            **{k: v for k, v in fields.items() if k != "transition_type"},
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_designer_transition",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)

        from_node_id = fields.get("from_node_id", row.from_node_id)
        to_node_id = fields.get("to_node_id", row.to_node_id)
        if from_node_id != row.from_node_id or to_node_id != row.to_node_id:
            from_node = self._nodes.get(ctx, from_node_id)
            to_node = self._nodes.get(ctx, to_node_id)
            if from_node is None or to_node is None:
                raise NotFoundException("Transition must reference existing nodes")
            if from_node.version_id != row.version_id or to_node.version_id != row.version_id:
                raise NotFoundException("Transition nodes must belong to the same version")
            existing = self._repo.find_edge(ctx, row.version_id, from_node_id, to_node_id)
            if existing and existing.id != row.id:
                raise DuplicateTransitionForbidden()

        transition_type = fields.get("transition_type", row.transition_type)
        if "transition_type" in fields and fields["transition_type"] is not None:
            self._engine.assert_valid_type(fields["transition_type"])
        self._engine.assert_conditional_payload(
            transition_type,
            condition_expression=fields.get(
                "condition_expression", row.condition_expression
            ),
            decision_table_id=fields.get("decision_table_id", row.decision_table_id),
        )

        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Designer transition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_designer_transition",
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
            raise NotFoundException("Designer transition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_designer_transition",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
