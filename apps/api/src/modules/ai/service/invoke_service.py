"""InvokeService — gateway path with policy engines; no provider SDK in service layer."""

from decimal import Decimalfrom typing import Anyfrom sqlalchemy.orm import Sessionfrom core.exceptions import AppException, ForbiddenException, NotFoundExceptionfrom modules.ai.adapters.provider_adapter import AiProviderAdapterfrom modules.ai.service.conversation_message_service import ConversationMessageServicefrom modules.ai.service.conversation_service import ConversationServicefrom modules.ai.service.cost_record_service import CostRecordServicefrom modules.ai.service.engines import (    CacheEligibilityEngine,    GuardrailModerationEngine,    RateLimitEngine,)from modules.ai.service.runtime_resolve_service import RuntimeResolveServicefrom modules.ai.service.session_service import SessionServicefrom modules.ai.service.usage_record_service import UsageRecordServicefrom modules.foundation.domain.value_objects import TenantContextclass InvokeService:
    def __init__(self, db: Session) -> None:
        self._adapter = AiProviderAdapter()
        self._resolve = RuntimeResolveService(db)
        self._sessions = SessionService(db)
        self._conversations = ConversationService(db)
        self._messages = ConversationMessageService(db)
        self._guardrail_mod = GuardrailModerationEngine()
        self._rate_limit = RateLimitEngine()
        self._cache_eligibility = CacheEligibilityEngine()
        self._usage = UsageRecordService(db)
        self._cost = CostRecordService(db)

    def invoke(self, ctx: TenantContext, **fields) -> dict[str, Any]:
        assistant_id = fields.get("assistant_id")
        if assistant_id is None:
            raise AppException("assistant_id is required")

        company_id = fields.get("company_id")
        session_id = fields.get("session_id")
        conversation_id = fields.get("conversation_id")
        user_message = fields.get("user_message")
        messages = fields.get("messages")
        use_cache = fields.get("use_cache", False)
        correlation_id = fields.get("correlation_id")
        metadata_json = fields.get("metadata_json")

        if messages:
            msg_list: list[dict] = messages
        elif user_message:
            msg_list = [{"role": "user", "content": user_message}]
        else:
            raise AppException("user_message or messages is required")

        resolved = self._resolve.resolve_assistant(ctx, assistant_id)
        guardrails_required = resolved.get("guardrail_policy_id") is not None
        moderation_required = resolved.get("moderation_policy_id") is not None

        if use_cache and not self._cache_eligibility.is_eligible(
            guardrails_required=guardrails_required,
            moderation_required=moderation_required,
        ):
            use_cache = False

        guardrail_ok = self._guardrail_mod.evaluate_guardrail(
            resolved.get("guardrail_policy_json"),
            protected=guardrails_required,
        )
        moderation_ok = self._guardrail_mod.evaluate_moderation(
            resolved.get("moderation_policy_json"),
            protected=moderation_required,
        )
        rate_ok = self._rate_limit.allow(
            resolved.get("rate_limit_policy_json"),
            key=str(ctx.user_id),
        )

        if not guardrail_ok:
            raise ForbiddenException("Guardrail policy blocked invocation")
        if not moderation_ok:
            raise ForbiddenException("Moderation policy blocked invocation")
        if not rate_ok:
            raise ForbiddenException("Rate limit policy blocked invocation")

        model_id = resolved.get("model_id")
        if model_id is None:
            raise NotFoundException("No routing rule resolved for assistant")

        if session_id is None:
            session = self._sessions.create(
                ctx, company_id=company_id, assistant_id=assistant_id
            )
            session_id = session.id
        else:
            self._sessions.get(ctx, session_id)

        if conversation_id is None:
            conversation = self._conversations.create(
                ctx, company_id=company_id, session_id=session_id
            )
            conversation_id = conversation.id
        else:
            self._conversations.get(ctx, conversation_id)

        if user_message:
            self._messages.append(
                ctx,
                conversation_id,
                message_role="user",
                content_text=user_message,
                company_id=company_id,
            )

        response = self._adapter.invoke(
            msg_list,
            model_ref=model_id,
            credential_ref=None,
            guardrail_allowed=guardrail_ok,
            moderation_allowed=moderation_ok,
            rate_limit_allowed=rate_ok,
        )

        assistant_content = response.get("content") or ""
        assistant_msg = self._messages.append(
            ctx,
            conversation_id,
            message_role="assistant",
            content_text=assistant_content,
            prompt_version_id=resolved.get("prompt_version_id"),
            company_id=company_id,
        )

        usage_record_id = None
        cost_record_id = None
        tokens = response.get("tokens", {})
        usage_row = self._usage.append(
            ctx,
            company_id=company_id,
            session_id=session_id,
            model_id=model_id,
            input_tokens=int(tokens.get("input", 0)),
            output_tokens=int(tokens.get("output", 0)),
            total_tokens=int(tokens.get("total", 0)),
        )
        cost_row = self._cost.append(
            ctx,
            company_id=company_id,
            session_id=session_id,
            model_id=model_id,
            amount=Decimal("0"),
            notes="Phase 1 stub cost",
        )
        usage_record_id = usage_row.id
        cost_record_id = cost_row.id

        return {
            "session_id": session_id,
            "conversation_id": conversation_id,
            "message_id": assistant_msg.id,
            "assistant_message": assistant_content,
            "model_id": model_id,
            "prompt_version_id": resolved.get("prompt_version_id"),
            "usage_record_id": usage_record_id,
            "cost_record_id": cost_record_id,
            "correlation_id": correlation_id,
            "metadata_json": metadata_json,
        }
