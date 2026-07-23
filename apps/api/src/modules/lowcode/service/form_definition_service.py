"""FormDefinitionService — Phase 1."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType, VersionStatus
from modules.lowcode.domain.value_objects import PageResult
from modules.lowcode.models import LcFormDefinition, LcFormVersion
from modules.lowcode.repository.form_definition_repository import FormDefinitionRepository
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.service.engines import FormDefinitionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class FormDefinitionService:
    def __init__(self, db: Session) -> None:
        self._repo = FormDefinitionRepository(db)
        self._versions = FormVersionRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = FormDefinitionEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        category_id: UUID | None = None,
        module_affinity: str | None = None,
        entity_type: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "form_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            category_id=category_id,
            module_affinity=module_affinity,
            entity_type=entity_type,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> LcFormDefinition:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Form definition not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("form_code", None) or self._numbers.generate(
            LowcodeEntityType.FORM_DEFINITION, cid, LcFormDefinition, "form_code"
        )
        row = self._repo.create(ctx, company_id=cid, form_code=code, **fields)
        ver_code = self._numbers.generate(
            LowcodeEntityType.FORM_VERSION, cid, LcFormVersion, "version_code"
        )
        self._versions.create(
            ctx,
            company_id=cid,
            definition_id=row.id,
            version_code=ver_code,
            version_number=1,
            version_label="v1",
            status=VersionStatus.DRAFT.value,
            change_notes="Initial draft",
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_definition",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("Form definition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_definition",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Form definition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_definition",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived form definition not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_form_definition",
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
