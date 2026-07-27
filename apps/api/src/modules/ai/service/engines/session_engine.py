"""Session lifecycle engine — open → active → close / expire."""

from datetime import datetime, timezone

from modules.ai.domain.enums import SessionStatus
from modules.ai.domain.exceptions import InvalidSessionState


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SessionEngine:
    def activate(self, row) -> None:
        if row.status not in {SessionStatus.OPEN.value, SessionStatus.ACTIVE.value}:
            raise InvalidSessionState("Only open sessions can be activated")
        if row.status == SessionStatus.ACTIVE.value:
            raise InvalidSessionState("Session already active")
        row.status = SessionStatus.ACTIVE.value

    def close(self, row) -> None:
        if row.status in {SessionStatus.CLOSED.value, SessionStatus.EXPIRED.value}:
            raise InvalidSessionState("Session already closed or expired")
        row.status = SessionStatus.CLOSED.value
        row.closed_at = _utcnow()

    def expire(self, row) -> None:
        if row.status in {SessionStatus.CLOSED.value, SessionStatus.EXPIRED.value}:
            raise InvalidSessionState("Session already closed or expired")
        row.status = SessionStatus.EXPIRED.value
        row.closed_at = _utcnow()
