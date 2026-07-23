"""Form field lifecycle engine — Phase 2A."""

import re

from modules.lowcode.domain.enums import FIELD_TYPE_VALUES, FieldStatus
from modules.lowcode.domain.exceptions import InvalidFieldState

_FIELD_KEY_RE = re.compile(r"^[a-z][a-z0-9_]{0,99}$")


class FormFieldEngine:
    def assert_valid_type(self, field_type: str | None) -> None:
        if not field_type or field_type not in FIELD_TYPE_VALUES:
            raise InvalidFieldState(f"Unsupported field type: {field_type}")

    def assert_field_key(self, field_key: str | None) -> None:
        if not field_key or not _FIELD_KEY_RE.match(field_key):
            raise InvalidFieldState(
                "field_key must be lowercase snake_case starting with a letter "
                "(max 100 chars)"
            )

    def assert_display_order(self, display_order: int | None) -> None:
        if display_order is not None and display_order < 0:
            raise InvalidFieldState("display_order must be >= 0")

    def activate(self, row) -> None:
        if row.status == FieldStatus.ACTIVE.value:
            raise InvalidFieldState("Field already active")
        row.status = FieldStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status != FieldStatus.ACTIVE.value:
            raise InvalidFieldState("Only active fields can be deactivated")
        row.status = FieldStatus.INACTIVE.value
