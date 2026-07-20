"""Analytics port — read-only UUID refs."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class VendorPortalAnalyticsAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_report_ref(self, ctx: TenantContext, report_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return report_id
