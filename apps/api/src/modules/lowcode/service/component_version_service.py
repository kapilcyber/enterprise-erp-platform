"""ComponentVersionService — Phase 2B publish / retire / clone."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType, VersionStatus
from modules.lowcode.models import LcComponentVersion
from modules.lowcode.repository.component_repository import ComponentRepository
from modules.lowcode.repository.component_version_repository import ComponentVersionRepository
from modules.lowcode.service.engines import ComponentVersionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class ComponentVersionService:
    def __init__(self, db: Session) -> None:
        self._repo = ComponentVersionRepository(db)
        self._components = ComponentRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = ComponentVersionEngine()
        self._audit = AuditService(db)

    def list_by_component(self, ctx: TenantContext, component_id: UUID):
        if self._components.get(ctx, component_id) is None:
            raise NotFoundException("Component not found")
        return self._repo.list_by_component(ctx, component_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcComponentVersion:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Component version not found")
        return row

    def create_draft(
        self,
        ctx: TenantContext,
        component_id: UUID,
        *,
        version_label: str | None = None,
        change_notes: str | None = None,
        properties_json: str | None = None,
        default_props_json: str | None = None,
        company_id: UUID | None = None,
    ):
        component = self._components.get(ctx, component_id)
        if component is None:
            raise NotFoundException("Component not found")
        cid = self._scope.resolve_company_id(ctx, company_id or component.company_id)
        version_number = self._repo.next_version_number(ctx, component_id)
        ver_code = self._numbers.generate(
            LowcodeEntityType.COMPONENT_VERSION, cid, LcComponentVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            component_id=component_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            change_notes=change_notes,
            properties_json=properties_json,
            default_props_json=default_props_json,
            status=VersionStatus.DRAFT.value,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_component_version",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        fields.pop("component_id", None)
        fields.pop("version_number", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Component version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_component_version",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def publish(self, ctx: TenantContext, row_id: UUID, *, publish_reason: str | None = None):
        row = self.get(ctx, row_id)
        prior = self._repo.get_published(ctx, row.component_id)
        if prior is not None and prior.id != row.id:
            self._engine.retire_published(prior, user_id=ctx.user_id)
            self._repo.update(
                ctx,
                prior.id,
                status=prior.status,
                retired_at=prior.retired_at,
                retired_by=prior.retired_by,
                retire_reason="Auto-retired: superseded by publish",
            )
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
            entity_name="lc_component_version",
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
            entity_name="lc_component_version",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
            new_value={"retire_reason": retire_reason},
        )
        return updated

    def clone_version(
        self,
        ctx: TenantContext,
        row_id: UUID,
        *,
        version_label: str | None = None,
        change_notes: str | None = None,
        clone_reason: str | None = None,
    ):
        source = self.get(ctx, row_id)
        cid = source.company_id
        version_number = self._repo.next_version_number(ctx, source.component_id)
        ver_code = self._numbers.generate(
            LowcodeEntityType.COMPONENT_VERSION, cid, LcComponentVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            component_id=source.component_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            change_notes=change_notes or f"Cloned from version {source.version_number}",
            properties_json=source.properties_json,
            default_props_json=source.default_props_json,
            status=VersionStatus.DRAFT.value,
            cloned_from_version_id=source.id,
            clone_reason=clone_reason or f"Cloned from {source.version_code}",
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_component_version",
            entity_id=row.id,
            operation="clone",
            performed_by=ctx.user_id,
            new_value={
                "source_id": str(source.id),
                "clone_reason": clone_reason,
            },
        )
        return row
