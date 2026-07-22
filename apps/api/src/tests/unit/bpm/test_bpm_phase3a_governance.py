"""BPM Phase 3A unit tests — governance engines."""

from uuid import uuid4

import pytest

from modules.bpm.domain.enums import (
    ASSIGNMENT_STRATEGY_VALUES,
    ASSIGNMENT_TYPE_VALUES,
    ESCALATION_TARGET_TYPE_VALUES,
)
from modules.bpm.domain.exceptions import (
    InvalidAssignmentRuleState,
    InvalidEscalationPolicyState,
    InvalidSlaPolicyState,
)
from modules.bpm.domain.value_objects import (
    AssignmentTargetRef,
    EscalationLevelSpec,
    SlaThresholdSpec,
)
from modules.bpm.service.engines import (
    AssignmentRuleEngine,
    EscalationPolicyEngine,
    SlaPolicyEngine,
)


def test_assignment_types_and_strategies():
    eng = AssignmentRuleEngine()
    assert set(ASSIGNMENT_TYPE_VALUES) == {"role", "user", "department", "dynamic"}
    assert set(ASSIGNMENT_STRATEGY_VALUES) == {"static", "round_robin", "load_balance"}
    for t in ASSIGNMENT_TYPE_VALUES:
        eng.assert_valid_type(t)
    for s in ASSIGNMENT_STRATEGY_VALUES:
        eng.assert_valid_strategy(s)
    with pytest.raises(InvalidAssignmentRuleState):
        eng.assert_valid_type("unknown")


def test_assignment_type_targets():
    eng = AssignmentRuleEngine()
    eng.assert_type_targets("role", role_id=uuid4())
    eng.assert_type_targets("user", user_id=uuid4())
    eng.assert_type_targets("department", department_id=uuid4())
    eng.assert_type_targets("dynamic", expression="manager_of(requester)")
    with pytest.raises(InvalidAssignmentRuleState):
        eng.assert_type_targets("role", role_id=None)
    with pytest.raises(InvalidAssignmentRuleState):
        eng.assert_type_targets("dynamic", expression="")


def test_assignment_strategy_metadata():
    eng = AssignmentRuleEngine()
    eng.assert_strategy_metadata("static", None)
    eng.assert_strategy_metadata("round_robin", '{"pool":["a","b"]}')
    with pytest.raises(InvalidAssignmentRuleState):
        eng.assert_strategy_metadata("load_balance", None)
    with pytest.raises(InvalidAssignmentRuleState):
        eng.assert_strategy_metadata("round_robin", "[]")


def test_escalation_policy_rules():
    eng = EscalationPolicyEngine()
    assert set(ESCALATION_TARGET_TYPE_VALUES) == {"role", "user", "department"}
    eng.assert_valid_target_type("role")
    eng.assert_level(1)
    eng.assert_delay(30)
    eng.assert_retry(2)
    eng.assert_levels_json('[{"level":1,"delay_minutes":15}]')
    with pytest.raises(InvalidEscalationPolicyState):
        eng.assert_level(0)
    with pytest.raises(InvalidEscalationPolicyState):
        eng.assert_levels_json("{}")


def test_sla_policy_thresholds_and_timezone():
    eng = SlaPolicyEngine()
    eng.assert_timezone("Asia/Kolkata")
    eng.assert_thresholds(60, 120)
    eng.assert_json_object_or_array("business_hours_json", '{"mon":["09:00","17:00"]}')
    eng.assert_json_object_or_array("reminder_intervals_json", "[30,60]")
    with pytest.raises(InvalidSlaPolicyState):
        eng.assert_timezone("")
    with pytest.raises(InvalidSlaPolicyState):
        eng.assert_thresholds(120, 60)


def test_governance_value_objects():
    ref = AssignmentTargetRef(target_type="role", target_id=uuid4())
    assert ref.target_type == "role"
    level = EscalationLevelSpec(level=2, delay_minutes=45, target_type="user", target_id=uuid4())
    assert level.retry_count == 0
    sla = SlaThresholdSpec(
        warning_threshold_minutes=30,
        breach_threshold_minutes=90,
        timezone="UTC",
    )
    assert sla.holiday_calendar_id is None
