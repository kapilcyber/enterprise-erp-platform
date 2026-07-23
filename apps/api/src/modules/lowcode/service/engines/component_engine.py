"""Component lifecycle engine — Phase 2B."""

from modules.lowcode.domain.enums import COMPONENT_KIND_VALUES, ComponentStatus
from modules.lowcode.domain.exceptions import InvalidComponentState


class ComponentEngine:
    def assert_valid_kind(self, component_kind: str | None) -> None:
        if not component_kind or component_kind not in COMPONENT_KIND_VALUES:
            raise InvalidComponentState(f"Unsupported component kind: {component_kind}")

    def activate(self, row) -> None:
        if row.status == ComponentStatus.ACTIVE.value:
            raise InvalidComponentState("Component already active")
        if row.status == ComponentStatus.RETIRED.value:
            raise InvalidComponentState("Retired components cannot be activated")
        row.status = ComponentStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status == ComponentStatus.RETIRED.value:
            raise InvalidComponentState("Component already retired")
        row.status = ComponentStatus.RETIRED.value
