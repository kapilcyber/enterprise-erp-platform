"""SubscriptionService — Phase 2 CRUD + approval lifecycle + binding validation."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.subscription import DpSubscription
from modules.devportal.repository.api_product_version_repository import (
    ApiProductVersionRepository,
)
from modules.devportal.repository.application_repository import ApplicationRepository
from modules.devportal.repository.plan_repository import PlanRepository
from modules.devportal.repository.subscription_repository import SubscriptionRepository
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.devportal.service.engines import (
    SubscriptionEligibilityEngine,
    SubscriptionLifecycleEngine,
)
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class SubscriptionService:
    def __init__(self, db: Session) -> None:
        self._repo = SubscriptionRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = SubscriptionLifecycleEngine()
        self._eligibility = SubscriptionEligibilityEngine()
        self._apps = ApplicationRepository(db)
        self._plans = PlanRepository(db)
        self._versions = ApiProductVersionRepository(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "created_at",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> DpSubscription:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Subscription not found")
        return row

    def _assert_binding(self, ctx: TenantContext, fields: dict) -> None:
        application = self._apps.get(ctx, fields["application_id"])
        plan = self._plans.get(ctx, fields["plan_id"])
        product_version = self._versions.get(ctx, fields["product_version_id"])
        self._eligibility.assert_binding_ok(
            plan=plan, product_version=product_version, application=application
        )

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("subscription_code", None) or f"SUB-{uuid4().hex[:8].upper()}"
        fields.setdefault("subscription_code", code)
        fields.setdefault("status", "draft")
        self._assert_binding(ctx, fields)
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_subscription",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        fields.pop("status", None)
        # Re-validate if binding fields change
        binding = {
            "application_id": fields.get("application_id", row.application_id),
            "plan_id": fields.get("plan_id", row.plan_id),
            "product_version_id": fields.get("product_version_id", row.product_version_id),
        }
        if any(k in fields for k in ("application_id", "plan_id", "product_version_id")):
            self._assert_binding(ctx, binding)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Subscription not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_subscription",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Subscription not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_subscription",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived Subscription not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_subscription",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def _lifecycle(self, ctx: TenantContext, row_id: UUID, action: str):
        row = self.get(ctx, row_id)
        getattr(self._engine, action)(row)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            workflow_status=getattr(row, "workflow_status", None),
        )
        if updated is None:
            raise NotFoundException("Subscription not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_subscription",
            entity_id=updated.id,
            operation=action,
            performed_by=ctx.user_id,
        )
        return updated

    def submit(self, ctx: TenantContext, row_id: UUID, **kwargs):
        return self._lifecycle(ctx, row_id, "submit")

    def approve(self, ctx: TenantContext, row_id: UUID, **kwargs):
        return self._lifecycle(ctx, row_id, "approve")

    def activate(self, ctx: TenantContext, row_id: UUID, **kwargs):
        return self._lifecycle(ctx, row_id, "activate")

    def suspend(self, ctx: TenantContext, row_id: UUID, **kwargs):
        return self._lifecycle(ctx, row_id, "suspend")

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        return self._lifecycle(ctx, row_id, "retire")
