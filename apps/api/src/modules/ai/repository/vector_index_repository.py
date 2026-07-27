"""AiVectorIndex repository — Phase 2."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.ai.domain.value_objects import PageResult
from modules.ai.models.vector_index import AiVectorIndex
from modules.ai.repository.base import AiScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {
    "index_code",
    "index_name",
    "status",
    "created_at",
    "updated_at",
}


class VectorIndexRepository(AiScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiVectorIndex | None:
        stmt = select(AiVectorIndex).where(
            AiVectorIndex.id == row_id,
            AiVectorIndex.is_deleted.is_(False),
        )
        stmt = self.apply_ai_filter(stmt, AiVectorIndex, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> AiVectorIndex | None:
        stmt = select(AiVectorIndex).where(AiVectorIndex.id == row_id)
        stmt = self.apply_ai_filter(stmt, AiVectorIndex, ctx)
        return self.db.scalar(stmt)

    def list_by_knowledge_base(
        self, ctx: TenantContext, knowledge_base_id: UUID
    ) -> list[AiVectorIndex]:
        stmt = (
            select(AiVectorIndex)
            .where(
                AiVectorIndex.knowledge_base_id == knowledge_base_id,
                AiVectorIndex.is_deleted.is_(False),
            )
            .order_by(AiVectorIndex.index_code.asc())
        )
        stmt = self.apply_ai_filter(stmt, AiVectorIndex, ctx)
        return list(self.db.scalars(stmt).all())

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "index_code",
        sort_dir: str = "asc",
        include_archived: bool = False,
        knowledge_base_id: UUID | None = None,
        model_id: UUID | None = None,
    ) -> PageResult:
        stmt = select(AiVectorIndex).where(AiVectorIndex.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(AiVectorIndex.is_deleted.is_(False))
        if status:
            stmt = stmt.where(AiVectorIndex.status == status)
        if knowledge_base_id:
            stmt = stmt.where(AiVectorIndex.knowledge_base_id == knowledge_base_id)
        if model_id:
            stmt = stmt.where(AiVectorIndex.model_id == model_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                AiVectorIndex.index_code.ilike(like) | AiVectorIndex.index_name.ilike(like)
            )
        stmt = self.apply_ai_filter(stmt, AiVectorIndex, ctx)
        return self.paginate_sorted(
            stmt,
            AiVectorIndex,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> AiVectorIndex:
        row = AiVectorIndex(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> AiVectorIndex | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> AiVectorIndex | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> AiVectorIndex | None:
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
