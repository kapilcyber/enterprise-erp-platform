"""AssignmentRuleService — Phase 3A (UUID refs only; no peer ORM writes)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import AssignmentStatus, AssignmentStrategy, BpmEntityType
from modules.bpm.domain.exceptions import InvalidAssignmentRuleState
from modules.bpm.models import BpmAssignmentRule
from modules.bpm.repository.assignment_rule_repository import AssignmentRuleRepository
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import AssignmentRuleEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class AssignmentRuleService:
    def __init__(self, db: Session) -> None:
        self._repo = AssignmentRuleRepository(db)
        self._nodes = DesignerNodeRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = AssignmentRuleEngine()
        self._version_engine = WorkflowVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        self._version_engine.assert_editable(version)
        return version

    def _assert_node_same_version(
        self, ctx: TenantContext, version_id: UUID, node_id: UUID | None
    ) -> None:
        if node_id is None:
            return
        node = self._nodes.get(ctx, node_id)
        if node is None:
            raise NotFoundException("Designer node not found")
        if node.version_id != version_id:
            raise InvalidAssignmentRuleState(
                "Assignment rule node must belong to the same workflow version"
            )

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmAssignmentRule:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Assignment rule not found")
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
        assignment_type = fields.get("assignment_type")
        strategy = fields.get("strategy") or AssignmentStrategy.STATIC.value
        fields["strategy"] = strategy
        self._engine.assert_valid_type(assignment_type)
        self._engine.assert_valid_strategy(strategy)
        self._engine.assert_type_targets(
            assignment_type,
            role_id=fields.get("role_id"),
            user_id=fields.get("user_id"),
            department_id=fields.get("department_id"),
            expression=fields.get("expression"),
        )
        self._engine.assert_strategy_metadata(strategy, fields.get("strategy_metadata_json"))
        self._assert_node_same_version(ctx, version_id, fields.get("node_id"))
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("assignment_code", None) or self._numbers.generate(
            BpmEntityType.ASSIGNMENT_RULE, cid, BpmAssignmentRule, "assignment_code"
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = AssignmentStatus.ACTIVE.value
        fields.setdefault("priority", 0)
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            assignment_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_assignment_rule",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        assignment_type = fields.get("assignment_type", row.assignment_type)
        strategy = fields.get("strategy", row.strategy)
        if "assignment_type" in fields and fields["assignment_type"] is not None:
            self._engine.assert_valid_type(fields["assignment_type"])
        if "strategy" in fields and fields["strategy"] is not None:
            self._engine.assert_valid_strategy(fields["strategy"])
        self._engine.assert_type_targets(
            assignment_type,
            role_id=fields.get("role_id", row.role_id),
            user_id=fields.get("user_id", row.user_id),
            department_id=fields.get("department_id", row.department_id),
            expression=fields.get("expression", row.expression),
        )
        meta = fields.get("strategy_metadata_json", row.strategy_metadata_json)
        self._engine.assert_strategy_metadata(strategy, meta)
        if "node_id" in fields:
            self._assert_node_same_version(ctx, row.version_id, fields["node_id"])
        if "status" in fields and fields["status"] is not None:
            allowed = {s.value for s in AssignmentStatus}
            if fields["status"] not in allowed:
                raise InvalidAssignmentRuleState(f"Unsupported status: {fields['status']}")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Assignment rule not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_assignment_rule",
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
            raise NotFoundException("Assignment rule not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_assignment_rule",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
