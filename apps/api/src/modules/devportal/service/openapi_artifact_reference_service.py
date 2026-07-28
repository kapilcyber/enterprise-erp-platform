"""OpenapiArtifactReferenceService — Phase 3 metadata; Document UUID only."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.devportal.adapters.document_port import DevportalDocumentAdapter
from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.openapi_artifact_reference import DpOpenapiArtifactReference
from modules.devportal.repository.openapi_artifact_reference_repository import (
    OpenapiArtifactReferenceRepository,
)
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.devportal.service.engines import OpenApiArtifactEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class OpenapiArtifactReferenceService:
    def __init__(self, db: Session) -> None:
        self._repo = OpenapiArtifactReferenceRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = OpenApiArtifactEngine()
        self._documents = DevportalDocumentAdapter(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "artifact_code",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> DpOpenapiArtifactReference:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("OpenapiArtifactReference not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        document_id = self._documents.resolve_document_ref(ctx, fields.get("document_id"))
        fields["document_id"] = document_id
        issues = self._engine.validate_reference(
            document_id=document_id,
            product_version_id=fields.get("product_version_id"),
        )
        if issues:
            codes = [i.code for i in issues]
            raise ConflictException(f"OpenAPI artifact validation failed: {codes}")
        code = fields.pop("artifact_code", None) or f"OAS-{uuid4().hex[:8].upper()}"
        fields.setdefault("artifact_code", code)
        fields.setdefault("status", "active")
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_openapi_artifact_reference",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        fields.pop("status", None)
        if "document_id" in fields:
            fields["document_id"] = self._documents.resolve_document_ref(
                ctx, fields.get("document_id")
            )
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("OpenapiArtifactReference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_openapi_artifact_reference",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("OpenapiArtifactReference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_openapi_artifact_reference",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived OpenapiArtifactReference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_openapi_artifact_reference",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("OpenapiArtifactReference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_openapi_artifact_reference",
            entity_id=updated.id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("OpenapiArtifactReference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_openapi_artifact_reference",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
