"""MonServicePolicyAssignment repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.models.service_policy_assignment import MonServicePolicyAssignment
from modules.monitoring.repository.base import MonitoringScopedRepository, utcnow

_SORT = {"assignment_code", "created_at", "effective_from", "status", "updated_at"}


class ServicePolicyAssignmentRepository(MonitoringScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> MonServicePolicyAssignment | None:
        stmt = select(MonServicePolicyAssignment).where(
            MonServicePolicyAssignment.id == row_id,
            MonServicePolicyAssignment.is_deleted.is_(False),
        )
        stmt = self.apply_monitoring_filter(stmt, MonServicePolicyAssignment, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> MonServicePolicyAssignment | None:  # noqa: E501
        stmt = select(MonServicePolicyAssignment).where(MonServicePolicyAssignment.id == row_id)
        stmt = self.apply_monitoring_filter(stmt, MonServicePolicyAssignment, ctx)
        return self.db.scalar(stmt)

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        search: str | None = None,
        service_id: UUID | None = None,
        policy_version_id: UUID | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "created_at",
        sort_dir: str = "asc",
        include_archived: bool = False,
    ) -> PageResult:
        stmt = select(MonServicePolicyAssignment).where(
            MonServicePolicyAssignment.company_id == company_id,
        )
        if not include_archived:
            stmt = stmt.where(MonServicePolicyAssignment.is_deleted.is_(False))
        if status:
            stmt = stmt.where(MonServicePolicyAssignment.status == status)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(MonServicePolicyAssignment.assignment_code.ilike(like))

        if service_id:
            stmt = stmt.where(MonServicePolicyAssignment.service_id == service_id)

        if policy_version_id:
            stmt = stmt.where(MonServicePolicyAssignment.policy_version_id == policy_version_id)
        stmt = self.apply_monitoring_filter(stmt, MonServicePolicyAssignment, ctx)
        return self.paginate_sorted(
            stmt,
            MonServicePolicyAssignment,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> MonServicePolicyAssignment:
        row = MonServicePolicyAssignment(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> MonServicePolicyAssignment | None:  # noqa: E501
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> MonServicePolicyAssignment | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> MonServicePolicyAssignment | None:
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
