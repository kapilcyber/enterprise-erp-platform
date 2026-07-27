"""EvaluationService — Phase 4 metadata lifecycle (no runtime execution)."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, EvaluationStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.evaluation import AiEvaluation
from modules.ai.repository.evaluation_repository import EvaluationRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import EvaluationEngine, EvaluationQualityEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class EvaluationService:
    def __init__(self, db: Session) -> None:
        self._repo = EvaluationRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = EvaluationEngine()
        self._quality_engine = EvaluationQualityEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "queued_at",
        sort_dir: str = "desc",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> AiEvaluation:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Evaluation not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("evaluation_code", None) or self._numbers.generate(
            AiEntityType.EVALUATION, cid, AiEvaluation, "evaluation_code"
        )
        fields.setdefault("status", EvaluationStatus.QUEUED.value)
        fields.setdefault("queued_at", _utcnow())
        row = self._repo.create(ctx, company_id=cid, evaluation_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_evaluation",
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
            raise NotFoundException("Evaluation not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_evaluation",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Evaluation not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_evaluation",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived evaluation not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_evaluation",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def start(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.start(row)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_evaluation",
            entity_id=row.id,
            operation="start",
            performed_by=ctx.user_id,
        )
        return row

    def complete(
        self,
        ctx: TenantContext,
        row_id: UUID,
        *,
        result_summary_json: str | None = None,
        metrics_json: str | None = None,
    ):
        row = self.get(ctx, row_id)
        self._engine.complete(
            row,
            result_summary_json=result_summary_json,
            metrics_json=metrics_json,
        )
        _ = self._quality_engine.summarize_metadata(
            status=row.status, metrics_json=row.metrics_json
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_evaluation",
            entity_id=row.id,
            operation="complete",
            performed_by=ctx.user_id,
        )
        return row

    def fail(self, ctx: TenantContext, row_id: UUID, *, failure_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.fail(row, failure_reason=failure_reason)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_evaluation",
            entity_id=row.id,
            operation="fail",
            performed_by=ctx.user_id,
        )
        return row

    def get_result_summary(self, ctx: TenantContext, row_id: UUID) -> dict:
        row = self.get(ctx, row_id)
        return {
            "evaluation_id": str(row.id),
            "status": row.status,
            "result_mode": "metadata_only",
            "summary": self._quality_engine.summarize_metadata(
                status=row.status, metrics_json=row.metrics_json
            ),
            "result_summary_json": row.result_summary_json,
            "metrics_json": row.metrics_json,
        }
