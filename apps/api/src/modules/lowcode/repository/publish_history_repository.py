"""Low-Code LcPublishHistory repository — Phase 4 append-oriented."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.models import LcPublishHistory
from modules.lowcode.repository.base import LowcodeScopedRepository


class PublishHistoryRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcPublishHistory | None:
        stmt = select(LcPublishHistory).where(
            LcPublishHistory.id == row_id,
            LcPublishHistory.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcPublishHistory, ctx)
        return self.db.scalar(stmt)

    def list_by_form_definition(self, ctx: TenantContext, form_definition_id: UUID):
        stmt = (
            select(LcPublishHistory)
            .where(
                LcPublishHistory.form_definition_id == form_definition_id,
                LcPublishHistory.is_deleted.is_(False),
            )
            .order_by(LcPublishHistory.occurred_at.desc())
        )
        stmt = self.apply_lowcode_filter(stmt, LcPublishHistory, ctx)
        return list(self.db.scalars(stmt).all())

    def list_by_page_definition(self, ctx: TenantContext, page_definition_id: UUID):
        stmt = (
            select(LcPublishHistory)
            .where(
                LcPublishHistory.page_definition_id == page_definition_id,
                LcPublishHistory.is_deleted.is_(False),
            )
            .order_by(LcPublishHistory.occurred_at.desc())
        )
        stmt = self.apply_lowcode_filter(stmt, LcPublishHistory, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> LcPublishHistory:
        row = LcPublishHistory(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row
