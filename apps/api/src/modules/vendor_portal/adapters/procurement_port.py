"""Procurement port — UUID refs only; no proc_* ORM writes."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class VendorPortalProcurementAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_rfq_ref(self, ctx: TenantContext, rfq_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return rfq_id

    def resolve_po_ref(self, ctx: TenantContext, po_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return po_id

    def resolve_quote_ref(self, ctx: TenantContext, quote_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return quote_id

    def resolve_invoice_ref(self, ctx: TenantContext, invoice_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return invoice_id
