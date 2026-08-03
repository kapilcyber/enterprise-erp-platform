"""SloDefinitionService — Phase 3 CRUD + lifecycle."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.repository.slo_definition_repository import SloDefinitionRepository
from modules.monitoring.service.engines import SloDefinitionLifecycleEngine
from modules.monitoring.service.monitored_service_service import MonitoredServiceService
from modules.monitoring.service.monitoring_scope_validator import MonitoringScopeValidator


class SloDefinitionService:
    def __init__(self, db: Session) -> None:
        self._repo = SloDefinitionRepository(db)
        self._scope = MonitoringScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = SloDefinitionLifecycleEngine()
        self._services = MonitoredServiceService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "slo_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("SloDefinition not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        service_id = fields.get("service_id")
        if service_id is not None:
            self._services.get(ctx, service_id)
        code = fields.pop("slo_code", None) or f"SLO-{uuid4().hex[:8].upper()}"
        fields.setdefault("slo_code", code)
        fields.setdefault("status", "draft")
        fields.setdefault("definition_version", 1)
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_slo_definition",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("SloDefinition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_slo_definition",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("SloDefinition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_slo_definition",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived SloDefinition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_slo_definition",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def publish(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.publish(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, published_at=row.published_at
        )
        if updated is None:
            raise NotFoundException("SloDefinition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_slo_definition",
            entity_id=updated.id,
            operation="publish",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("SloDefinition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_slo_definition",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
