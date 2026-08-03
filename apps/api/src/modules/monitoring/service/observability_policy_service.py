"""ObservabilityPolicyService — Phase 1 CRUD."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.repository.observability_policy_repository import (
    ObservabilityPolicyRepository,
)
from modules.monitoring.service.monitoring_scope_validator import MonitoringScopeValidator


class ObservabilityPolicyService:
    def __init__(self, db: Session) -> None:
        self._repo = ObservabilityPolicyRepository(db)
        self._scope = MonitoringScopeValidator(db)
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "policy_name",
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
            raise NotFoundException("ObservabilityPolicy not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("policy_code", None) or f"POL-{uuid4().hex[:8].upper()}"
        fields.setdefault("policy_code", code)
        fields.setdefault("status", "draft")
        fields.setdefault("scope_level", "platform")
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("ObservabilityPolicy not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("ObservabilityPolicy not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived ObservabilityPolicy not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_policy",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row
