"""FormReferenceService — Phase 2B (Low-Code UUID reference only)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, FormReferenceStatus
from modules.bpm.domain.exceptions import InvalidFormReferenceState
from modules.bpm.models import BpmFormReference
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.form_reference_repository import FormReferenceRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import FormReferenceEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class FormReferenceService:
    def __init__(self, db: Session) -> None:
        self._repo = FormReferenceRepository(db)
        self._nodes = DesignerNodeRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = FormReferenceEngine()
        self._version_engine = WorkflowVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        self._version_engine.assert_editable(version)
        return version

    def _assert_node_same_version(
        self, ctx: TenantContext, version_id: UUID, node_id: UUID | None
    ) -> None:
        if node_id is None:
            return
        node = self._nodes.get(ctx, node_id)
        if node is None:
            raise NotFoundException("Designer node not found")
        if node.version_id != version_id:
            raise InvalidFormReferenceState(
                "Form reference node must belong to the same workflow version"
            )

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmFormReference:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Form reference not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        version_id: UUID,
        *,
        company_id: UUID | None = None,
        **fields,
    ):
        version = self._require_editable_version(ctx, version_id)
        self._engine.assert_form_uuid(fields.get("low_code_form_id"))
        access_mode = fields.get("access_mode") or "editable"
        self._engine.assert_valid_mode(access_mode)
        fields["access_mode"] = access_mode
        self._assert_node_same_version(ctx, version_id, fields.get("node_id"))
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("reference_code", None) or self._numbers.generate(
            BpmEntityType.FORM_REFERENCE, cid, BpmFormReference, "reference_code"
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = FormReferenceStatus.ACTIVE.value
        fields.setdefault("is_required", False)
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            reference_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_form_reference",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        if "low_code_form_id" in fields and fields["low_code_form_id"] is not None:
            self._engine.assert_form_uuid(fields["low_code_form_id"])
        if "access_mode" in fields and fields["access_mode"] is not None:
            self._engine.assert_valid_mode(fields["access_mode"])
        if "node_id" in fields:
            self._assert_node_same_version(ctx, row.version_id, fields["node_id"])
        if "status" in fields and fields["status"] is not None:
            allowed = {s.value for s in FormReferenceStatus}
            if fields["status"] not in allowed:
                raise InvalidFormReferenceState(f"Unsupported status: {fields['status']}")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Form reference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_form_reference",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Form reference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_form_reference",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
