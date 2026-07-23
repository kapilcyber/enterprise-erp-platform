"""LocalizationEntryService — Phase 3A localization metadata only."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LocalizationOwnerType, LowcodeEntityType, VersionStatus
from modules.lowcode.domain.exceptions import (
    DuplicateLocalizationKeyForbidden,
    InvalidLocalizationEntryState,
)
from modules.lowcode.models import LcLocalizationEntry
from modules.lowcode.repository.component_repository import ComponentRepository
from modules.lowcode.repository.form_field_repository import FormFieldRepository
from modules.lowcode.repository.form_section_repository import FormSectionRepository
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.repository.localization_entry_repository import (
    LocalizationEntryRepository,
)
from modules.lowcode.service.engines import FormVersionEngine, LocalizationEntryEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class LocalizationEntryService:
    def __init__(self, db: Session) -> None:
        self._repo = LocalizationEntryRepository(db)
        self._versions = FormVersionRepository(db)
        self._sections = FormSectionRepository(db)
        self._fields = FormFieldRepository(db)
        self._components = ComponentRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = LocalizationEntryEngine()
        self._version_engine = FormVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_form_version(self, ctx: TenantContext, form_version_id: UUID):
        version = self._versions.get(ctx, form_version_id)
        if version is None:
            raise NotFoundException("Form version not found")
        self._version_engine.assert_editable(version)
        return version

    def _assert_unique(
        self,
        ctx: TenantContext,
        *,
        owner_type: str,
        owner_ref_id: UUID,
        locale: str,
        translation_key: str,
        exclude_id: UUID | None = None,
    ) -> None:
        existing = self._repo.get_by_owner_key(
            ctx,
            owner_type=owner_type,
            owner_ref_id=owner_ref_id,
            locale=locale,
            translation_key=translation_key,
        )
        if existing is not None and (exclude_id is None or existing.id != exclude_id):
            raise DuplicateLocalizationKeyForbidden(
                f"locale '{locale}' + key '{translation_key}' already exists for this owner"
            )

    def _resolve_owner(
        self,
        ctx: TenantContext,
        *,
        owner_type: str,
        form_version_id: UUID | None,
        section_id: UUID | None,
        field_id: UUID | None,
        component_id: UUID | None,
        page_version_id: UUID | None,
    ) -> tuple[UUID, dict, UUID | None]:
        """Return owner_ref_id, column payload, company_id."""
        self._engine.assert_valid_owner_type(owner_type)

        if owner_type == LocalizationOwnerType.PAGE.value:
            owner_ref, cols = self._engine.resolve_owner_refs(
                owner_type=owner_type,
                form_version_id=None,
                section_id=None,
                field_id=None,
                component_id=None,
                page_version_id=page_version_id,
            )
            return owner_ref, cols, None

        if owner_type == LocalizationOwnerType.COMPONENT.value:
            if component_id is None:
                raise InvalidLocalizationEntryState("component_id is required")
            component = self._components.get(ctx, component_id)
            if component is None:
                raise NotFoundException("Component not found")
            owner_ref, cols = self._engine.resolve_owner_refs(
                owner_type=owner_type,
                form_version_id=None,
                section_id=None,
                field_id=None,
                component_id=component_id,
                page_version_id=None,
            )
            return owner_ref, cols, component.company_id

        if owner_type == LocalizationOwnerType.FORM.value:
            if form_version_id is None:
                raise InvalidLocalizationEntryState("form_version_id is required")
            version = self._require_editable_form_version(ctx, form_version_id)
            owner_ref, cols = self._engine.resolve_owner_refs(
                owner_type=owner_type,
                form_version_id=form_version_id,
                section_id=None,
                field_id=None,
                component_id=None,
                page_version_id=None,
            )
            return owner_ref, cols, version.company_id

        if owner_type == LocalizationOwnerType.SECTION.value:
            if section_id is None:
                raise InvalidLocalizationEntryState("section_id is required")
            section = self._sections.get(ctx, section_id)
            if section is None:
                raise NotFoundException("Form section not found")
            version = self._require_editable_form_version(ctx, section.form_version_id)
            owner_ref, cols = self._engine.resolve_owner_refs(
                owner_type=owner_type,
                form_version_id=section.form_version_id,
                section_id=section_id,
                field_id=None,
                component_id=None,
                page_version_id=None,
            )
            return owner_ref, cols, version.company_id

        if owner_type == LocalizationOwnerType.FIELD.value:
            if field_id is None:
                raise InvalidLocalizationEntryState("field_id is required")
            field = self._fields.get(ctx, field_id)
            if field is None:
                raise NotFoundException("Form field not found")
            version = self._require_editable_form_version(ctx, field.form_version_id)
            owner_ref, cols = self._engine.resolve_owner_refs(
                owner_type=owner_type,
                form_version_id=field.form_version_id,
                section_id=field.section_id,
                field_id=field_id,
                component_id=None,
                page_version_id=None,
            )
            return owner_ref, cols, version.company_id

        raise InvalidLocalizationEntryState(f"Unsupported owner_type: {owner_type}")

    def list_by_form_version(self, ctx: TenantContext, form_version_id: UUID):
        if self._versions.get(ctx, form_version_id) is None:
            raise NotFoundException("Form version not found")
        return self._repo.list_by_form_version(ctx, form_version_id)

    def list_by_owner(self, ctx: TenantContext, owner_type: str, owner_ref_id: UUID):
        self._engine.assert_valid_owner_type(owner_type)
        return self._repo.list_by_owner(ctx, owner_type, owner_ref_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcLocalizationEntry:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Localization entry not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        owner_type = fields.pop("owner_type")
        locale = fields.get("locale")
        translation_key = fields.get("translation_key")
        translated_value = fields.get("translated_value")
        if locale is None:
            raise InvalidLocalizationEntryState("locale is required")
        if translation_key is None:
            raise InvalidLocalizationEntryState("translation_key is required")
        self._engine.assert_locale(locale)
        self._engine.assert_translation_key(translation_key)
        self._engine.assert_translated_value(translated_value)

        owner_ref, cols, owner_company = self._resolve_owner(
            ctx,
            owner_type=owner_type,
            form_version_id=fields.pop("form_version_id", None),
            section_id=fields.pop("section_id", None),
            field_id=fields.pop("field_id", None),
            component_id=fields.pop("component_id", None),
            page_version_id=fields.pop("page_version_id", None),
        )
        self._assert_unique(
            ctx,
            owner_type=owner_type,
            owner_ref_id=owner_ref,
            locale=locale,
            translation_key=translation_key,
        )
        cid = self._scope.resolve_company_id(ctx, company_id or owner_company)
        code = fields.pop("entry_code", None) or self._numbers.generate(
            LowcodeEntityType.LOCALIZATION_ENTRY, cid, LcLocalizationEntry, "entry_code"
        )
        fields.setdefault("status", VersionStatus.DRAFT.value)
        row = self._repo.create(
            ctx,
            company_id=cid,
            entry_code=code,
            owner_type=owner_type,
            owner_ref_id=owner_ref,
            **cols,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_localization_entry",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        if row.form_version_id is not None:
            self._require_editable_form_version(ctx, row.form_version_id)
        locale = fields.get("locale", row.locale)
        translation_key = fields.get("translation_key", row.translation_key)
        if "locale" in fields and fields["locale"] is not None:
            self._engine.assert_locale(fields["locale"])
        if "translation_key" in fields and fields["translation_key"] is not None:
            self._engine.assert_translation_key(fields["translation_key"])
        if "translated_value" in fields and fields["translated_value"] is not None:
            self._engine.assert_translated_value(fields["translated_value"])
        if "locale" in fields or "translation_key" in fields:
            self._assert_unique(
                ctx,
                owner_type=row.owner_type,
                owner_ref_id=row.owner_ref_id,
                locale=locale,
                translation_key=translation_key,
                exclude_id=row.id,
            )
        for locked in (
            "entry_code",
            "owner_type",
            "owner_ref_id",
            "form_version_id",
            "section_id",
            "field_id",
            "component_id",
            "page_version_id",
            "status",
        ):
            fields.pop(locked, None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Localization entry not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_localization_entry",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        if row.form_version_id is not None:
            self._require_editable_form_version(ctx, row.form_version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Localization entry not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_localization_entry",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted

    def publish(self, ctx: TenantContext, row_id: UUID, *, publish_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.publish(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            published_at=row.published_at,
            published_by=row.published_by,
            publish_reason=publish_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_localization_entry",
            entity_id=row_id,
            operation="publish",
            performed_by=ctx.user_id,
            new_value={"publish_reason": publish_reason},
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, *, retire_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
            retired_by=row.retired_by,
            retire_reason=retire_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_localization_entry",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
            new_value={"retire_reason": retire_reason},
        )
        return updated
