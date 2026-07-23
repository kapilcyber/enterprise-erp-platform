"""FormFieldService — Phase 2A."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType
from modules.lowcode.domain.exceptions import DuplicateFieldKeyForbidden, InvalidFieldState
from modules.lowcode.models import LcFormField
from modules.lowcode.repository.component_version_repository import ComponentVersionRepository
from modules.lowcode.repository.data_source_repository import DataSourceRepository
from modules.lowcode.repository.form_field_repository import FormFieldRepository
from modules.lowcode.repository.form_section_repository import FormSectionRepository
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.service.engines import FormFieldEngine, FormVersionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class FormFieldService:
    def __init__(self, db: Session) -> None:
        self._repo = FormFieldRepository(db)
        self._sections = FormSectionRepository(db)
        self._versions = FormVersionRepository(db)
        self._component_versions = ComponentVersionRepository(db)
        self._data_sources = DataSourceRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = FormFieldEngine()
        self._version_engine = FormVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, form_version_id: UUID):
        version = self._versions.get(ctx, form_version_id)
        if version is None:
            raise NotFoundException("Form version not found")
        self._version_engine.assert_editable(version)
        return version

    def _assert_section_same_version(
        self, ctx: TenantContext, form_version_id: UUID, section_id: UUID | None
    ) -> None:
        if section_id is None:
            return
        section = self._sections.get(ctx, section_id)
        if section is None:
            raise NotFoundException("Form section not found")
        if section.form_version_id != form_version_id:
            raise InvalidFieldState("Section must belong to the same Form Version")

    def _assert_component_version(
        self, ctx: TenantContext, component_version_id: UUID | None
    ) -> None:
        if component_version_id is None:
            return
        cv = self._component_versions.get(ctx, component_version_id)
        if cv is None:
            raise NotFoundException("Component version not found")

    def _assert_data_source(self, ctx: TenantContext, data_source_id: UUID | None) -> None:
        if data_source_id is None:
            return
        ds = self._data_sources.get(ctx, data_source_id)
        if ds is None:
            raise NotFoundException("Data source not found")

    def _assert_unique_key(
        self,
        ctx: TenantContext,
        form_version_id: UUID,
        field_key: str,
        *,
        exclude_id: UUID | None = None,
    ) -> None:
        existing = self._repo.get_by_key(ctx, form_version_id, field_key)
        if existing is not None and (exclude_id is None or existing.id != exclude_id):
            raise DuplicateFieldKeyForbidden(
                f"Field key '{field_key}' already exists on this Form Version"
            )

    def list_by_version(self, ctx: TenantContext, form_version_id: UUID):
        if self._versions.get(ctx, form_version_id) is None:
            raise NotFoundException("Form version not found")
        return self._repo.list_by_version(ctx, form_version_id)

    def list_by_section(self, ctx: TenantContext, section_id: UUID):
        if self._sections.get(ctx, section_id) is None:
            raise NotFoundException("Form section not found")
        return self._repo.list_by_section(ctx, section_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcFormField:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Form field not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        form_version_id: UUID,
        *,
        company_id: UUID | None = None,
        **fields,
    ):
        version = self._require_editable_version(ctx, form_version_id)
        field_type = fields.get("field_type")
        self._engine.assert_valid_type(field_type)
        field_key = fields.get("field_key")
        if field_key is None:
            raise InvalidFieldState("field_key is required")
        self._engine.assert_field_key(field_key)
        self._engine.assert_display_order(fields.get("display_order"))
        self._assert_unique_key(ctx, form_version_id, field_key)
        self._assert_section_same_version(ctx, form_version_id, fields.get("section_id"))
        self._assert_component_version(ctx, fields.get("component_version_id"))
        self._assert_data_source(ctx, fields.get("data_source_id"))

        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("field_code", None) or self._numbers.generate(
            LowcodeEntityType.FORM_FIELD, cid, LcFormField, "field_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            form_version_id=form_version_id,
            field_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_field",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.form_version_id)
        if "field_type" in fields and fields["field_type"] is not None:
            self._engine.assert_valid_type(fields["field_type"])
        if "field_key" in fields and fields["field_key"] is not None:
            self._engine.assert_field_key(fields["field_key"])
            self._assert_unique_key(
                ctx, row.form_version_id, fields["field_key"], exclude_id=row.id
            )
        if "display_order" in fields:
            self._engine.assert_display_order(fields.get("display_order"))
        if "section_id" in fields:
            self._assert_section_same_version(
                ctx, row.form_version_id, fields.get("section_id")
            )
        if "component_version_id" in fields:
            self._assert_component_version(ctx, fields.get("component_version_id"))
        if "data_source_id" in fields:
            self._assert_data_source(ctx, fields.get("data_source_id"))
        fields.pop("form_version_id", None)
        fields.pop("field_code", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Form field not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_field",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.form_version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Form field not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_field",
            entity_id=row_id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
