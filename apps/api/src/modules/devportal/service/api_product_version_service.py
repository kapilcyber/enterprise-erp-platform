"""ApiProductVersionService — Phase 1 CRUD + lifecycle."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.api_product_version import DpApiProductVersion
from modules.devportal.repository.api_product_version_repository import ApiProductVersionRepository
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.devportal.service.engines import ProductVersionLifecycleEngine
from modules.devportal.service.publish_validation_service import PublishValidationService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class ApiProductVersionService:
    def __init__(self, db: Session) -> None:
        self._repo = ApiProductVersionRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = ProductVersionLifecycleEngine()
        self._publish_validator = PublishValidationService(db)

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

    def get(self, ctx: TenantContext, row_id: UUID) -> DpApiProductVersion:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("ApiProductVersion not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)

        fields.setdefault("status", "draft")

        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_api_product_version",
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
            raise NotFoundException("ApiProductVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_api_product_version",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("ApiProductVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_api_product_version",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived ApiProductVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_api_product_version",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def validate_publish(self, ctx: TenantContext, row_id: UUID):
        from modules.devportal.schemas import PublishValidationResponse, ValidationIssueResponse

        result = self._publish_validator.validate_product_version(ctx, row_id)
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
            warnings=[
                ValidationIssueResponse(
                    code=w.code, message=w.message, severity=w.severity, field=w.field
                )
                for w in result.warnings
            ],
        )

    def publish(self, ctx: TenantContext, row_id: UUID):
        from core.exceptions import ConflictException

        result = self._publish_validator.validate_product_version(ctx, row_id)
        if not result.valid:
            raise ConflictException(f"Publish validation failed: {[i.code for i in result.issues]}")
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
            raise NotFoundException("ApiProductVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_api_product_version",
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
            raise NotFoundException("ApiProductVersion not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_api_product_version",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated

