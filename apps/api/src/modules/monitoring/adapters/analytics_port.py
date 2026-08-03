"""Analytics export port — UUID pass-through only, no peer ORM (Phase 0).

Analytics remains enterprise reporting SoR; Monitoring does not own warehouses.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class MonitoringAnalyticsAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_export_ref(self, ctx: TenantContext, export_id: UUID | None) -> UUID | None:
        """Pass-through Analytics export UUID — no Analytics ORM load."""
        _ = (ctx, self._db)
        return export_id
