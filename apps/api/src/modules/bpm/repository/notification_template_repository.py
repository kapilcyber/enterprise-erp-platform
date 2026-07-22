"""Notification template repository — Phase 3B."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.bpm.models import BpmNotificationTemplate
from modules.bpm.repository.base import BpmScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext


class NotificationTemplateRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmNotificationTemplate | None:
        stmt = select(BpmNotificationTemplate).where(
            BpmNotificationTemplate.id == row_id,
            BpmNotificationTemplate.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmNotificationTemplate, ctx)
        return self.db.scalar(stmt)

    def list_by_version(
        self, ctx: TenantContext, version_id: UUID
    ) -> list[BpmNotificationTemplate]:
        stmt = (
            select(BpmNotificationTemplate)
            .where(
                BpmNotificationTemplate.version_id == version_id,
                BpmNotificationTemplate.is_deleted.is_(False),
            )
            .order_by(BpmNotificationTemplate.template_name)
        )
        stmt = self.apply_bpm_filter(stmt, BpmNotificationTemplate, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> BpmNotificationTemplate:
        row = BpmNotificationTemplate(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(
        self, ctx: TenantContext, row_id: UUID, **fields
    ) -> BpmNotificationTemplate | None:
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

    def soft_delete(
        self, ctx: TenantContext, row_id: UUID
    ) -> BpmNotificationTemplate | None:
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
