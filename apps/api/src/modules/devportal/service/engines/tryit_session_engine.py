"""Try-it session engine — metadata only; fail closed on invoke misuse."""

from datetime import datetime, timezone

from modules.devportal.domain.enums import TryitSessionStatus
from modules.devportal.domain.exceptions import InvalidTryitSessionState, TryitInvokeForbidden


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TryitSessionEngine:
    def assert_metadata_only(self) -> None:
        """Fail closed if treated as live gateway invoke."""
        raise TryitInvokeForbidden()

    def close(self, row) -> None:
        if row.status != TryitSessionStatus.ACTIVE.value:
            raise InvalidTryitSessionState("Only active try-it sessions can be closed")
        row.status = TryitSessionStatus.CLOSED.value
        row.closed_at = _utcnow()

    def expire(self, row) -> None:
        if row.status != TryitSessionStatus.ACTIVE.value:
            raise InvalidTryitSessionState("Only active try-it sessions can expire")
        row.status = TryitSessionStatus.EXPIRED.value
        row.closed_at = _utcnow()
