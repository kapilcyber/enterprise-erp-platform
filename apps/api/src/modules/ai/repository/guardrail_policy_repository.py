"""AiGuardrailPolicy repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.ai.domain.value_objects import PageResult
from modules.ai.models.guardrail_policy import AiGuardrailPolicy
from modules.ai.repository.base import AiScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {"policy_code", "policy_name", "status", "created_at", "updated_at"}


class GuardrailPolicyRepository(AiScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiGuardrailPolicy | None:
        stmt = select(AiGuardrailPolicy).where(
            AiGuardrailPolicy.id == row_id,
            AiGuardrailPolicy.is_deleted.is_(False),
        )
        stmt = self.apply_ai_filter(stmt, AiGuardrailPolicy, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> AiGuardrailPolicy | None:
        stmt = select(AiGuardrailPolicy).where(AiGuardrailPolicy.id == row_id)
        stmt = self.apply_ai_filter(stmt, AiGuardrailPolicy, ctx)
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
        sort_by: str | None = "policy_name",
        sort_dir: str = "asc",
        include_archived: bool = False,
    ) -> PageResult:
        stmt = select(AiGuardrailPolicy).where(AiGuardrailPolicy.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(AiGuardrailPolicy.is_deleted.is_(False))
        if status:
            stmt = stmt.where(AiGuardrailPolicy.status == status)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(AiGuardrailPolicy.policy_name.ilike(like) | AiGuardrailPolicy.policy_code.ilike(like))
        stmt = self.apply_ai_filter(stmt, AiGuardrailPolicy, ctx)
        return self.paginate_sorted(
            stmt,
            AiGuardrailPolicy,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> AiGuardrailPolicy:
        row = AiGuardrailPolicy(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> AiGuardrailPolicy | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> AiGuardrailPolicy | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> AiGuardrailPolicy | None:
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
