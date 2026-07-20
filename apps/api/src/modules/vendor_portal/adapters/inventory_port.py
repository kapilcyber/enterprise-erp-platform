"""Inventory port — receipt UUID only; ASN envelope never writes inventory."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class VendorPortalInventoryAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_receipt_ref(self, ctx: TenantContext, receipt_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return receipt_id
