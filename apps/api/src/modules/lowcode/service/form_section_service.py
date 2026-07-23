"""FormSectionService — Phase 2A."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType
from modules.lowcode.models import LcFormSection
from modules.lowcode.repository.form_section_repository import FormSectionRepository
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.service.engines import FormSectionEngine, FormVersionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class FormSectionService:
    def __init__(self, db: Session) -> None:
        self._repo = FormSectionRepository(db)
        self._versions = FormVersionRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = FormSectionEngine()
        self._version_engine = FormVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, form_version_id: UUID):
        version = self._versions.get(ctx, form_version_id)
        if version is None:
            raise NotFoundException("Form version not found")
        self._version_engine.assert_editable(version)
        return version

    def list_by_version(self, ctx: TenantContext, form_version_id: UUID):
        if self._versions.get(ctx, form_version_id) is None:
            raise NotFoundException("Form version not found")
        return self._repo.list_by_version(ctx, form_version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcFormSection:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Form section not found")
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
        self._engine.assert_display_order(fields.get("display_order"))
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("section_code", None) or self._numbers.generate(
            LowcodeEntityType.FORM_SECTION, cid, LcFormSection, "section_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            form_version_id=form_version_id,
            section_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_section",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.form_version_id)
        if "display_order" in fields:
            self._engine.assert_display_order(fields.get("display_order"))
        fields.pop("form_version_id", None)
        fields.pop("section_code", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Form section not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_section",
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
            raise NotFoundException("Form section not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_section",
            entity_id=row_id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
