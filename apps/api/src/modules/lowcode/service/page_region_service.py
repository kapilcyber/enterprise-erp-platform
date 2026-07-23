"""PageRegionService — Phase 3B layout region metadata (no rendering)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType
from modules.lowcode.models import LcPageRegion
from modules.lowcode.repository.component_version_repository import ComponentVersionRepository
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.repository.page_region_repository import PageRegionRepository
from modules.lowcode.repository.page_version_repository import PageVersionRepository
from modules.lowcode.service.engines import PageRegionEngine, PageVersionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class PageRegionService:
    def __init__(self, db: Session) -> None:
        self._repo = PageRegionRepository(db)
        self._versions = PageVersionRepository(db)
        self._form_versions = FormVersionRepository(db)
        self._component_versions = ComponentVersionRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = PageRegionEngine()
        self._version_engine = PageVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, page_version_id: UUID):
        version = self._versions.get(ctx, page_version_id)
        if version is None:
            raise NotFoundException("Page version not found")
        self._version_engine.assert_editable(version)
        return version

    def _assert_embeds(
        self,
        ctx: TenantContext,
        *,
        embedded_form_version_id: UUID | None,
        embedded_component_version_id: UUID | None,
    ) -> None:
        if (
            embedded_form_version_id is not None
            and self._form_versions.get(ctx, embedded_form_version_id) is None
        ):
            raise NotFoundException("Embedded form version not found")
        if (
            embedded_component_version_id is not None
            and self._component_versions.get(ctx, embedded_component_version_id) is None
        ):
            raise NotFoundException("Embedded component version not found")

    def list_by_version(self, ctx: TenantContext, page_version_id: UUID):
        if self._versions.get(ctx, page_version_id) is None:
            raise NotFoundException("Page version not found")
        return self._repo.list_by_version(ctx, page_version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcPageRegion:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Page region not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        page_version_id: UUID,
        *,
        company_id: UUID | None = None,
        **fields,
    ):
        version = self._require_editable_version(ctx, page_version_id)
        self._engine.assert_valid_type(fields.get("region_type"))
        self._engine.assert_region_name(fields.get("region_name"))
        self._engine.assert_display_order(fields.get("display_order"))
        self._assert_embeds(
            ctx,
            embedded_form_version_id=fields.get("embedded_form_version_id"),
            embedded_component_version_id=fields.get("embedded_component_version_id"),
        )
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("region_code", None) or self._numbers.generate(
            LowcodeEntityType.PAGE_REGION, cid, LcPageRegion, "region_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            page_version_id=page_version_id,
            region_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_page_region",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.page_version_id)
        if "region_type" in fields and fields["region_type"] is not None:
            self._engine.assert_valid_type(fields["region_type"])
        if "region_name" in fields and fields["region_name"] is not None:
            self._engine.assert_region_name(fields["region_name"])
        if "display_order" in fields:
            self._engine.assert_display_order(fields.get("display_order"))
        if (
            "embedded_form_version_id" in fields
            or "embedded_component_version_id" in fields
        ):
            self._assert_embeds(
                ctx,
                embedded_form_version_id=fields.get(
                    "embedded_form_version_id", row.embedded_form_version_id
                ),
                embedded_component_version_id=fields.get(
                    "embedded_component_version_id", row.embedded_component_version_id
                ),
            )
        fields.pop("page_version_id", None)
        fields.pop("region_code", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Page region not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_page_region",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.page_version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Page region not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_page_region",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
