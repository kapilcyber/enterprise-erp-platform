"""ExpressionBinding validation engine — Phase 2C design-time metadata only."""

from uuid import UUID

from modules.lowcode.domain.enums import BINDING_TARGET_TYPE_VALUES, BindingTargetType
from modules.lowcode.domain.exceptions import InvalidExpressionBindingState


class ExpressionBindingEngine:
    def assert_valid_target_type(self, target_type: str | None) -> None:
        if not target_type or target_type not in BINDING_TARGET_TYPE_VALUES:
            raise InvalidExpressionBindingState(f"Unsupported binding target_type: {target_type}")

    def assert_sort_order(self, sort_order: int | None) -> None:
        if sort_order is not None and sort_order < 0:
            raise InvalidExpressionBindingState("sort_order must be >= 0")

    def normalize_targets(
        self,
        *,
        target_type: str,
        form_version_id: UUID | None,
        section_id: UUID | None,
        field_id: UUID | None,
        page_version_id: UUID | None,
    ) -> dict:
        """Ensure exactly the columns matching target_type are set."""
        self.assert_valid_target_type(target_type)
        if target_type == BindingTargetType.FORM_VERSION.value:
            if form_version_id is None:
                raise InvalidExpressionBindingState(
                    "form_version_id is required for form_version bindings"
                )
            if section_id or field_id or page_version_id:
                raise InvalidExpressionBindingState(
                    "form_version bindings must not set section/field/page_version"
                )
            return {
                "form_version_id": form_version_id,
                "section_id": None,
                "field_id": None,
                "page_version_id": None,
            }
        if target_type == BindingTargetType.SECTION.value:
            if section_id is None or form_version_id is None:
                raise InvalidExpressionBindingState(
                    "section_id and form_version_id are required for section bindings"
                )
            if field_id or page_version_id:
                raise InvalidExpressionBindingState(
                    "section bindings must not set field_id or page_version_id"
                )
            return {
                "form_version_id": form_version_id,
                "section_id": section_id,
                "field_id": None,
                "page_version_id": None,
            }
        if target_type == BindingTargetType.FIELD.value:
            if field_id is None or form_version_id is None:
                raise InvalidExpressionBindingState(
                    "field_id and form_version_id are required for field bindings"
                )
            if page_version_id:
                raise InvalidExpressionBindingState(
                    "field bindings must not set page_version_id"
                )
            return {
                "form_version_id": form_version_id,
                "section_id": section_id,
                "field_id": field_id,
                "page_version_id": None,
            }
        # page_version — future pages; UUID metadata only (no FK / no execution)
        if page_version_id is None:
            raise InvalidExpressionBindingState(
                "page_version_id is required for page_version bindings"
            )
        if form_version_id or section_id or field_id:
            raise InvalidExpressionBindingState(
                "page_version bindings must not set form/section/field targets"
            )
        return {
            "form_version_id": None,
            "section_id": None,
            "field_id": None,
            "page_version_id": page_version_id,
        }
