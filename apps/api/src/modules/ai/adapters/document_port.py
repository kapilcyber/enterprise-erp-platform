"""Document port — UUID pass-through only, no peer ORM."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class AiDocumentAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_document_ref(self, ctx: TenantContext, document_id: UUID | None) -> UUID | None:
        """Pass-through UUID document reference — no Document ORM load."""
        _ = (ctx, self._db)
        return document_id
