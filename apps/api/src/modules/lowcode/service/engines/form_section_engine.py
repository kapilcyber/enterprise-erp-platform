"""Form section lifecycle engine — Phase 2A."""

from modules.lowcode.domain.enums import SectionStatus
from modules.lowcode.domain.exceptions import InvalidSectionState


class FormSectionEngine:
    def assert_display_order(self, display_order: int | None) -> None:
        if display_order is not None and display_order < 0:
            raise InvalidSectionState("display_order must be >= 0")

    def activate(self, row) -> None:
        if row.status == SectionStatus.ACTIVE.value:
            raise InvalidSectionState("Section already active")
        row.status = SectionStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status != SectionStatus.ACTIVE.value:
            raise InvalidSectionState("Only active sections can be deactivated")
        row.status = SectionStatus.INACTIVE.value
