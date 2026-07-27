"""ConversationMessageService — Phase 1 append-only messages."""

from uuid import UUIDfrom sqlalchemy.orm import Sessionfrom core.exceptions import NotFoundExceptionfrom modules.ai.domain.value_objects import PageResultfrom modules.ai.models.conversation_message import AiConversationMessagefrom modules.ai.repository.conversation_message_repository import ConversationMessageRepositoryfrom modules.ai.repository.conversation_repository import ConversationRepositoryfrom modules.ai.service.ai_scope_validator import AiScopeValidatorfrom modules.ai.service.engines import ConversationMessageEnginefrom modules.foundation.domain.value_objects import TenantContextfrom modules.foundation.service.audit_service import AuditServiceclass ConversationMessageService:
    def __init__(self, db: Session) -> None:
        self._repo = ConversationMessageRepository(db)
        self._conversations = ConversationRepository(db)
        self._scope = AiScopeValidator(db)
        self._engine = ConversationMessageEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        conversation_id: UUID | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "sequence_no",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            search=search,
            conversation_id=conversation_id,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def list_by_conversation(self, ctx: TenantContext, conversation_id: UUID):
        if self._conversations.get(ctx, conversation_id) is None:
            raise NotFoundException("Conversation not found")
        return self._repo.list_by_conversation(ctx, conversation_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiConversationMessage:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Conversation message not found")
        return row

    def append(
        self,
        ctx: TenantContext,
        conversation_id: UUID,
        *,
        message_role: str,
        content_text: str,
        prompt_version_id: UUID | None = None,
        tool_version_id: UUID | None = None,
        token_count: int | None = None,
        sequence_no: int | None = None,
        company_id: UUID | None = None,
    ):
        conversation = self._conversations.get(ctx, conversation_id)
        if conversation is None:
            raise NotFoundException("Conversation not found")
        self._engine.validate_role(message_role)
        existing = self._repo.list_by_conversation(ctx, conversation_id)
        seq = sequence_no if sequence_no is not None else len(existing)
        self._engine.validate_sequence(seq, seq)
        cid = self._scope.resolve_company_id(ctx, company_id or conversation.company_id)
        row = self._repo.create(
            ctx,
            company_id=cid,
            conversation_id=conversation_id,
            message_role=message_role,
            content_text=content_text,
            sequence_no=seq,
            prompt_version_id=prompt_version_id,
            tool_version_id=tool_version_id,
            token_count=token_count,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation_message",
            entity_id=row.id,
            operation="append",
            performed_by=ctx.user_id,
        )
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        conversation_id = fields.pop("conversation_id")
        return self.append(ctx, conversation_id, company_id=company_id, **fields)

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        if "content_text" in fields:
            self._engine.assert_content_immutable(
                row, content_text=fields.get("content_text")
            )
            fields.pop("content_text", None)
        fields.pop("sequence_no", None)
        fields.pop("message_role", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Conversation message not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation_message",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Conversation message not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation_message",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived conversation message not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_conversation_message",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row
