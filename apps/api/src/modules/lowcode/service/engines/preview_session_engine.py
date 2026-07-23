"""PreviewSession validation engine — Phase 4 design-time only."""

from datetime import datetime, timezone
from uuid import UUID

from modules.lowcode.domain.enums import (
    PREVIEW_MODE_VALUES,
    PREVIEW_SESSION_STATUS_VALUES,
    PreviewMode,
    PreviewSessionStatus,
    VersionStatus,
)
from modules.lowcode.domain.exceptions import InvalidPreviewSessionState


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PreviewSessionEngine:
    def assert_valid_mode(self, preview_mode: str | None) -> None:
        if not preview_mode or preview_mode not in PREVIEW_MODE_VALUES:
            raise InvalidPreviewSessionState(f"Unsupported preview_mode: {preview_mode}")

    def assert_version_target(
        self,
        *,
        form_version_id: UUID | None,
        page_version_id: UUID | None,
    ) -> None:
        if form_version_id is None and page_version_id is None:
            raise InvalidPreviewSessionState(
                "At least one of form_version_id or page_version_id is required"
            )

    def assert_mode_matches_version(self, preview_mode: str, version_status: str) -> None:
        if (
            preview_mode == PreviewMode.DRAFT.value
            and version_status != VersionStatus.DRAFT.value
        ):
            raise InvalidPreviewSessionState(
                "draft preview requires a draft form/page version"
            )
        if (
            preview_mode == PreviewMode.PUBLISHED.value
            and version_status != VersionStatus.PUBLISHED.value
        ):
            raise InvalidPreviewSessionState(
                "published preview requires a published form/page version"
            )

    def assert_active(self, row) -> None:
        if row.status != PreviewSessionStatus.ACTIVE.value:
            raise InvalidPreviewSessionState("Preview session is not active")
        if row.expires_at is not None and row.expires_at <= _utcnow():
            raise InvalidPreviewSessionState("Preview session has expired")

    def expire(self, row) -> None:
        if row.status != PreviewSessionStatus.ACTIVE.value:
            raise InvalidPreviewSessionState("Only active preview sessions can expire")
        row.status = PreviewSessionStatus.EXPIRED.value

    def close(self, row) -> None:
        if row.status not in {
            PreviewSessionStatus.ACTIVE.value,
            PreviewSessionStatus.EXPIRED.value,
        }:
            raise InvalidPreviewSessionState("Preview session already closed")
        row.status = PreviewSessionStatus.CLOSED.value
        row.closed_at = _utcnow()

    def assert_valid_status(self, status: str | None) -> None:
        if status is not None and status not in PREVIEW_SESSION_STATUS_VALUES:
            raise InvalidPreviewSessionState(f"Unsupported preview status: {status}")
