"""RuntimeSubmission validation engine — Phase 4 correlation only."""

from uuid import UUID

from modules.lowcode.domain.enums import SUBMISSION_STATUS_VALUES
from modules.lowcode.domain.exceptions import InvalidRuntimeSubmissionState


class RuntimeSubmissionEngine:
    def assert_valid_status(self, status: str | None) -> None:
        if not status or status not in SUBMISSION_STATUS_VALUES:
            raise InvalidRuntimeSubmissionState(
                f"Unsupported submission_status: {status}"
            )

    def assert_module_context(self, module_code: str | None, entity_id: UUID | None) -> None:
        if not module_code or not str(module_code).strip():
            raise InvalidRuntimeSubmissionState("module_code is required")
        if entity_id is None:
            raise InvalidRuntimeSubmissionState("entity_id is required")

    def assert_correlation_id(self, correlation_id: str | None) -> None:
        if not correlation_id or not str(correlation_id).strip():
            raise InvalidRuntimeSubmissionState("correlation_id is required")

    def assert_version_target(
        self,
        *,
        form_version_id: UUID | None,
        page_version_id: UUID | None,
    ) -> None:
        if form_version_id is None and page_version_id is None:
            raise InvalidRuntimeSubmissionState(
                "At least one of form_version_id or page_version_id is required"
            )
