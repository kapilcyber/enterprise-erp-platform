"""Designer transition lifecycle engine — Phase 2A."""

from modules.bpm.domain.enums import TRANSITION_TYPE_VALUES, TransitionStatus, TransitionType
from modules.bpm.domain.exceptions import InvalidDesignerTransitionState


class DesignerTransitionEngine:
    def assert_valid_type(self, transition_type: str) -> None:
        if transition_type not in TRANSITION_TYPE_VALUES:
            raise InvalidDesignerTransitionState(
                f"Unsupported transition type: {transition_type}"
            )

    def assert_conditional_payload(
        self, transition_type: str, *, condition_expression: str | None, decision_table_id
    ) -> None:
        if (
            transition_type == TransitionType.CONDITIONAL.value
            and not condition_expression
            and decision_table_id is None
        ):
            raise InvalidDesignerTransitionState(
                "Conditional transitions require condition_expression or decision_table_id"
            )

    def activate(self, row) -> None:
        if row.status == TransitionStatus.ACTIVE.value:
            raise InvalidDesignerTransitionState("Transition already active")
        row.status = TransitionStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status != TransitionStatus.ACTIVE.value:
            raise InvalidDesignerTransitionState("Only active transitions can be deactivated")
        row.status = TransitionStatus.INACTIVE.value
