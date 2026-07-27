"""UsageRecordService — Phase 1 append-only telemetry."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.ai.domain.enums import AiEntityType
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.usage_record import AiUsageRecord
from modules.ai.repository.usage_record_repository import UsageRecordRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import UsageRecordEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class UsageRecordService:
    def __init__(self, db: Session) -> None:
        self._repo = UsageRecordRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = UsageRecordEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        session_id: UUID | None = None,
        model_id: UUID | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "recorded_at",
        sort_dir: str = "desc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            search=search,
            session_id=session_id,
            model_id=model_id,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiUsageRecord:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Usage record not found")
        return row

    def append(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("usage_code", None) or self._numbers.generate(
            AiEntityType.USAGE_RECORD, cid, AiUsageRecord, "usage_code"
        )
        fields.setdefault("recorded_at", _utcnow())
        row = self._repo.create(ctx, company_id=cid, usage_code=code, **fields)
        self._engine.validate_append(row)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_usage_record",
            entity_id=row.id,
            operation="append",
            performed_by=ctx.user_id,
        )
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        return self.append(ctx, company_id=company_id, **fields)

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        raise ConflictException("Usage records are append-only")

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Usage record not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_usage_record",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived usage record not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_usage_record",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row
