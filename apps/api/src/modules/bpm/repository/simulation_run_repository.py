"""Simulation run repository — Phase 5."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.bpm.models import BpmSimulationRun
from modules.bpm.repository.base import BpmScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext


class SimulationRunRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmSimulationRun | None:
        stmt = select(BpmSimulationRun).where(
            BpmSimulationRun.id == row_id,
            BpmSimulationRun.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmSimulationRun, ctx)
        return self.db.scalar(stmt)

    def list_by_version(self, ctx: TenantContext, version_id: UUID) -> list[BpmSimulationRun]:
        stmt = (
            select(BpmSimulationRun)
            .where(
                BpmSimulationRun.version_id == version_id,
                BpmSimulationRun.is_deleted.is_(False),
            )
            .order_by(BpmSimulationRun.created_at.desc())
        )
        stmt = self.apply_bpm_filter(stmt, BpmSimulationRun, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> BpmSimulationRun:
        row = BpmSimulationRun(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> BpmSimulationRun | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> BpmSimulationRun | None:
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
