"""BPM port — UUID pass-through for bpm_definition_id (HITL hook metadata only)."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class AiBpmAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_bpm_definition_ref(
        self, ctx: TenantContext, bpm_definition_id: UUID | None
    ) -> UUID | None:
        """Pass-through UUID BPM definition reference — no peer ORM load."""
        _ = (ctx, self._db)
        return bpm_definition_id
