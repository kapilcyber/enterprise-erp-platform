"""PublishHistory validation engine — Phase 4 append-only metadata."""

from uuid import UUID

from modules.lowcode.domain.enums import (
    ARTIFACT_KIND_VALUES,
    PUBLISH_HISTORY_ACTION_VALUES,
    ArtifactKind,
)
from modules.lowcode.domain.exceptions import InvalidPublishHistoryState


class PublishHistoryEngine:
    def assert_valid_action(self, action: str | None) -> None:
        if not action or action not in PUBLISH_HISTORY_ACTION_VALUES:
            raise InvalidPublishHistoryState(f"Unsupported publish history action: {action}")

    def assert_valid_artifact_kind(self, artifact_kind: str | None) -> None:
        if not artifact_kind or artifact_kind not in ARTIFACT_KIND_VALUES:
            raise InvalidPublishHistoryState(
                f"Unsupported artifact_kind: {artifact_kind}"
            )

    def normalize_targets(
        self,
        *,
        artifact_kind: str,
        form_definition_id: UUID | None,
        page_definition_id: UUID | None,
    ) -> dict:
        self.assert_valid_artifact_kind(artifact_kind)
        if artifact_kind == ArtifactKind.FORM.value:
            if form_definition_id is None:
                raise InvalidPublishHistoryState(
                    "form_definition_id is required for form publish history"
                )
            if page_definition_id is not None:
                raise InvalidPublishHistoryState(
                    "form publish history must not set page_definition_id"
                )
            return {
                "form_definition_id": form_definition_id,
                "page_definition_id": None,
            }
        if page_definition_id is None:
            raise InvalidPublishHistoryState(
                "page_definition_id is required for page publish history"
            )
        if form_definition_id is not None:
            raise InvalidPublishHistoryState(
                "page publish history must not set form_definition_id"
            )
        return {
            "form_definition_id": None,
            "page_definition_id": page_definition_id,
        }
