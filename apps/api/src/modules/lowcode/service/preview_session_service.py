"""PreviewSessionService — Phase 4 design-time preview (no business mutation)."""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType, PreviewMode, PreviewSessionStatus
from modules.lowcode.models import LcPreviewSession
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.repository.page_version_repository import PageVersionRepository
from modules.lowcode.repository.preview_session_repository import PreviewSessionRepository
from modules.lowcode.service.engines import PreviewSessionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator

_DEFAULT_TTL_MINUTES = 60


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PreviewSessionService:
    def __init__(self, db: Session) -> None:
        self._repo = PreviewSessionRepository(db)
        self._form_versions = FormVersionRepository(db)
        self._page_versions = PageVersionRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = PreviewSessionEngine()
        self._audit = AuditService(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcPreviewSession:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Preview session not found")
        # Lazy expire without starting workflows / mutating business
        if (
            row.status == PreviewSessionStatus.ACTIVE.value
            and row.expires_at is not None
            and row.expires_at <= _utcnow()
        ):
            self._engine.expire(row)
            row = self._repo.update(ctx, row_id, status=row.status) or row
        return row

    def list_by_designer(
        self, ctx: TenantContext, designer_user_id: UUID | None = None
    ):
        uid = designer_user_id or ctx.user_id
        return self._repo.list_by_designer(ctx, uid)

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        preview_mode = fields.get("preview_mode") or PreviewMode.DRAFT.value
        self._engine.assert_valid_mode(preview_mode)
        form_version_id = fields.get("form_version_id")
        page_version_id = fields.get("page_version_id")
        self._engine.assert_version_target(
            form_version_id=form_version_id, page_version_id=page_version_id
        )

        company = company_id
        if form_version_id is not None:
            fv = self._form_versions.get(ctx, form_version_id)
            if fv is None:
                raise NotFoundException("Form version not found")
            self._engine.assert_mode_matches_version(preview_mode, fv.status)
            company = company or fv.company_id
        if page_version_id is not None:
            pv = self._page_versions.get(ctx, page_version_id)
            if pv is None:
                raise NotFoundException("Page version not found")
            self._engine.assert_mode_matches_version(preview_mode, pv.status)
            company = company or pv.company_id

        cid = self._scope.resolve_company_id(ctx, company)
        ttl = fields.pop("ttl_minutes", None) or _DEFAULT_TTL_MINUTES
        expires_at = fields.pop("expires_at", None) or (
            _utcnow() + timedelta(minutes=int(ttl))
        )
        designer_user_id = fields.pop("designer_user_id", None) or ctx.user_id
        code = fields.pop("session_code", None) or self._numbers.generate(
            LowcodeEntityType.PREVIEW_SESSION, cid, LcPreviewSession, "session_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            session_code=code,
            preview_mode=preview_mode,
            status=PreviewSessionStatus.ACTIVE.value,
            designer_user_id=designer_user_id,
            expires_at=expires_at,
            form_version_id=form_version_id,
            page_version_id=page_version_id,
            sample_context_json=fields.get("sample_context_json"),
            notes=fields.get("notes"),
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_preview_session",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def close(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.close(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, closed_at=row.closed_at
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_preview_session",
            entity_id=row_id,
            operation="close",
            performed_by=ctx.user_id,
        )
        return updated

    def expire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        if row.status == PreviewSessionStatus.EXPIRED.value:
            return row
        self._engine.expire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_preview_session",
            entity_id=row_id,
            operation="expire",
            performed_by=ctx.user_id,
        )
        return updated
