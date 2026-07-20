"""Document port — document UUID only; no Document ORM writes."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class VendorPortalDocumentAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_document_uuid(self, ctx: TenantContext, document_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return document_id
