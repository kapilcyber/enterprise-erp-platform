"""NotificationTemplateService — Phase 3B (WHAT only; Foundation delivers)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, NotificationTemplateStatus
from modules.bpm.domain.exceptions import InvalidNotificationTemplateState
from modules.bpm.models import BpmNotificationTemplate
from modules.bpm.repository.notification_template_repository import (
    NotificationTemplateRepository,
)
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import NotificationTemplateEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class NotificationTemplateService:
    def __init__(self, db: Session) -> None:
        self._repo = NotificationTemplateRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = NotificationTemplateEngine()
        self._version_engine = WorkflowVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        self._version_engine.assert_editable(version)
        return version

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmNotificationTemplate:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Notification template not found")
        return row

    def create(
        self, ctx: TenantContext, version_id: UUID, *, company_id: UUID | None = None, **fields
    ):
        version = self._require_editable_version(ctx, version_id)
        template_type = fields.get("template_type")
        self._engine.assert_valid_type(template_type)
        self._engine.assert_content(
            template_type, subject=fields.get("subject"), body=fields.get("body")
        )
        self._engine.assert_json_field("variables_json", fields.get("variables_json"))
        self._engine.assert_json_field("localization_json", fields.get("localization_json"))
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("template_code", None) or self._numbers.generate(
            BpmEntityType.NOTIFICATION_TEMPLATE,
            cid,
            BpmNotificationTemplate,
            "template_code",
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = NotificationTemplateStatus.ENABLED.value
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            template_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_notification_template",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        template_type = fields.get("template_type", row.template_type)
        if "template_type" in fields and fields["template_type"] is not None:
            self._engine.assert_valid_type(fields["template_type"])
        self._engine.assert_content(
            template_type,
            subject=fields.get("subject", row.subject),
            body=fields.get("body", row.body),
        )
        if "variables_json" in fields:
            self._engine.assert_json_field("variables_json", fields["variables_json"])
        if "localization_json" in fields:
            self._engine.assert_json_field("localization_json", fields["localization_json"])
        if "status" in fields and fields["status"] is not None:
            allowed = {s.value for s in NotificationTemplateStatus}
            if fields["status"] not in allowed:
                raise InvalidNotificationTemplateState(
                    f"Unsupported status: {fields['status']}"
                )
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Notification template not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_notification_template",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def enable(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        self._engine.enable(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def disable(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        self._engine.disable(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Notification template not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_notification_template",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
