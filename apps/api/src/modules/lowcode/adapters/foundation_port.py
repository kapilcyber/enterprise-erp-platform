"""Foundation Security port — consume-only."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class LowcodeFoundationAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_role_ref(self, ctx: TenantContext, role_id: UUID | None) -> UUID | None:
        _ = (ctx, self._db)
        return role_id
