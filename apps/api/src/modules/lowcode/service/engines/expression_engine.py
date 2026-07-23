"""Expression lifecycle engine — UI expressions only (Phase 2C)."""

from datetime import datetime, timezone

from modules.lowcode.domain.enums import EXPRESSION_KIND_VALUES, VersionStatus
from modules.lowcode.domain.exceptions import (
    InvalidExpressionState,
    PublishedExpressionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ExpressionEngine:
    def assert_valid_kind(self, expression_kind: str | None) -> None:
        if not expression_kind or expression_kind not in EXPRESSION_KIND_VALUES:
            raise InvalidExpressionState(f"Unsupported expression kind: {expression_kind}")

    def assert_body(self, expression_body: str | None) -> None:
        if expression_body is None or not str(expression_body).strip():
            raise InvalidExpressionState("expression_body is required")

    def assert_editable(self, row) -> None:
        if row.status == VersionStatus.PUBLISHED.value:
            raise PublishedExpressionImmutable()
        if row.status == VersionStatus.RETIRED.value:
            raise InvalidExpressionState("Retired expressions are read-only")
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidExpressionState("Only draft expressions are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidExpressionState("Only draft expressions can be published")
        self.assert_body(row.expression_body)
        self.assert_valid_kind(row.expression_kind)
        row.status = VersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {VersionStatus.PUBLISHED.value, VersionStatus.DRAFT.value}:
            raise InvalidExpressionState("Only draft or published expressions can be retired")
        row.status = VersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
