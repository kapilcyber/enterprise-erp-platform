"""ConversationService — Phase 1 CRUD + archive / purge."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, ConversationStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.conversation import AiConversation
from modules.ai.repository.conversation_repository import ConversationRepository
from modules.ai.repository.session_repository import SessionRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import ConversationEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class ConversationService:
    def __init__(self, db: Session) -> None:
        self._repo = ConversationRepository(db)
        self._sessions = SessionRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = ConversationEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        session_id: UUID | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "conversation_code",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            session_id=session_id,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiConversation:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Conversation not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        session_id = fields.get("session_id")
        if session_id and self._sessions.get(ctx, session_id) is None:
            raise NotFoundException("AI session not found")
        code = fields.pop("conversation_code", None) or self._numbers.generate(
            AiEntityType.CONVERSATION, cid, AiConversation, "conversation_code"
        )
        fields.setdefault("status", ConversationStatus.ACTIVE.value)
        row = self._repo.create(ctx, company_id=cid, conversation_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation",
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
            raise NotFoundException("Conversation not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Conversation not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived conversation not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def purge(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.purge(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation",
            entity_id=row_id,
            operation="purge",
            performed_by=ctx.user_id,
        )
        return updated
