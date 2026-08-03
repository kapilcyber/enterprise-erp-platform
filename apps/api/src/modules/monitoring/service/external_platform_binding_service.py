"""ExternalPlatformBindingService — Phase 3 CRUD + lifecycle."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.monitoring.domain.exceptions import SecretMaterializationForbidden
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.repository.external_platform_binding_repository import (
    ExternalPlatformBindingRepository,
)
from modules.monitoring.service.engines import ExternalPlatformBindingLifecycleEngine
from modules.monitoring.service.monitoring_scope_validator import MonitoringScopeValidator

_PLAINTEXT_MARKERS = ("password=", "secret=", "token=", "apikey=", "-----BEGIN")


def _reject_plaintext_secret(secret_ref: str | None) -> None:
    if secret_ref is None:
        return
    lowered = secret_ref.strip().lower()
    if any(m in lowered for m in _PLAINTEXT_MARKERS) or "\n" in secret_ref:
        raise SecretMaterializationForbidden()


class ExternalPlatformBindingService:
    def __init__(self, db: Session) -> None:
        self._repo = ExternalPlatformBindingRepository(db)
        self._scope = MonitoringScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = ExternalPlatformBindingLifecycleEngine()

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "binding_name",
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
            raise NotFoundException("ExternalPlatformBinding not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        platform_type = fields.get("platform_type")
        if not platform_type:
            raise ConflictException("ExternalPlatformBinding requires platform_type")
        _reject_plaintext_secret(fields.get("secret_ref"))
        code = fields.pop("binding_code", None) or f"EPB-{uuid4().hex[:8].upper()}"
        fields.setdefault("binding_code", code)
        fields.setdefault("status", "draft")
        fields.setdefault("definition_version", 1)
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_external_platform_binding",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        if "secret_ref" in fields:
            _reject_plaintext_secret(fields.get("secret_ref"))
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("ExternalPlatformBinding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_external_platform_binding",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("ExternalPlatformBinding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_external_platform_binding",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived ExternalPlatformBinding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_external_platform_binding",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, activated_at=row.activated_at
        )
        if updated is None:
            raise NotFoundException("ExternalPlatformBinding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_external_platform_binding",
            entity_id=updated.id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("ExternalPlatformBinding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_external_platform_binding",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
