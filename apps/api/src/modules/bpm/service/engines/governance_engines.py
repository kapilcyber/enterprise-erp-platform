"""Assignment / escalation / SLA engines — Phase 3A."""

import json

from modules.bpm.domain.enums import (
    ASSIGNMENT_STRATEGY_VALUES,
    ASSIGNMENT_TYPE_VALUES,
    ESCALATION_TARGET_TYPE_VALUES,
    AssignmentType,
)
from modules.bpm.domain.exceptions import (
    InvalidAssignmentRuleState,
    InvalidEscalationPolicyState,
    InvalidSlaPolicyState,
)


class AssignmentRuleEngine:
    def assert_valid_type(self, assignment_type: str | None) -> None:
        if not assignment_type or assignment_type not in ASSIGNMENT_TYPE_VALUES:
            raise InvalidAssignmentRuleState(f"Unsupported assignment type: {assignment_type}")

    def assert_valid_strategy(self, strategy: str) -> None:
        if strategy not in ASSIGNMENT_STRATEGY_VALUES:
            raise InvalidAssignmentRuleState(f"Unsupported assignment strategy: {strategy}")

    def assert_type_targets(
        self,
        assignment_type: str | None,
        *,
        role_id=None,
        user_id=None,
        department_id=None,
        expression: str | None = None,
    ) -> None:
        if not assignment_type:
            raise InvalidAssignmentRuleState("assignment_type is required")
        if assignment_type == AssignmentType.ROLE.value and role_id is None:
            raise InvalidAssignmentRuleState("role_id is required for role assignment")
        if assignment_type == AssignmentType.USER.value and user_id is None:
            raise InvalidAssignmentRuleState("user_id is required for user assignment")
        if assignment_type == AssignmentType.DEPARTMENT.value and department_id is None:
            raise InvalidAssignmentRuleState(
                "department_id is required for department assignment"
            )
        if assignment_type == AssignmentType.DYNAMIC.value and (
            not expression or not str(expression).strip()
        ):
            raise InvalidAssignmentRuleState("expression is required for dynamic assignment")

    def assert_strategy_metadata(self, strategy: str, metadata_json: str | None) -> None:
        if strategy == "static":
            return
        if not metadata_json:
            raise InvalidAssignmentRuleState(
                f"strategy_metadata_json is required for strategy '{strategy}'"
            )
        try:
            data = json.loads(metadata_json)
        except json.JSONDecodeError as exc:
            raise InvalidAssignmentRuleState(f"Invalid strategy_metadata_json: {exc}") from exc
        if not isinstance(data, dict):
            raise InvalidAssignmentRuleState("strategy_metadata_json must be a JSON object")


class EscalationPolicyEngine:
    def assert_valid_target_type(self, target_type: str | None) -> None:
        if not target_type or target_type not in ESCALATION_TARGET_TYPE_VALUES:
            raise InvalidEscalationPolicyState(
                f"Unsupported escalation target type: {target_type}"
            )

    def assert_level(self, level: int | None) -> None:
        if level is None or int(level) < 1:
            raise InvalidEscalationPolicyState("escalation_level must be >= 1")

    def assert_delay(self, delay_minutes: int | None) -> None:
        if delay_minutes is None or int(delay_minutes) < 0:
            raise InvalidEscalationPolicyState("escalation_delay_minutes must be >= 0")

    def assert_retry(self, retry_count: int | None) -> None:
        if retry_count is None or int(retry_count) < 0:
            raise InvalidEscalationPolicyState("retry_count must be >= 0")

    def assert_levels_json(self, levels_json: str | None) -> None:
        if levels_json is None:
            return
        try:
            data = json.loads(levels_json)
        except json.JSONDecodeError as exc:
            raise InvalidEscalationPolicyState(f"Invalid levels_json: {exc}") from exc
        if not isinstance(data, list):
            raise InvalidEscalationPolicyState("levels_json must be a JSON array")


class SlaPolicyEngine:
    def assert_timezone(self, timezone: str | None) -> None:
        if not timezone or not str(timezone).strip():
            raise InvalidSlaPolicyState("timezone is required")

    def assert_thresholds(
        self, warning_threshold_minutes: int | None, breach_threshold_minutes: int | None
    ) -> None:
        if warning_threshold_minutes is None or int(warning_threshold_minutes) < 0:
            raise InvalidSlaPolicyState("warning_threshold_minutes must be >= 0")
        if breach_threshold_minutes is None or int(breach_threshold_minutes) < 0:
            raise InvalidSlaPolicyState("breach_threshold_minutes must be >= 0")
        if int(breach_threshold_minutes) < int(warning_threshold_minutes):
            raise InvalidSlaPolicyState(
                "breach_threshold_minutes must be >= warning_threshold_minutes"
            )

    def assert_json_object_or_array(self, field: str, value: str | None) -> None:
        if value is None:
            return
        try:
            data = json.loads(value)
        except json.JSONDecodeError as exc:
            raise InvalidSlaPolicyState(f"Invalid {field}: {exc}") from exc
        if not isinstance(data, (dict, list)):
            raise InvalidSlaPolicyState(f"{field} must be a JSON object or array")
