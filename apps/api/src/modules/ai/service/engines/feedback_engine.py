"""Feedback lifecycle engine — captured / reviewed / closed."""

from datetime import datetime, timezone
from uuid import UUID

from modules.ai.domain.enums import FeedbackStatus
from modules.ai.domain.exceptions import InvalidFeedbackState


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class FeedbackEngine:
    def assert_editable(self, row) -> None:
        if row.status == FeedbackStatus.CLOSED.value:
            raise InvalidFeedbackState("Closed feedback is read-only")

    def capture(self, row) -> None:
        if row.status != FeedbackStatus.CAPTURED.value:
            raise InvalidFeedbackState("Feedback is already past captured state")

    def review(self, row, *, user_id: UUID) -> None:
        if row.status != FeedbackStatus.CAPTURED.value:
            raise InvalidFeedbackState("Only captured feedback can be reviewed")
        row.status = FeedbackStatus.REVIEWED.value
        row.reviewed_at = _utcnow()
        row.reviewed_by = user_id

    def close(self, row, *, user_id: UUID) -> None:
        if row.status not in {
            FeedbackStatus.CAPTURED.value,
            FeedbackStatus.REVIEWED.value,
        }:
            raise InvalidFeedbackState("Only captured or reviewed feedback can be closed")
        row.status = FeedbackStatus.CLOSED.value
        row.closed_at = _utcnow()
        row.closed_by = user_id
