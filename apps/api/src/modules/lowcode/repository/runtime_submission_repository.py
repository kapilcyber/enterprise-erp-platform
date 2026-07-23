"""Low-Code LcRuntimeSubmission repository — Phase 4."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.models import LcRuntimeSubmission
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class RuntimeSubmissionRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcRuntimeSubmission | None:
        stmt = select(LcRuntimeSubmission).where(
            LcRuntimeSubmission.id == row_id,
            LcRuntimeSubmission.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcRuntimeSubmission, ctx)
        return self.db.scalar(stmt)

    def get_by_correlation(
        self, ctx: TenantContext, company_id: UUID, correlation_id: str
    ) -> LcRuntimeSubmission | None:
        stmt = select(LcRuntimeSubmission).where(
            LcRuntimeSubmission.company_id == company_id,
            LcRuntimeSubmission.correlation_id == correlation_id,
            LcRuntimeSubmission.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcRuntimeSubmission, ctx)
        return self.db.scalar(stmt)

    def list_by_module_entity(
        self, ctx: TenantContext, module_code: str, entity_id: UUID
    ):
        stmt = (
            select(LcRuntimeSubmission)
            .where(
                LcRuntimeSubmission.module_code == module_code,
                LcRuntimeSubmission.entity_id == entity_id,
                LcRuntimeSubmission.is_deleted.is_(False),
            )
            .order_by(LcRuntimeSubmission.created_at.desc())
        )
        stmt = self.apply_lowcode_filter(stmt, LcRuntimeSubmission, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> LcRuntimeSubmission:
        row = LcRuntimeSubmission(
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
    ) -> LcRuntimeSubmission | None:
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
