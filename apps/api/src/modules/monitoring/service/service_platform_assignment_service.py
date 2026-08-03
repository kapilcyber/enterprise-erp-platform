"""ServicePlatformAssignmentService — Phase 3 CRUD + lifecycle."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.repository.service_platform_assignment_repository import (
    ServicePlatformAssignmentRepository,
)
from modules.monitoring.service.engines import ServicePlatformAssignmentLifecycleEngine
from modules.monitoring.service.external_platform_binding_service import (
    ExternalPlatformBindingService,
)
from modules.monitoring.service.monitored_component_service import MonitoredComponentService
from modules.monitoring.service.monitored_service_service import MonitoredServiceService
from modules.monitoring.service.monitoring_scope_validator import MonitoringScopeValidator


class ServicePlatformAssignmentService:
    def __init__(self, db: Session) -> None:
        self._repo = ServicePlatformAssignmentRepository(db)
        self._scope = MonitoringScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = ServicePlatformAssignmentLifecycleEngine()
        self._services = MonitoredServiceService(db)
        self._components = MonitoredComponentService(db)
        self._bindings = ExternalPlatformBindingService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "created_at",
        sort_dir: str = "desc",
        service_id: UUID | None = None,
        platform_binding_id: UUID | None = None,
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
            service_id=service_id,
            platform_binding_id=platform_binding_id,
        )

    def get(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("ServicePlatformAssignment not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        service_id = fields.get("service_id")
        platform_binding_id = fields.get("platform_binding_id")
        if service_id is None or platform_binding_id is None:
            raise ConflictException(
                "ServicePlatformAssignment requires service_id and platform_binding_id"
            )
        self._services.get(ctx, service_id)
        self._bindings.get(ctx, platform_binding_id)
        component_id = fields.get("component_id")
        if component_id is not None:
            self._components.get(ctx, component_id)
        fields.setdefault("status", "active")
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_service_platform_assignment",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("ServicePlatformAssignment not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_service_platform_assignment",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("ServicePlatformAssignment not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_service_platform_assignment",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived ServicePlatformAssignment not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_service_platform_assignment",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("ServicePlatformAssignment not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_service_platform_assignment",
            entity_id=updated.id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def deactivate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.deactivate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("ServicePlatformAssignment not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_service_platform_assignment",
            entity_id=updated.id,
            operation="deactivate",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("ServicePlatformAssignment not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_service_platform_assignment",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
