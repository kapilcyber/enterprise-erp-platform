"""Quality port — NCR / inspection UUID only; no qm_* ORM writes."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class VendorPortalQualityAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_ncr_ref(self, ctx: TenantContext, ncr_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return ncr_id

    def resolve_inspection_ref(self, ctx: TenantContext, inspection_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return inspection_id
