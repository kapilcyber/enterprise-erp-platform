"""BPM Phase 2B unit tests — intelligence engines."""

from types import SimpleNamespace

import pytest

from modules.bpm.domain.enums import (
    BUSINESS_RULE_TYPE_VALUES,
    FORM_MODE_VALUES,
    VARIABLE_TYPE_VALUES,
)
from modules.bpm.domain.exceptions import (
    InvalidBusinessRuleState,
    InvalidDecisionTableState,
    InvalidFormReferenceState,
    InvalidWorkflowVariableState,
)
from modules.bpm.service.engines import (
    BusinessRuleEngine,
    DecisionTableEngine,
    FormReferenceEngine,
    WorkflowVariableEngine,
)


def test_decision_table_enable_disable():
    eng = DecisionTableEngine()
    row = SimpleNamespace(status="disabled")
    eng.enable(row)
    assert row.status == "enabled"
    eng.disable(row)
    assert row.status == "disabled"
    with pytest.raises(InvalidDecisionTableState):
        eng.disable(row)


def test_decision_table_rows_json_must_be_array():
    eng = DecisionTableEngine()
    eng.assert_rows_json('[{"row_id":"1"}]')
    with pytest.raises(InvalidDecisionTableState):
        eng.assert_rows_json('{"not":"array"}')
    with pytest.raises(InvalidDecisionTableState):
        eng.assert_rows_json("not-json")


def test_business_rule_types_and_expression():
    eng = BusinessRuleEngine()
    for t in BUSINESS_RULE_TYPE_VALUES:
        eng.assert_valid_type(t)
    with pytest.raises(InvalidBusinessRuleState):
        eng.assert_valid_type("unknown")
    eng.assert_expression("amount > 100")
    with pytest.raises(InvalidBusinessRuleState):
        eng.assert_expression("  ")


def test_variable_types_and_key():
    eng = WorkflowVariableEngine()
    expected = {"string", "number", "boolean", "date", "json"}
    assert set(VARIABLE_TYPE_VALUES) == expected
    for t in VARIABLE_TYPE_VALUES:
        eng.assert_valid_type(t)
    with pytest.raises(InvalidWorkflowVariableState):
        eng.assert_valid_type("blob")
    eng.assert_key("invoice_total")
    with pytest.raises(InvalidWorkflowVariableState):
        eng.assert_key("")


def test_form_reference_mode_and_uuid():
    eng = FormReferenceEngine()
    assert set(FORM_MODE_VALUES) == {"read_only", "editable"}
    for m in FORM_MODE_VALUES:
        eng.assert_valid_mode(m)
    with pytest.raises(InvalidFormReferenceState):
        eng.assert_valid_mode("write_once")
    from uuid import uuid4

    eng.assert_form_uuid(uuid4())
    with pytest.raises(InvalidFormReferenceState):
        eng.assert_form_uuid(None)


def test_business_rule_type_enum_coverage():
    expected = {"expression", "decision", "validation", "routing"}
    assert set(BUSINESS_RULE_TYPE_VALUES) == expected
