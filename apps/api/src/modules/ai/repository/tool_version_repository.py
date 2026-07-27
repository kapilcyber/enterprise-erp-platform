"""AiToolVersion repository — Phase 3."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.ai.domain.enums import ToolVersionStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.tool_version import AiToolVersion
from modules.ai.repository.base import AiScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {"version_code", "version_number", "status", "created_at", "updated_at"}


class ToolVersionRepository(AiScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiToolVersion | None:
        stmt = select(AiToolVersion).where(
            AiToolVersion.id == row_id,
            AiToolVersion.is_deleted.is_(False),
        )
        stmt = self.apply_ai_filter(stmt, AiToolVersion, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> AiToolVersion | None:
        stmt = select(AiToolVersion).where(AiToolVersion.id == row_id)
        stmt = self.apply_ai_filter(stmt, AiToolVersion, ctx)
        return self.db.scalar(stmt)

    def list_by_tool(self, ctx: TenantContext, tool_id: UUID) -> list[AiToolVersion]:
        stmt = select(AiToolVersion).where(
            AiToolVersion.tool_id == tool_id,
            AiToolVersion.is_deleted.is_(False),
        )
        stmt = self.apply_ai_filter(stmt, AiToolVersion, ctx)
        stmt = stmt.order_by(AiToolVersion.version_number.desc())
        return list(self.db.scalars(stmt).all())

    def get_published(self, ctx: TenantContext, tool_id: UUID) -> AiToolVersion | None:
        stmt = select(AiToolVersion).where(
            AiToolVersion.tool_id == tool_id,
            AiToolVersion.status == ToolVersionStatus.PUBLISHED.value,
            AiToolVersion.is_deleted.is_(False),
        )
        stmt = self.apply_ai_filter(stmt, AiToolVersion, ctx)
        return self.db.scalar(stmt)

    def next_version_number(self, ctx: TenantContext, tool_id: UUID) -> int:
        rows = self.list_by_tool(ctx, tool_id)
        if not rows:
            return 1
        return max(r.version_number for r in rows) + 1

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "version_number",
        sort_dir: str = "asc",
        include_archived: bool = False,
        tool_id: UUID | None = None,
    ) -> PageResult:
        stmt = select(AiToolVersion).where(AiToolVersion.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(AiToolVersion.is_deleted.is_(False))
        if status:
            stmt = stmt.where(AiToolVersion.status == status)
        if tool_id:
            stmt = stmt.where(AiToolVersion.tool_id == tool_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                AiToolVersion.version_code.ilike(like) | AiToolVersion.version_label.ilike(like)
            )
        stmt = self.apply_ai_filter(stmt, AiToolVersion, ctx)
        return self.paginate_sorted(
            stmt,
            AiToolVersion,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> AiToolVersion:
        row = AiToolVersion(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> AiToolVersion | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> AiToolVersion | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> AiToolVersion | None:
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
