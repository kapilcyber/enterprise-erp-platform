"""EntitlementService — Phase 2 metadata CRUD (no runtime enforcement)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.entitlement import DpEntitlement
from modules.devportal.repository.entitlement_repository import EntitlementRepository
from modules.devportal.repository.subscription_repository import SubscriptionRepository
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.devportal.service.engines import EntitlementEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class EntitlementService:
    def __init__(self, db: Session) -> None:
        self._repo = EntitlementRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = EntitlementEngine()
        self._subscriptions = SubscriptionRepository(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "scope_code",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> DpEntitlement:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Entitlement not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        subscription = self._subscriptions.get(ctx, fields["subscription_id"])
        if subscription is None:
            raise NotFoundException("Subscription not found")
        fields.setdefault("status", "active")
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_entitlement",
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
            raise NotFoundException("Entitlement not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_entitlement",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Entitlement not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_entitlement",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived Entitlement not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_entitlement",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def _lifecycle(self, ctx: TenantContext, row_id: UUID, action: str):
        row = self.get(ctx, row_id)
        getattr(self._engine, action)(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("Entitlement not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_entitlement",
            entity_id=updated.id,
            operation=action,
            performed_by=ctx.user_id,
        )
        return updated

    def activate(self, ctx: TenantContext, row_id: UUID, **kwargs):
        return self._lifecycle(ctx, row_id, "activate")

    def suspend(self, ctx: TenantContext, row_id: UUID, **kwargs):
        return self._lifecycle(ctx, row_id, "suspend")

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        return self._lifecycle(ctx, row_id, "retire")
