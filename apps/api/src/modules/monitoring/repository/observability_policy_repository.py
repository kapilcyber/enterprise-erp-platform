"""MonObservabilityPolicy repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.models.observability_policy import MonObservabilityPolicy
from modules.monitoring.repository.base import MonitoringScopedRepository, utcnow

_SORT = {"created_at", "policy_code", "policy_name", "scope_level", "status", "updated_at"}


class ObservabilityPolicyRepository(MonitoringScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> MonObservabilityPolicy | None:
        stmt = select(MonObservabilityPolicy).where(
            MonObservabilityPolicy.id == row_id,
            MonObservabilityPolicy.is_deleted.is_(False),
        )
        stmt = self.apply_monitoring_filter(stmt, MonObservabilityPolicy, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> MonObservabilityPolicy | None:  # noqa: E501
        stmt = select(MonObservabilityPolicy).where(MonObservabilityPolicy.id == row_id)
        stmt = self.apply_monitoring_filter(stmt, MonObservabilityPolicy, ctx)
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
        stmt = select(MonObservabilityPolicy).where(MonObservabilityPolicy.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(MonObservabilityPolicy.is_deleted.is_(False))
        if status:
            stmt = stmt.where(MonObservabilityPolicy.status == status)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                MonObservabilityPolicy.policy_name.ilike(like) |
                MonObservabilityPolicy.policy_code.ilike(like)
            )
        stmt = self.apply_monitoring_filter(stmt, MonObservabilityPolicy, ctx)
        return self.paginate_sorted(
            stmt,
            MonObservabilityPolicy,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> MonObservabilityPolicy:
        row = MonObservabilityPolicy(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> MonObservabilityPolicy | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> MonObservabilityPolicy | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> MonObservabilityPolicy | None:
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
