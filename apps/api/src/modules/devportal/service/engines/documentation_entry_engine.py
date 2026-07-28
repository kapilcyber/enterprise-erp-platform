"""Documentation entry lifecycle — Draft → Published → Retired."""

from datetime import datetime, timezone

from modules.devportal.domain.enums import (
    DOCUMENTATION_ENTRY_TYPE_VALUES,
    DocumentationEntryStatus,
)
from modules.devportal.domain.exceptions import (
    DocumentationEntryTypeError,
    InvalidDocumentationEntryState,
    PublishedDocumentationImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DocumentationEntryEngine:
    def assert_entry_type(self, entry_type: str) -> None:
        if entry_type not in DOCUMENTATION_ENTRY_TYPE_VALUES:
            raise DocumentationEntryTypeError(
                f"entry_type must be one of {DOCUMENTATION_ENTRY_TYPE_VALUES}"
            )

    def assert_editable(self, row) -> None:
        if row.status == DocumentationEntryStatus.PUBLISHED.value:
            raise PublishedDocumentationImmutable()
        if row.status == DocumentationEntryStatus.RETIRED.value:
            raise InvalidDocumentationEntryState("Retired documentation is read-only")
        if row.status != DocumentationEntryStatus.DRAFT.value:
            raise InvalidDocumentationEntryState("Only draft documentation is editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != DocumentationEntryStatus.DRAFT.value:
            raise InvalidDocumentationEntryState("Only draft documentation can be published")
        row.status = DocumentationEntryStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {
            DocumentationEntryStatus.PUBLISHED.value,
            DocumentationEntryStatus.DRAFT.value,
        }:
            raise InvalidDocumentationEntryState(
                "Only draft or published documentation can be retired"
            )
        row.status = DocumentationEntryStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
