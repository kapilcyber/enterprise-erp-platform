"""Foundation Security port — consume-only (Phase 0).

AI Platform never writes Foundation ORM models. Cross-module reads/writes
use service contracts and UUID references only (Architecture Lock / no peer ORM).
"""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class AiFoundationAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_role_ref(self, ctx: TenantContext, role_id: UUID | None) -> UUID | None:
        """Pass-through UUID role reference — no peer ORM load in Phase 0."""
        _ = (ctx, self._db)
        return role_id
