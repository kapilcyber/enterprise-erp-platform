"""EscalationPolicyService — Phase 3A."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, EscalationStatus
from modules.bpm.domain.exceptions import InvalidEscalationPolicyState
from modules.bpm.models import BpmEscalationPolicy
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.escalation_policy_repository import EscalationPolicyRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import EscalationPolicyEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class EscalationPolicyService:
    def __init__(self, db: Session) -> None:
        self._repo = EscalationPolicyRepository(db)
        self._nodes = DesignerNodeRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = EscalationPolicyEngine()
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
            raise InvalidEscalationPolicyState(
                "Escalation policy node must belong to the same workflow version"
            )

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmEscalationPolicy:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Escalation policy not found")
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
        target_type = fields.get("escalation_target_type")
        self._engine.assert_valid_target_type(target_type)
        self._engine.assert_level(fields.get("escalation_level", 1))
        self._engine.assert_delay(fields.get("escalation_delay_minutes", 0))
        self._engine.assert_retry(fields.get("retry_count", 0))
        self._engine.assert_levels_json(fields.get("levels_json"))
        if fields.get("escalation_target_id") is None:
            raise InvalidEscalationPolicyState("escalation_target_id is required (UUID only)")
        self._assert_node_same_version(ctx, version_id, fields.get("node_id"))
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("policy_code", None) or self._numbers.generate(
            BpmEntityType.ESCALATION_POLICY, cid, BpmEscalationPolicy, "policy_code"
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = EscalationStatus.ACTIVE.value
        fields.setdefault("escalation_level", 1)
        fields.setdefault("escalation_delay_minutes", 0)
        fields.setdefault("retry_count", 0)
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            policy_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_escalation_policy",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        if "escalation_target_type" in fields and fields["escalation_target_type"] is not None:
            self._engine.assert_valid_target_type(fields["escalation_target_type"])
        if "escalation_level" in fields and fields["escalation_level"] is not None:
            self._engine.assert_level(fields["escalation_level"])
        if "escalation_delay_minutes" in fields and fields["escalation_delay_minutes"] is not None:
            self._engine.assert_delay(fields["escalation_delay_minutes"])
        if "retry_count" in fields and fields["retry_count"] is not None:
            self._engine.assert_retry(fields["retry_count"])
        if "levels_json" in fields:
            self._engine.assert_levels_json(fields["levels_json"])
        if "node_id" in fields:
            self._assert_node_same_version(ctx, row.version_id, fields["node_id"])
        if "status" in fields and fields["status"] is not None:
            allowed = {s.value for s in EscalationStatus}
            if fields["status"] not in allowed:
                raise InvalidEscalationPolicyState(f"Unsupported status: {fields['status']}")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Escalation policy not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_escalation_policy",
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
            raise NotFoundException("Escalation policy not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_escalation_policy",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
