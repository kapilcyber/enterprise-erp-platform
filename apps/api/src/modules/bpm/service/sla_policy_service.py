"""SlaPolicyService — Phase 3A."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, SlaStatus
from modules.bpm.domain.exceptions import InvalidSlaPolicyState
from modules.bpm.models import BpmSlaPolicy
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.sla_policy_repository import SlaPolicyRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import SlaPolicyEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class SlaPolicyService:
    def __init__(self, db: Session) -> None:
        self._repo = SlaPolicyRepository(db)
        self._nodes = DesignerNodeRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = SlaPolicyEngine()
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
            raise InvalidSlaPolicyState(
                "SLA policy node must belong to the same workflow version"
            )

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmSlaPolicy:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("SLA policy not found")
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
        timezone = fields.get("timezone") or "UTC"
        fields["timezone"] = timezone
        warning = fields.get("warning_threshold_minutes", 60)
        breach = fields.get("breach_threshold_minutes", 120)
        self._engine.assert_timezone(timezone)
        self._engine.assert_thresholds(warning, breach)
        self._engine.assert_json_object_or_array(
            "business_hours_json", fields.get("business_hours_json")
        )
        self._engine.assert_json_object_or_array(
            "reminder_intervals_json", fields.get("reminder_intervals_json")
        )
        self._assert_node_same_version(ctx, version_id, fields.get("node_id"))
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("policy_code", None) or self._numbers.generate(
            BpmEntityType.SLA_POLICY, cid, BpmSlaPolicy, "policy_code"
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = SlaStatus.ACTIVE.value
        fields.setdefault("warning_threshold_minutes", 60)
        fields.setdefault("breach_threshold_minutes", 120)
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            policy_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_sla_policy",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        warning = fields.get("warning_threshold_minutes", row.warning_threshold_minutes)
        breach = fields.get("breach_threshold_minutes", row.breach_threshold_minutes)
        if "timezone" in fields and fields["timezone"] is not None:
            self._engine.assert_timezone(fields["timezone"])
        self._engine.assert_thresholds(warning, breach)
        if "business_hours_json" in fields:
            self._engine.assert_json_object_or_array(
                "business_hours_json", fields["business_hours_json"]
            )
        if "reminder_intervals_json" in fields:
            self._engine.assert_json_object_or_array(
                "reminder_intervals_json", fields["reminder_intervals_json"]
            )
        if "node_id" in fields:
            self._assert_node_same_version(ctx, row.version_id, fields["node_id"])
        if "status" in fields and fields["status"] is not None:
            allowed = {s.value for s in SlaStatus}
            if fields["status"] not in allowed:
                raise InvalidSlaPolicyState(f"Unsupported status: {fields['status']}")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("SLA policy not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_sla_policy",
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
            raise NotFoundException("SLA policy not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_sla_policy",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
