"""PublishHistoryService — Phase 4 append-oriented trail (not Foundation Audit)."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import ArtifactKind, LowcodeEntityType, PublishHistoryAction
from modules.lowcode.models import LcPublishHistory
from modules.lowcode.repository.form_definition_repository import FormDefinitionRepository
from modules.lowcode.repository.page_definition_repository import PageDefinitionRepository
from modules.lowcode.repository.publish_history_repository import PublishHistoryRepository
from modules.lowcode.service.engines import PublishHistoryEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PublishHistoryService:
    def __init__(self, db: Session) -> None:
        self._repo = PublishHistoryRepository(db)
        self._forms = FormDefinitionRepository(db)
        self._pages = PageDefinitionRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = PublishHistoryEngine()
        self._audit = AuditService(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcPublishHistory:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Publish history entry not found")
        return row

    def list_by_form_definition(self, ctx: TenantContext, form_definition_id: UUID):
        if self._forms.get(ctx, form_definition_id) is None:
            raise NotFoundException("Form definition not found")
        return self._repo.list_by_form_definition(ctx, form_definition_id)

    def list_by_page_definition(self, ctx: TenantContext, page_definition_id: UUID):
        if self._pages.get(ctx, page_definition_id) is None:
            raise NotFoundException("Page definition not found")
        return self._repo.list_by_page_definition(ctx, page_definition_id)

    def record(
        self,
        ctx: TenantContext,
        *,
        artifact_kind: str,
        action: str,
        company_id: UUID,
        form_definition_id: UUID | None = None,
        page_definition_id: UUID | None = None,
        from_version_id: UUID | None = None,
        to_version_id: UUID | None = None,
        reason: str | None = None,
    ) -> LcPublishHistory:
        """Append-only write used by version publish/retire services."""
        self._engine.assert_valid_action(action)
        targets = self._engine.normalize_targets(
            artifact_kind=artifact_kind,
            form_definition_id=form_definition_id,
            page_definition_id=page_definition_id,
        )
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = self._numbers.generate(
            LowcodeEntityType.PUBLISH_HISTORY, cid, LcPublishHistory, "history_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            history_code=code,
            artifact_kind=artifact_kind,
            action=action,
            reason=reason,
            occurred_at=_utcnow(),
            performed_by=ctx.user_id,
            from_version_id=from_version_id,
            to_version_id=to_version_id,
            **targets,
        )
        # Complement Foundation Audit — does not replace it
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_publish_history",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
            new_value={"action": action, "artifact_kind": artifact_kind},
        )
        return row

    def record_form_publish(
        self,
        ctx: TenantContext,
        *,
        company_id: UUID,
        form_definition_id: UUID,
        from_version_id: UUID | None,
        to_version_id: UUID,
        reason: str | None = None,
    ) -> LcPublishHistory:
        return self.record(
            ctx,
            artifact_kind=ArtifactKind.FORM.value,
            action=PublishHistoryAction.PUBLISH.value,
            company_id=company_id,
            form_definition_id=form_definition_id,
            from_version_id=from_version_id,
            to_version_id=to_version_id,
            reason=reason,
        )

    def record_form_retire(
        self,
        ctx: TenantContext,
        *,
        company_id: UUID,
        form_definition_id: UUID,
        from_version_id: UUID,
        reason: str | None = None,
    ) -> LcPublishHistory:
        return self.record(
            ctx,
            artifact_kind=ArtifactKind.FORM.value,
            action=PublishHistoryAction.RETIRE.value,
            company_id=company_id,
            form_definition_id=form_definition_id,
            from_version_id=from_version_id,
            to_version_id=None,
            reason=reason,
        )

    def record_page_publish(
        self,
        ctx: TenantContext,
        *,
        company_id: UUID,
        page_definition_id: UUID,
        from_version_id: UUID | None,
        to_version_id: UUID,
        reason: str | None = None,
    ) -> LcPublishHistory:
        return self.record(
            ctx,
            artifact_kind=ArtifactKind.PAGE.value,
            action=PublishHistoryAction.PUBLISH.value,
            company_id=company_id,
            page_definition_id=page_definition_id,
            from_version_id=from_version_id,
            to_version_id=to_version_id,
            reason=reason,
        )

    def record_page_retire(
        self,
        ctx: TenantContext,
        *,
        company_id: UUID,
        page_definition_id: UUID,
        from_version_id: UUID,
        reason: str | None = None,
    ) -> LcPublishHistory:
        return self.record(
            ctx,
            artifact_kind=ArtifactKind.PAGE.value,
            action=PublishHistoryAction.RETIRE.value,
            company_id=company_id,
            page_definition_id=page_definition_id,
            from_version_id=from_version_id,
            to_version_id=None,
            reason=reason,
        )
