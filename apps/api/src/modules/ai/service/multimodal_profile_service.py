"""MultimodalProfileService — Phase 4 integration readiness metadata (no runtime)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, MultimodalProfileStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.multimodal_profile import AiMultimodalProfile
from modules.ai.repository.multimodal_profile_repository import MultimodalProfileRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import MultimodalProfileEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class MultimodalProfileService:
    def __init__(self, db: Session) -> None:
        self._repo = MultimodalProfileRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = MultimodalProfileEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        modality_kind: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "profile_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            modality_kind=modality_kind,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiMultimodalProfile:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Multimodal profile not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("profile_code", None) or self._numbers.generate(
            AiEntityType.MULTIMODAL_PROFILE, cid, AiMultimodalProfile, "profile_code"
        )
        fields.setdefault("status", MultimodalProfileStatus.DRAFT.value)
        row = self._repo.create(ctx, company_id=cid, profile_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_multimodal_profile",
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
            raise NotFoundException("Multimodal profile not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_multimodal_profile",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Multimodal profile not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_multimodal_profile",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived multimodal profile not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_multimodal_profile",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def publish(self, ctx: TenantContext, row_id: UUID, publish_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.publish(row, user_id=ctx.user_id, publish_reason=publish_reason)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_multimodal_profile",
            entity_id=row.id,
            operation="publish",
            performed_by=ctx.user_id,
        )
        return row

    def retire(self, ctx: TenantContext, row_id: UUID, retire_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id, retire_reason=retire_reason)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_multimodal_profile",
            entity_id=row.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return row

    def get_readiness_snapshot(self, ctx: TenantContext, row_id: UUID) -> dict:
        row = self.get(ctx, row_id)
        return {
            "profile_id": str(row.id),
            "profile_code": row.profile_code,
            "modality_kind": row.modality_kind,
            "status": row.status,
            "provider_id": str(row.provider_id),
            "model_id": str(row.model_id) if row.model_id else None,
            "document_id": str(row.document_id) if row.document_id else None,
            "readiness_mode": "metadata_only",
            "capabilities_json": row.capabilities_json,
        }
