"""Decision table / business rule / variable / form engines — Phase 2B."""

from modules.bpm.domain.enums import (
    BUSINESS_RULE_TYPE_VALUES,
    FORM_MODE_VALUES,
    VARIABLE_TYPE_VALUES,
    DecisionTableStatus,
)
from modules.bpm.domain.exceptions import (
    InvalidBusinessRuleState,
    InvalidDecisionTableState,
    InvalidFormReferenceState,
    InvalidWorkflowVariableState,
)


class DecisionTableEngine:
    def enable(self, row) -> None:
        if row.status == DecisionTableStatus.ENABLED.value:
            raise InvalidDecisionTableState("Decision table already enabled")
        row.status = DecisionTableStatus.ENABLED.value

    def disable(self, row) -> None:
        if row.status != DecisionTableStatus.ENABLED.value:
            raise InvalidDecisionTableState("Only enabled tables can be disabled")
        row.status = DecisionTableStatus.DISABLED.value

    def assert_rows_json(self, rows_json: str | None) -> None:
        if rows_json is None:
            return
        import json

        try:
            data = json.loads(rows_json)
        except json.JSONDecodeError as exc:
            raise InvalidDecisionTableState(f"Invalid rows_json: {exc}") from exc
        if not isinstance(data, list):
            raise InvalidDecisionTableState("rows_json must be a JSON array")


class BusinessRuleEngine:
    def assert_valid_type(self, rule_type: str | None) -> None:
        if not rule_type or rule_type not in BUSINESS_RULE_TYPE_VALUES:
            raise InvalidBusinessRuleState(f"Unsupported rule type: {rule_type}")

    def assert_expression(self, expression: str | None) -> None:
        if not expression or not str(expression).strip():
            raise InvalidBusinessRuleState("Expression is required")


class WorkflowVariableEngine:
    def assert_valid_type(self, variable_type: str | None) -> None:
        if not variable_type or variable_type not in VARIABLE_TYPE_VALUES:
            raise InvalidWorkflowVariableState(f"Unsupported variable type: {variable_type}")

    def assert_key(self, variable_key: str | None) -> None:
        if not variable_key or not str(variable_key).strip():
            raise InvalidWorkflowVariableState("variable_key is required")


class FormReferenceEngine:
    def assert_valid_mode(self, access_mode: str) -> None:
        if access_mode not in FORM_MODE_VALUES:
            raise InvalidFormReferenceState(f"Unsupported access mode: {access_mode}")

    def assert_form_uuid(self, low_code_form_id) -> None:
        if low_code_form_id is None:
            raise InvalidFormReferenceState("low_code_form_id is required (Low-Code UUID only)")
