"""Business rule repository — Phase 2B."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.bpm.models import BpmBusinessRule
from modules.bpm.repository.base import BpmScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext


class BusinessRuleRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmBusinessRule | None:
        stmt = select(BpmBusinessRule).where(
            BpmBusinessRule.id == row_id,
            BpmBusinessRule.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmBusinessRule, ctx)
        return self.db.scalar(stmt)

    def list_by_version(self, ctx: TenantContext, version_id: UUID) -> list[BpmBusinessRule]:
        stmt = (
            select(BpmBusinessRule)
            .where(
                BpmBusinessRule.version_id == version_id,
                BpmBusinessRule.is_deleted.is_(False),
            )
            .order_by(BpmBusinessRule.priority, BpmBusinessRule.rule_name)
        )
        stmt = self.apply_bpm_filter(stmt, BpmBusinessRule, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> BpmBusinessRule:
        row = BpmBusinessRule(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> BpmBusinessRule | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> BpmBusinessRule | None:
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
