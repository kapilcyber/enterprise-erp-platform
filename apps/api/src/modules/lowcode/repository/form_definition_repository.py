"""Low-Code LcFormDefinition repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.domain.value_objects import PageResult
from modules.lowcode.models import LcFormDefinition
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow

_SORT = {
    "form_code",
    "form_name",
    "status",
    "module_affinity",
    "entity_type",
    "created_at",
    "updated_at",
}


class FormDefinitionRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcFormDefinition | None:
        stmt = select(LcFormDefinition).where(
            LcFormDefinition.id == row_id,
            LcFormDefinition.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormDefinition, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(
        self, ctx: TenantContext, row_id: UUID
    ) -> LcFormDefinition | None:
        stmt = select(LcFormDefinition).where(LcFormDefinition.id == row_id)
        stmt = self.apply_lowcode_filter(stmt, LcFormDefinition, ctx)
        return self.db.scalar(stmt)

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
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
        include_archived: bool = False,
    ) -> PageResult:
        stmt = select(LcFormDefinition).where(LcFormDefinition.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(LcFormDefinition.is_deleted.is_(False))
        if status:
            stmt = stmt.where(LcFormDefinition.status == status)
        if category_id:
            stmt = stmt.where(LcFormDefinition.category_id == category_id)
        if module_affinity:
            stmt = stmt.where(LcFormDefinition.module_affinity == module_affinity)
        if entity_type:
            stmt = stmt.where(LcFormDefinition.entity_type == entity_type)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                LcFormDefinition.form_name.ilike(like)
                | LcFormDefinition.form_code.ilike(like)
            )
        stmt = self.apply_lowcode_filter(stmt, LcFormDefinition, ctx)
        return self.paginate_sorted(
            stmt,
            LcFormDefinition,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> LcFormDefinition:
        row = LcFormDefinition(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> LcFormDefinition | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> LcFormDefinition | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> LcFormDefinition | None:
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
