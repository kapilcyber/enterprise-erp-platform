"""Foundation Notification port — consume-only (Phase 0).

Monitoring emits notification requests; Foundation Notification remains delivery SoR (C-05).
"""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class MonitoringNotificationAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_channel_ref(
        self, ctx: TenantContext, notification_channel_ref: UUID | None
    ) -> UUID | None:
        """Pass-through notification channel UUID — no peer ORM load."""
        _ = (ctx, self._db)
        return notification_channel_ref
