"""DataSourceService — Phase 2C module contract registry (no business rows)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType
from modules.lowcode.domain.value_objects import PageResult
from modules.lowcode.models import LcDataSource
from modules.lowcode.repository.data_source_repository import DataSourceRepository
from modules.lowcode.service.engines import DataSourceEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class DataSourceService:
    def __init__(self, db: Session) -> None:
        self._repo = DataSourceRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = DataSourceEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        module_code: str | None = None,
        entity_type: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "data_source_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            module_code=module_code,
            entity_type=entity_type,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> LcDataSource:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Data source not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        self._engine.assert_module_contract(
            fields.get("module_code"), fields.get("entity_type")
        )
        ops = fields.get("allowed_operations") or "read,lookup"
        self._engine.assert_allowed_operations(ops)
        fields["allowed_operations"] = ops
        code = fields.pop("data_source_code", None) or self._numbers.generate(
            LowcodeEntityType.DATA_SOURCE, cid, LcDataSource, "data_source_code"
        )
        row = self._repo.create(ctx, company_id=cid, data_source_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_data_source",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        if "module_code" in fields or "entity_type" in fields:
            self._engine.assert_module_contract(
                fields.get("module_code", row.module_code),
                fields.get("entity_type", row.entity_type),
            )
        if "allowed_operations" in fields and fields["allowed_operations"] is not None:
            self._engine.assert_allowed_operations(fields["allowed_operations"])
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Data source not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_data_source",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Data source not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_data_source",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived data source not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_data_source",
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
