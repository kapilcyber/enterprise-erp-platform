"""BPM BpmWorkflowDefinition repository — Phase 1.5."""

from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from modules.bpm.domain.value_objects import PageResult
from modules.bpm.models import BpmWorkflowDefinition
from modules.bpm.repository.base import BpmScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {
    "definition_code",
    "definition_name",
    "status",
    "module_code",
    "entity_type",
    "created_at",
    "updated_at",
}


class WorkflowDefinitionRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowDefinition | None:
        stmt = select(BpmWorkflowDefinition).where(
            BpmWorkflowDefinition.id == row_id,
            BpmWorkflowDefinition.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowDefinition, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(
        self, ctx: TenantContext, row_id: UUID
    ) -> BpmWorkflowDefinition | None:
        stmt = select(BpmWorkflowDefinition).where(BpmWorkflowDefinition.id == row_id)
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowDefinition, ctx)
        return self.db.scalar(stmt)

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        module_code: str | None = None,
        entity_type: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "definition_name",
        sort_dir: str = "asc",
        include_archived: bool = False,
    ) -> PageResult:
        stmt = select(BpmWorkflowDefinition).where(
            BpmWorkflowDefinition.company_id == company_id
        )
        if not include_archived:
            stmt = stmt.where(BpmWorkflowDefinition.is_deleted.is_(False))
        if status:
            stmt = stmt.where(BpmWorkflowDefinition.status == status)
        if module_code:
            stmt = stmt.where(BpmWorkflowDefinition.module_code == module_code)
        if entity_type:
            stmt = stmt.where(BpmWorkflowDefinition.entity_type == entity_type)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                BpmWorkflowDefinition.definition_name.ilike(like)
                | BpmWorkflowDefinition.definition_code.ilike(like)
            )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowDefinition, ctx)
        return self.paginate_sorted(
            stmt,
            BpmWorkflowDefinition,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def count_active(self, ctx: TenantContext, company_id: UUID) -> int:
        stmt = select(func.count()).select_from(BpmWorkflowDefinition).where(
            BpmWorkflowDefinition.company_id == company_id,
            BpmWorkflowDefinition.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowDefinition, ctx)
        return int(self.db.scalar(stmt) or 0)

    def create(self, ctx: TenantContext, **fields) -> BpmWorkflowDefinition:
        row = BpmWorkflowDefinition(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> BpmWorkflowDefinition | None:
        row = self.get(ctx, row_id)
        if row is None:
            return None
        for k, v in fields.items():
            if v is not None:
                setattr(row, k, v)
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowDefinition | None:
        row = self.get(ctx, row_id)
        if row is None:
            return None
        row.is_deleted = True
        row.deleted_at = utcnow()
        row.deleted_by = ctx.user_id
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row

    def restore(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowDefinition | None:
        row = self.get_including_archived(ctx, row_id)
        if row is None or not row.is_deleted:
            return None
        row.is_deleted = False
        row.deleted_at = None
        row.deleted_by = None
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row
