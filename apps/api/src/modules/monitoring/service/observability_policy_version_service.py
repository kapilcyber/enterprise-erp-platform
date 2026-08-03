"""ObservabilityPolicyVersionService — Phase 1 CRUD + lifecycle."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.repository.observability_policy_version_repository import (
    ObservabilityPolicyVersionRepository,
)
from modules.monitoring.service.engines import PolicyVersionLifecycleEngine
from modules.monitoring.service.monitoring_scope_validator import MonitoringScopeValidator
from modules.monitoring.service.observability_policy_service import ObservabilityPolicyService


class ObservabilityPolicyVersionService:
    def __init__(self, db: Session) -> None:
        self._repo = ObservabilityPolicyVersionRepository(db)
        self._scope = MonitoringScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = PolicyVersionLifecycleEngine()
        self._policies = ObservabilityPolicyService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "version_label",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("ObservabilityPolicyVersion not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        policy_id = fields.get("policy_id")
        if policy_id is None:
            raise ConflictException("ObservabilityPolicyVersion requires policy_id")
        self._policies.get(ctx, policy_id)
        fields.setdefault("status", "draft")
        fields.setdefault("version_number", 1)
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy_version",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("ObservabilityPolicyVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy_version",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("ObservabilityPolicyVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy_version",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived ObservabilityPolicyVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy_version",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def publish(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.publish(row)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            published_at=row.published_at,
        )
        if updated is None:
            raise NotFoundException("ObservabilityPolicyVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy_version",
            entity_id=updated.id,
            operation="publish",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
        )
        if updated is None:
            raise NotFoundException("ObservabilityPolicyVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy_version",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
