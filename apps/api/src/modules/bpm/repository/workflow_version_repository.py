"""BPM BpmWorkflowVersion repository — Phase 1.5."""

from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from modules.bpm.domain.enums import VersionStatus
from modules.bpm.models import BpmWorkflowVersion
from modules.bpm.repository.base import BpmScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext


class WorkflowVersionRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowVersion | None:
        stmt = select(BpmWorkflowVersion).where(
            BpmWorkflowVersion.id == row_id,
            BpmWorkflowVersion.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowVersion, ctx)
        return self.db.scalar(stmt)

    def list_by_definition(self, ctx: TenantContext, definition_id: UUID):
        stmt = select(BpmWorkflowVersion).where(
            BpmWorkflowVersion.definition_id == definition_id,
            BpmWorkflowVersion.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowVersion, ctx)
        stmt = stmt.order_by(BpmWorkflowVersion.version_number.desc())
        return list(self.db.scalars(stmt).all())

    def get_published(self, ctx: TenantContext, definition_id: UUID) -> BpmWorkflowVersion | None:
        stmt = select(BpmWorkflowVersion).where(
            BpmWorkflowVersion.definition_id == definition_id,
            BpmWorkflowVersion.status == VersionStatus.PUBLISHED.value,
            BpmWorkflowVersion.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowVersion, ctx)
        return self.db.scalar(stmt)

    def count_published(self, ctx: TenantContext, definition_id: UUID) -> int:
        stmt = select(func.count()).select_from(BpmWorkflowVersion).where(
            BpmWorkflowVersion.definition_id == definition_id,
            BpmWorkflowVersion.status == VersionStatus.PUBLISHED.value,
            BpmWorkflowVersion.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowVersion, ctx)
        return int(self.db.scalar(stmt) or 0)

    def count_by_status(self, ctx: TenantContext, company_id: UUID, status: str) -> int:
        stmt = select(func.count()).select_from(BpmWorkflowVersion).where(
            BpmWorkflowVersion.company_id == company_id,
            BpmWorkflowVersion.status == status,
            BpmWorkflowVersion.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowVersion, ctx)
        return int(self.db.scalar(stmt) or 0)

    def next_version_number(self, ctx: TenantContext, definition_id: UUID) -> int:
        rows = self.list_by_definition(ctx, definition_id)
        if not rows:
            return 1
        return max(r.version_number for r in rows) + 1

    def create(self, ctx: TenantContext, **fields) -> BpmWorkflowVersion:
        row = BpmWorkflowVersion(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> BpmWorkflowVersion | None:
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
