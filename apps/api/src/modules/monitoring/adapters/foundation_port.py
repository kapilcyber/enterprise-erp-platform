"""Foundation Auth / RBAC port — consume-only (Phase 0).

Monitoring never writes Foundation ORM models. UUID references only.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class MonitoringFoundationAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_role_ref(self, ctx: TenantContext, role_id: UUID | None) -> UUID | None:
        """Pass-through UUID role reference — no peer ORM load."""
        _ = (ctx, self._db)
        return role_id

    def resolve_user_ref(self, ctx: TenantContext, user_id: UUID | None) -> UUID | None:
        """Pass-through Foundation user UUID — Auth SoR remains Foundation."""
        _ = (ctx, self._db)
        return user_id
