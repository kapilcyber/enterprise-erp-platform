"""CostRecordService — Phase 1 append-only cost telemetry."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.ai.domain.enums import AiEntityType
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.cost_record import AiCostRecord
from modules.ai.repository.cost_record_repository import CostRecordRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import CostRecordEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class CostRecordService:
    def __init__(self, db: Session) -> None:
        self._repo = CostRecordRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = CostRecordEngine()
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

    def get(self, ctx: TenantContext, row_id: UUID) -> AiCostRecord:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Cost record not found")
        return row

    def append(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("cost_code", None) or self._numbers.generate(
            AiEntityType.COST_RECORD, cid, AiCostRecord, "cost_code"
        )
        fields.setdefault("recorded_at", _utcnow())
        row = self._repo.create(ctx, company_id=cid, cost_code=code, **fields)
        self._engine.validate_append(row)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_cost_record",
            entity_id=row.id,
            operation="append",
            performed_by=ctx.user_id,
        )
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        return self.append(ctx, company_id=company_id, **fields)

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        raise ConflictException("Cost records are append-only")

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Cost record not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_cost_record",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived cost record not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_cost_record",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row
