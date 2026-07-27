"""FeedbackService — Phase 4 capture / review / close metadata."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, FeedbackStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.feedback import AiFeedback
from modules.ai.repository.feedback_repository import FeedbackRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import FeedbackEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class FeedbackService:
    def __init__(self, db: Session) -> None:
        self._repo = FeedbackRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = FeedbackEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        session_id: UUID | None = None,
        conversation_id: UUID | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "created_at",
        sort_dir: str = "desc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            session_id=session_id,
            conversation_id=conversation_id,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiFeedback:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Feedback not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("feedback_code", None) or self._numbers.generate(
            AiEntityType.FEEDBACK, cid, AiFeedback, "feedback_code"
        )
        fields.setdefault("status", FeedbackStatus.CAPTURED.value)
        row = self._repo.create(ctx, company_id=cid, feedback_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_feedback",
            entity_id=row.id,
            operation="capture",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Feedback not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_feedback",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Feedback not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_feedback",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived feedback not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_feedback",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def review(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.review(row, user_id=ctx.user_id)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_feedback",
            entity_id=row.id,
            operation="review",
            performed_by=ctx.user_id,
        )
        return row

    def close(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.close(row, user_id=ctx.user_id)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_feedback",
            entity_id=row.id,
            operation="close",
            performed_by=ctx.user_id,
        )
        return row
