"""DesignerNodeService — Phase 2A."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, DesignerNodeType
from modules.bpm.domain.exceptions import InvalidDesignerNodeState
from modules.bpm.models import BpmDesignerNode
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.designer_transition_repository import DesignerTransitionRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import DesignerNodeEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class DesignerNodeService:
    def __init__(self, db: Session) -> None:
        self._repo = DesignerNodeRepository(db)
        self._transitions = DesignerTransitionRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = DesignerNodeEngine()
        self._version_engine = WorkflowVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        self._version_engine.assert_editable(version)
        return version

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmDesignerNode:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Designer node not found")
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
        node_type = fields.get("node_type")
        self._engine.assert_valid_type(node_type)

        if node_type == DesignerNodeType.START.value:
            existing = self._repo.list_by_type(ctx, version_id, DesignerNodeType.START.value)
            if existing:
                raise InvalidDesignerNodeState("Exactly one Start Node allowed per version")

        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("node_code", None) or self._numbers.generate(
            BpmEntityType.DESIGNER_NODE, cid, BpmDesignerNode, "node_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            node_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_designer_node",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        if "node_type" in fields and fields["node_type"] is not None:
            self._engine.assert_valid_type(fields["node_type"])
            if fields["node_type"] == DesignerNodeType.START.value:
                existing = self._repo.list_by_type(
                    ctx, row.version_id, DesignerNodeType.START.value
                )
                if any(n.id != row.id for n in existing):
                    raise InvalidDesignerNodeState("Exactly one Start Node allowed per version")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Designer node not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_designer_node",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        # Soft-delete connected transitions first (designer integrity)
        for tr in self._transitions.list_involving_node(ctx, row.version_id, row.id):
            self._transitions.soft_delete(ctx, tr.id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Designer node not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_designer_node",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted
