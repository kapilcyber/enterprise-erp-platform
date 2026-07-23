"""EventHandlerService — Phase 3A event metadata (no runtime execution)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import BindingTargetType, LowcodeEntityType
from modules.lowcode.domain.exceptions import InvalidEventHandlerState
from modules.lowcode.models import LcEventHandler
from modules.lowcode.repository.event_handler_repository import EventHandlerRepository
from modules.lowcode.repository.form_field_repository import FormFieldRepository
from modules.lowcode.repository.form_section_repository import FormSectionRepository
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.service.engines import EventHandlerEngine, FormVersionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class EventHandlerService:
    def __init__(self, db: Session) -> None:
        self._repo = EventHandlerRepository(db)
        self._versions = FormVersionRepository(db)
        self._sections = FormSectionRepository(db)
        self._fields = FormFieldRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = EventHandlerEngine()
        self._version_engine = FormVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_form_version(self, ctx: TenantContext, form_version_id: UUID):
        version = self._versions.get(ctx, form_version_id)
        if version is None:
            raise NotFoundException("Form version not found")
        self._version_engine.assert_editable(version)
        return version

    def _resolve_targets(
        self,
        ctx: TenantContext,
        *,
        target_type: str,
        form_version_id: UUID | None,
        section_id: UUID | None,
        field_id: UUID | None,
        page_version_id: UUID | None,
    ) -> tuple[dict, UUID | None]:
        self._engine.assert_valid_target_type(target_type)

        if target_type == BindingTargetType.PAGE_VERSION.value:
            targets = self._engine.normalize_targets(
                target_type=target_type,
                form_version_id=None,
                section_id=None,
                field_id=None,
                page_version_id=page_version_id,
            )
            return targets, None

        if target_type == BindingTargetType.FORM_VERSION.value:
            if form_version_id is None:
                raise InvalidEventHandlerState("form_version_id is required")
            version = self._require_editable_form_version(ctx, form_version_id)
            targets = self._engine.normalize_targets(
                target_type=target_type,
                form_version_id=form_version_id,
                section_id=None,
                field_id=None,
                page_version_id=None,
            )
            return targets, version.company_id

        if target_type == BindingTargetType.SECTION.value:
            if section_id is None:
                raise InvalidEventHandlerState("section_id is required")
            section = self._sections.get(ctx, section_id)
            if section is None:
                raise NotFoundException("Form section not found")
            version = self._require_editable_form_version(ctx, section.form_version_id)
            targets = self._engine.normalize_targets(
                target_type=target_type,
                form_version_id=section.form_version_id,
                section_id=section_id,
                field_id=None,
                page_version_id=None,
            )
            return targets, version.company_id

        if target_type == BindingTargetType.FIELD.value:
            if field_id is None:
                raise InvalidEventHandlerState("field_id is required")
            field = self._fields.get(ctx, field_id)
            if field is None:
                raise NotFoundException("Form field not found")
            version = self._require_editable_form_version(ctx, field.form_version_id)
            targets = self._engine.normalize_targets(
                target_type=target_type,
                form_version_id=field.form_version_id,
                section_id=field.section_id,
                field_id=field_id,
                page_version_id=None,
            )
            return targets, version.company_id

        raise InvalidEventHandlerState(f"Unsupported target_type: {target_type}")

    def list_by_form_version(self, ctx: TenantContext, form_version_id: UUID):
        if self._versions.get(ctx, form_version_id) is None:
            raise NotFoundException("Form version not found")
        return self._repo.list_by_form_version(ctx, form_version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcEventHandler:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Event handler not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        event_type = fields.pop("event_type")
        target_type = fields.pop("target_type")
        custom_event_name = fields.get("custom_event_name")
        self._engine.assert_valid_event_type(event_type)
        self._engine.assert_custom_name(event_type, custom_event_name)
        self._engine.assert_execution_order(fields.get("execution_order"))

        targets, target_company = self._resolve_targets(
            ctx,
            target_type=target_type,
            form_version_id=fields.pop("form_version_id", None),
            section_id=fields.pop("section_id", None),
            field_id=fields.pop("field_id", None),
            page_version_id=fields.pop("page_version_id", None),
        )
        cid = self._scope.resolve_company_id(ctx, company_id or target_company)
        code = fields.pop("handler_code", None) or self._numbers.generate(
            LowcodeEntityType.EVENT_HANDLER, cid, LcEventHandler, "handler_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            handler_code=code,
            event_type=event_type,
            target_type=target_type,
            **targets,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_event_handler",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        if row.form_version_id is not None:
            self._require_editable_form_version(ctx, row.form_version_id)
        if "event_type" in fields and fields["event_type"] is not None:
            self._engine.assert_valid_event_type(fields["event_type"])
            self._engine.assert_custom_name(
                fields["event_type"],
                fields.get("custom_event_name", row.custom_event_name),
            )
        elif "custom_event_name" in fields:
            self._engine.assert_custom_name(row.event_type, fields.get("custom_event_name"))
        if "execution_order" in fields:
            self._engine.assert_execution_order(fields.get("execution_order"))
        for locked in (
            "handler_code",
            "target_type",
            "form_version_id",
            "section_id",
            "field_id",
            "page_version_id",
        ):
            fields.pop(locked, None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Event handler not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_event_handler",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        if row.form_version_id is not None:
            self._require_editable_form_version(ctx, row.form_version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Event handler not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_event_handler",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
