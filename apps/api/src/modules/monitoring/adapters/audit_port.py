"""Foundation Audit port — consume-only (Phase 0).

Monitoring emits audit events; Foundation Audit remains warehouse SoR (C-06).
"""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class MonitoringAuditAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_actor_ref(self, ctx: TenantContext, actor_id: UUID | None) -> UUID | None:
        """Pass-through actor UUID for audit emission — no peer ORM load."""
        _ = (ctx, self._db)
        return actor_id
