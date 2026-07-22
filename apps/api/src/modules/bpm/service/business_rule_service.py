"""BusinessRuleService — Phase 2B."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, BusinessRuleStatus
from modules.bpm.domain.exceptions import InvalidBusinessRuleState
from modules.bpm.models import BpmBusinessRule
from modules.bpm.repository.business_rule_repository import BusinessRuleRepository
from modules.bpm.repository.decision_table_repository import DecisionTableRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import BusinessRuleEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class BusinessRuleService:
    def __init__(self, db: Session) -> None:
        self._repo = BusinessRuleRepository(db)
        self._tables = DecisionTableRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = BusinessRuleEngine()
        self._version_engine = WorkflowVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        self._version_engine.assert_editable(version)
        return version

    def _assert_decision_table_same_version(
        self, ctx: TenantContext, version_id: UUID, decision_table_id: UUID | None
    ) -> None:
        if decision_table_id is None:
            return
        table = self._tables.get(ctx, decision_table_id)
        if table is None:
            raise NotFoundException("Decision table not found")
        if table.version_id != version_id:
            raise InvalidBusinessRuleState(
                "Decision table must belong to the same workflow version"
            )

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmBusinessRule:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Business rule not found")
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
        rule_type = fields.get("rule_type")
        self._engine.assert_valid_type(rule_type)
        self._engine.assert_expression(fields.get("expression"))
        self._assert_decision_table_same_version(
            ctx, version_id, fields.get("decision_table_id")
        )
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("rule_code", None) or self._numbers.generate(
            BpmEntityType.BUSINESS_RULE, cid, BpmBusinessRule, "rule_code"
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = BusinessRuleStatus.DRAFT.value
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            rule_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_business_rule",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        if "rule_type" in fields and fields["rule_type"] is not None:
            self._engine.assert_valid_type(fields["rule_type"])
        if "expression" in fields and fields["expression"] is not None:
            self._engine.assert_expression(fields["expression"])
        if "decision_table_id" in fields:
            self._assert_decision_table_same_version(
                ctx, row.version_id, fields["decision_table_id"]
            )
        if "status" in fields and fields["status"] is not None:
            allowed = {s.value for s in BusinessRuleStatus}
            if fields["status"] not in allowed:
                raise InvalidBusinessRuleState(f"Unsupported status: {fields['status']}")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Business rule not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_business_rule",
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
            raise NotFoundException("Business rule not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_business_rule",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
