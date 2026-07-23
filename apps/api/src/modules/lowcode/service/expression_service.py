"""ExpressionService — Phase 2C UI expression definitions (no runtime execution)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType, VersionStatus
from modules.lowcode.domain.value_objects import PageResult
from modules.lowcode.models import LcExpression
from modules.lowcode.repository.expression_repository import ExpressionRepository
from modules.lowcode.service.engines import ExpressionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class ExpressionService:
    def __init__(self, db: Session) -> None:
        self._repo = ExpressionRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = ExpressionEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        expression_kind: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "expression_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        if expression_kind:
            self._engine.assert_valid_kind(expression_kind)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            expression_kind=expression_kind,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> LcExpression:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Expression not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        self._engine.assert_valid_kind(fields.get("expression_kind"))
        self._engine.assert_body(fields.get("expression_body"))
        code = fields.pop("expression_code", None) or self._numbers.generate(
            LowcodeEntityType.EXPRESSION, cid, LcExpression, "expression_code"
        )
        fields.setdefault("status", VersionStatus.DRAFT.value)
        row = self._repo.create(ctx, company_id=cid, expression_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_expression",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        if "expression_kind" in fields and fields["expression_kind"] is not None:
            self._engine.assert_valid_kind(fields["expression_kind"])
        if "expression_body" in fields and fields["expression_body"] is not None:
            self._engine.assert_body(fields["expression_body"])
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Expression not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_expression",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        archived = self._repo.soft_delete(ctx, row_id)
        if archived is None:
            raise NotFoundException("Expression not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_expression",
            entity_id=archived.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return archived

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived expression not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_expression",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def publish(self, ctx: TenantContext, row_id: UUID, *, publish_reason: str | None = None):
        row = self.get(ctx, row_id)
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
            entity_name="lc_expression",
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
            entity_name="lc_expression",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
            new_value={"retire_reason": retire_reason},
        )
        return updated
