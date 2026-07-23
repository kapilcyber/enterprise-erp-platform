"""ComponentService — Phase 2B catalog identity + initial draft version."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType, VersionStatus
from modules.lowcode.domain.value_objects import PageResult
from modules.lowcode.models import LcComponent, LcComponentVersion
from modules.lowcode.repository.component_repository import ComponentRepository
from modules.lowcode.repository.component_version_repository import ComponentVersionRepository
from modules.lowcode.service.engines import ComponentEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class ComponentService:
    def __init__(self, db: Session) -> None:
        self._repo = ComponentRepository(db)
        self._versions = ComponentVersionRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = ComponentEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        component_kind: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "component_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        if component_kind:
            self._engine.assert_valid_kind(component_kind)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            component_kind=component_kind,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> LcComponent:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Component not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        self._engine.assert_valid_kind(fields.get("component_kind"))
        code = fields.pop("component_code", None) or self._numbers.generate(
            LowcodeEntityType.COMPONENT, cid, LcComponent, "component_code"
        )
        row = self._repo.create(ctx, company_id=cid, component_code=code, **fields)
        ver_code = self._numbers.generate(
            LowcodeEntityType.COMPONENT_VERSION, cid, LcComponentVersion, "version_code"
        )
        self._versions.create(
            ctx,
            company_id=cid,
            component_id=row.id,
            version_code=ver_code,
            version_number=1,
            version_label="v1",
            status=VersionStatus.DRAFT.value,
            change_notes="Initial draft",
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_component",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        if "component_kind" in fields and fields["component_kind"] is not None:
            self._engine.assert_valid_kind(fields["component_kind"])
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("Component not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_component",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Component not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_component",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived component not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_component",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def retire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        return self._repo.update(ctx, row_id, status=row.status)
