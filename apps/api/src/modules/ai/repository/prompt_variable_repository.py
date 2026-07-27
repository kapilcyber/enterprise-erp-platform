"""AiPromptVariable repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.ai.domain.value_objects import PageResult
from modules.ai.models.prompt_variable import AiPromptVariable
from modules.ai.repository.base import AiScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {"variable_code", "variable_name", "data_type", "created_at", "updated_at"}


class PromptVariableRepository(AiScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiPromptVariable | None:
        stmt = select(AiPromptVariable).where(
            AiPromptVariable.id == row_id,
            AiPromptVariable.is_deleted.is_(False),
        )
        stmt = self.apply_ai_filter(stmt, AiPromptVariable, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> AiPromptVariable | None:
        stmt = select(AiPromptVariable).where(AiPromptVariable.id == row_id)
        stmt = self.apply_ai_filter(stmt, AiPromptVariable, ctx)
        return self.db.scalar(stmt)


    def list_by_version(self, ctx: TenantContext, prompt_version_id: UUID) -> list[AiPromptVariable]:
        stmt = (
            select(AiPromptVariable)
            .where(
                AiPromptVariable.prompt_version_id == prompt_version_id,
                AiPromptVariable.is_deleted.is_(False),
            )
            .order_by(AiPromptVariable.variable_name, AiPromptVariable.variable_code)
        )
        stmt = self.apply_ai_filter(stmt, AiPromptVariable, ctx)
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
        sort_by: str | None = "variable_name",
        sort_dir: str = "asc",
        include_archived: bool = False,
        prompt_version_id: UUID | None = None
    ) -> PageResult:
        stmt = select(AiPromptVariable).where(AiPromptVariable.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(AiPromptVariable.is_deleted.is_(False))
        if status:
            stmt = stmt.where(AiPromptVariable.status == status)
        if prompt_version_id:
            stmt = stmt.where(AiPromptVariable.prompt_version_id == prompt_version_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(AiPromptVariable.variable_name.ilike(like) | AiPromptVariable.variable_code.ilike(like))
        stmt = self.apply_ai_filter(stmt, AiPromptVariable, ctx)
        return self.paginate_sorted(
            stmt,
            AiPromptVariable,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> AiPromptVariable:
        row = AiPromptVariable(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> AiPromptVariable | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> AiPromptVariable | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> AiPromptVariable | None:
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
