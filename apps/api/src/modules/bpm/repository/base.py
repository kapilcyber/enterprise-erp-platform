"""BPM scoped repository base — Phase 1.5 pagination / sort helpers."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from core.exceptions import ForbiddenException
from modules.bpm.domain.value_objects import PageResult
from modules.foundation.domain.value_objects import TenantContext
from modules.organization.repository.base import OrgScopedRepository


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BpmScopedRepository(OrgScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    @staticmethod
    def apply_bpm_filter(stmt, model, ctx: TenantContext, *, branch_scoped: bool = False):
        stmt = BpmScopedRepository.apply_tenant_filter(stmt, model, ctx)
        if ctx.company_id and ctx.user_type not in {"super_admin", "tenant_admin"}:
            stmt = stmt.where(model.company_id == ctx.company_id)
        if (
            branch_scoped
            and ctx.branch_id
            and ctx.user_type not in {"super_admin", "tenant_admin"}
            and hasattr(model, "branch_id")
        ):
            stmt = stmt.where(model.branch_id == ctx.branch_id)
        return stmt

    @staticmethod
    def resolve_company_id(ctx: TenantContext, company_id: UUID | None) -> UUID:
        if company_id is not None:
            BpmScopedRepository.ensure_company_access(ctx, company_id)
            return company_id
        if ctx.company_id is None:
            raise ForbiddenException("Company context required")
        return ctx.company_id

    def paginate_sorted(
        self,
        stmt,
        model,
        *,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = None,
        sort_dir: str = "asc",
        allowed_sort: set[str] | None = None,
    ) -> PageResult:
        allowed = allowed_sort or set()
        col_name = sort_by if sort_by in allowed else None
        if col_name and hasattr(model, col_name):
            col = getattr(model, col_name)
            stmt = stmt.order_by(desc(col) if sort_dir == "desc" else asc(col))
        count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
        total = int(self.db.scalar(count_stmt) or 0)
        offset = max(page - 1, 0) * page_size
        items = list(self.db.scalars(stmt.offset(offset).limit(page_size)).all())
        return PageResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            sort_by=col_name,
            sort_dir=sort_dir if col_name else "asc",
        )
