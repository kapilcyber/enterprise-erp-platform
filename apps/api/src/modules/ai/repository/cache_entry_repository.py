"""AiCacheEntry repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.ai.domain.value_objects import PageResult
from modules.ai.models.cache_entry import AiCacheEntry
from modules.ai.repository.base import AiScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {"entry_code", "cache_key", "status", "expires_at", "created_at", "updated_at"}


class CacheEntryRepository(AiScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiCacheEntry | None:
        stmt = select(AiCacheEntry).where(
            AiCacheEntry.id == row_id,
            AiCacheEntry.is_deleted.is_(False),
        )
        stmt = self.apply_ai_filter(stmt, AiCacheEntry, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> AiCacheEntry | None:
        stmt = select(AiCacheEntry).where(AiCacheEntry.id == row_id)
        stmt = self.apply_ai_filter(stmt, AiCacheEntry, ctx)
        return self.db.scalar(stmt)

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "created_at",
        sort_dir: str = "asc",
        include_archived: bool = False,
        session_id: UUID | None = None
    ) -> PageResult:
        stmt = select(AiCacheEntry).where(AiCacheEntry.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(AiCacheEntry.is_deleted.is_(False))
        if status:
            stmt = stmt.where(AiCacheEntry.status == status)
        if session_id:
            stmt = stmt.where(AiCacheEntry.session_id == session_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(AiCacheEntry.entry_code.ilike(like) | AiCacheEntry.cache_key.ilike(like))
        stmt = self.apply_ai_filter(stmt, AiCacheEntry, ctx)
        return self.paginate_sorted(
            stmt,
            AiCacheEntry,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> AiCacheEntry:
        row = AiCacheEntry(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> AiCacheEntry | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> AiCacheEntry | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> AiCacheEntry | None:
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
