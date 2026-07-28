"""PlanService — Phase 2 CRUD + Draft / Publish / Retire."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.devportal.domain.value_objects import PageResult, PublishValidationResult
from modules.devportal.models.plan import DpPlan
from modules.devportal.repository.plan_repository import PlanRepository
from modules.devportal.schemas import PublishValidationResponse, ValidationIssueResponse
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.devportal.service.engines import PlanLifecycleEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class PlanService:
    def __init__(self, db: Session) -> None:
        self._repo = PlanRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = PlanLifecycleEngine()

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "plan_name",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> DpPlan:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Plan not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("plan_code", None) or f"PLAN-{uuid4().hex[:8].upper()}"
        fields.setdefault("plan_code", code)
        fields.setdefault("status", "draft")
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_plan",
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
            raise NotFoundException("Plan not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_plan",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Plan not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_plan",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived Plan not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_plan",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def validate_publish(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        # Reuse gate shape: treat plan_code as version_label analogue
        issues = []
        from modules.devportal.domain.enums import PlanStatus
        from modules.devportal.domain.value_objects import ValidationIssue

        if row.status != PlanStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="NOT_DRAFT",
                    message="Only draft plans can be published",
                    field="status",
                )
            )
        if not row.plan_code:
            issues.append(
                ValidationIssue(
                    code="MISSING_PLAN_CODE",
                    message="plan_code is required",
                    field="plan_code",
                )
            )
        result = PublishValidationResult(
            valid=len(issues) == 0,
            version_id=row.id,
            product_id=row.id,
            issues=issues,
        )
        return PublishValidationResponse(
            valid=result.valid,
            version_id=result.version_id,
            product_id=result.product_id,
            issues=[
                ValidationIssueResponse(
                    code=i.code, message=i.message, severity=i.severity, field=i.field
                )
                for i in result.issues
            ],
        )

    def publish(self, ctx: TenantContext, row_id: UUID):
        validation = self.validate_publish(ctx, row_id)
        if not validation.valid:
            raise ConflictException(
                f"Publish validation failed: {[i.code for i in validation.issues]}"
            )
        row = self.get(ctx, row_id)
        self._engine.publish(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            published_at=row.published_at,
            published_by=row.published_by,
        )
        if updated is None:
            raise NotFoundException("Plan not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_plan",
            entity_id=updated.id,
            operation="publish",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
            retired_by=row.retired_by,
        )
        if updated is None:
            raise NotFoundException("Plan not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_plan",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
