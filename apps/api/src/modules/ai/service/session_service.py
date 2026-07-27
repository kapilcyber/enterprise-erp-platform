"""SessionService — Phase 1 CRUD + lifecycle."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, SessionStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.session import AiSession
from modules.ai.repository.session_repository import SessionRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import SessionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SessionService:
    def __init__(self, db: Session) -> None:
        self._repo = SessionRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = SessionEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        assistant_id: UUID | None = None,
        user_id: UUID | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "opened_at",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            assistant_id=assistant_id,
            user_id=user_id,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiSession:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("AI session not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("session_code", None) or self._numbers.generate(
            AiEntityType.SESSION, cid, AiSession, "session_code"
        )
        fields.setdefault("status", SessionStatus.OPEN.value)
        fields.setdefault("opened_at", _utcnow())
        fields.setdefault("user_id", ctx.user_id)
        row = self._repo.create(ctx, company_id=cid, session_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_session",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        fields.pop("status", None)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("AI session not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_session",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("AI session not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_session",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived AI session not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_session",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_session",
            entity_id=row_id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def close(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.close(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, closed_at=row.closed_at
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_session",
            entity_id=row_id,
            operation="close",
            performed_by=ctx.user_id,
        )
        return updated

    def expire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.expire(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, closed_at=row.closed_at
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_session",
            entity_id=row_id,
            operation="expire",
            performed_by=ctx.user_id,
        )
        return updated
