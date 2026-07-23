"""EventHandler validation engine — Phase 3A metadata only (no execution)."""

from uuid import UUID

from modules.lowcode.domain.enums import (
    BINDING_TARGET_TYPE_VALUES,
    EVENT_TYPE_VALUES,
    BindingTargetType,
    EventType,
)
from modules.lowcode.domain.exceptions import InvalidEventHandlerState


class EventHandlerEngine:
    def assert_valid_event_type(self, event_type: str | None) -> None:
        if not event_type or event_type not in EVENT_TYPE_VALUES:
            raise InvalidEventHandlerState(f"Unsupported event_type: {event_type}")

    def assert_custom_name(self, event_type: str, custom_event_name: str | None) -> None:
        if event_type == EventType.CUSTOM.value:
            if not custom_event_name or not str(custom_event_name).strip():
                raise InvalidEventHandlerState(
                    "custom_event_name is required when event_type is custom"
                )
        elif custom_event_name:
            raise InvalidEventHandlerState(
                "custom_event_name is only allowed when event_type is custom"
            )

    def assert_valid_target_type(self, target_type: str | None) -> None:
        if not target_type or target_type not in BINDING_TARGET_TYPE_VALUES:
            raise InvalidEventHandlerState(f"Unsupported target_type: {target_type}")

    def assert_execution_order(self, execution_order: int | None) -> None:
        if execution_order is not None and execution_order < 0:
            raise InvalidEventHandlerState("execution_order must be >= 0")

    def normalize_targets(
        self,
        *,
        target_type: str,
        form_version_id: UUID | None,
        section_id: UUID | None,
        field_id: UUID | None,
        page_version_id: UUID | None,
    ) -> dict:
        self.assert_valid_target_type(target_type)
        if target_type == BindingTargetType.FORM_VERSION.value:
            if form_version_id is None:
                raise InvalidEventHandlerState(
                    "form_version_id is required for form_version targets"
                )
            if section_id or field_id or page_version_id:
                raise InvalidEventHandlerState(
                    "form_version targets must not set section/field/page_version"
                )
            return {
                "form_version_id": form_version_id,
                "section_id": None,
                "field_id": None,
                "page_version_id": None,
            }
        if target_type == BindingTargetType.SECTION.value:
            if section_id is None or form_version_id is None:
                raise InvalidEventHandlerState(
                    "section_id and form_version_id are required for section targets"
                )
            if field_id or page_version_id:
                raise InvalidEventHandlerState(
                    "section targets must not set field_id or page_version_id"
                )
            return {
                "form_version_id": form_version_id,
                "section_id": section_id,
                "field_id": None,
                "page_version_id": None,
            }
        if target_type == BindingTargetType.FIELD.value:
            if field_id is None or form_version_id is None:
                raise InvalidEventHandlerState(
                    "field_id and form_version_id are required for field targets"
                )
            if page_version_id:
                raise InvalidEventHandlerState(
                    "field targets must not set page_version_id"
                )
            return {
                "form_version_id": form_version_id,
                "section_id": section_id,
                "field_id": field_id,
                "page_version_id": None,
            }
        if page_version_id is None:
            raise InvalidEventHandlerState(
                "page_version_id is required for page_version targets"
            )
        if form_version_id or section_id or field_id:
            raise InvalidEventHandlerState(
                "page_version targets must not set form/section/field targets"
            )
        return {
            "form_version_id": None,
            "section_id": None,
            "field_id": None,
            "page_version_id": page_version_id,
        }
