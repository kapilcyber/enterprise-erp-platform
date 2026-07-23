"""ExpressionBindingService — Phase 2C version-scoped design bindings."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import BindingTargetType, LowcodeEntityType
from modules.lowcode.domain.exceptions import InvalidExpressionBindingState
from modules.lowcode.models import LcExpressionBinding
from modules.lowcode.repository.expression_binding_repository import (
    ExpressionBindingRepository,
)
from modules.lowcode.repository.expression_repository import ExpressionRepository
from modules.lowcode.repository.form_field_repository import FormFieldRepository
from modules.lowcode.repository.form_section_repository import FormSectionRepository
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.service.engines import ExpressionBindingEngine, FormVersionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class ExpressionBindingService:
    def __init__(self, db: Session) -> None:
        self._repo = ExpressionBindingRepository(db)
        self._expressions = ExpressionRepository(db)
        self._versions = FormVersionRepository(db)
        self._sections = FormSectionRepository(db)
        self._fields = FormFieldRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = ExpressionBindingEngine()
        self._version_engine = FormVersionEngine()
        self._audit = AuditService(db)

    def _require_expression(self, ctx: TenantContext, expression_id: UUID):
        expr = self._expressions.get(ctx, expression_id)
        if expr is None:
            raise NotFoundException("Expression not found")
        return expr

    def _require_editable_form_version(self, ctx: TenantContext, form_version_id: UUID):
        version = self._versions.get(ctx, form_version_id)
        if version is None:
            raise NotFoundException("Form version not found")
        self._version_engine.assert_editable(version)
        return version

    def _resolve_targets(
        self,
        ctx: TenantContext,
        *,
        target_type: str,
        form_version_id: UUID | None,
        section_id: UUID | None,
        field_id: UUID | None,
        page_version_id: UUID | None,
    ) -> tuple[dict, UUID | None]:
        """Return normalized target columns and optional company_id from form targets."""
        self._engine.assert_valid_target_type(target_type)

        if target_type == BindingTargetType.PAGE_VERSION.value:
            targets = self._engine.normalize_targets(
                target_type=target_type,
                form_version_id=None,
                section_id=None,
                field_id=None,
                page_version_id=page_version_id,
            )
            # Page tables are future — UUID metadata only; company from expression/caller
            return targets, None

        if target_type == BindingTargetType.FORM_VERSION.value:
            if form_version_id is None:
                raise InvalidExpressionBindingState("form_version_id is required")
            version = self._require_editable_form_version(ctx, form_version_id)
            targets = self._engine.normalize_targets(
                target_type=target_type,
                form_version_id=form_version_id,
                section_id=None,
                field_id=None,
                page_version_id=None,
            )
            return targets, version.company_id

        if target_type == BindingTargetType.SECTION.value:
            if section_id is None:
                raise InvalidExpressionBindingState("section_id is required")
            section = self._sections.get(ctx, section_id)
            if section is None:
                raise NotFoundException("Form section not found")
            version = self._require_editable_form_version(ctx, section.form_version_id)
            targets = self._engine.normalize_targets(
                target_type=target_type,
                form_version_id=section.form_version_id,
                section_id=section_id,
                field_id=None,
                page_version_id=None,
            )
            return targets, version.company_id

        if target_type == BindingTargetType.FIELD.value:
            if field_id is None:
                raise InvalidExpressionBindingState("field_id is required")
            field = self._fields.get(ctx, field_id)
            if field is None:
                raise NotFoundException("Form field not found")
            version = self._require_editable_form_version(ctx, field.form_version_id)
            targets = self._engine.normalize_targets(
                target_type=target_type,
                form_version_id=field.form_version_id,
                section_id=field.section_id,
                field_id=field_id,
                page_version_id=None,
            )
            return targets, version.company_id

        raise InvalidExpressionBindingState(f"Unsupported target_type: {target_type}")

    def list_by_expression(self, ctx: TenantContext, expression_id: UUID):
        self._require_expression(ctx, expression_id)
        return self._repo.list_by_expression(ctx, expression_id)

    def list_by_form_version(self, ctx: TenantContext, form_version_id: UUID):
        if self._versions.get(ctx, form_version_id) is None:
            raise NotFoundException("Form version not found")
        return self._repo.list_by_form_version(ctx, form_version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcExpressionBinding:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Expression binding not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        expression_id = fields.pop("expression_id")
        expr = self._require_expression(ctx, expression_id)
        target_type = fields.pop("target_type")
        self._engine.assert_sort_order(fields.get("sort_order"))

        targets, target_company = self._resolve_targets(
            ctx,
            target_type=target_type,
            form_version_id=fields.pop("form_version_id", None),
            section_id=fields.pop("section_id", None),
            field_id=fields.pop("field_id", None),
            page_version_id=fields.pop("page_version_id", None),
        )
        cid = self._scope.resolve_company_id(
            ctx, company_id or target_company or expr.company_id
        )
        code = fields.pop("binding_code", None) or self._numbers.generate(
            LowcodeEntityType.EXPRESSION_BINDING, cid, LcExpressionBinding, "binding_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            expression_id=expression_id,
            binding_code=code,
            target_type=target_type,
            **targets,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_expression_binding",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        # Mutations on form-scoped bindings require draft form version
        if row.form_version_id is not None:
            self._require_editable_form_version(ctx, row.form_version_id)
        if "sort_order" in fields:
            self._engine.assert_sort_order(fields.get("sort_order"))
        # Target reassignment not supported via update — create a new binding
        for locked in (
            "expression_id",
            "target_type",
            "form_version_id",
            "section_id",
            "field_id",
            "page_version_id",
            "binding_code",
        ):
            fields.pop(locked, None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Expression binding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_expression_binding",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        if row.form_version_id is not None:
            self._require_editable_form_version(ctx, row.form_version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Expression binding not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_expression_binding",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
