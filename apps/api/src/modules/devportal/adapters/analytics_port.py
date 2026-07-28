"""Analytics port — UUID pass-through only, no peer ORM (Phase 0)."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class DevportalAnalyticsAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_report_ref(self, ctx: TenantContext, report_id: UUID | None) -> UUID | None:
        """Pass-through UUID analytics report reference — no Analytics ORM load."""
        _ = (ctx, self._db)
        return report_id
