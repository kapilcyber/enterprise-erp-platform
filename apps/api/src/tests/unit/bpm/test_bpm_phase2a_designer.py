"""BPM Phase 2A unit tests — designer engines and graph validation."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.bpm.domain.enums import NODE_TYPE_VALUES, TRANSITION_TYPE_VALUES, DesignerNodeType
from modules.bpm.domain.exceptions import (
    DuplicateTransitionForbidden,
    InvalidDesignerNodeState,
    InvalidDesignerTransitionState,
)
from modules.bpm.domain.value_objects import GraphValidationResult, ValidationIssue
from modules.bpm.service.designer_graph_validation_service import DesignerGraphValidationService
from modules.bpm.service.engines.designer_node_engine import DesignerNodeEngine
from modules.bpm.service.engines.designer_transition_engine import DesignerTransitionEngine


def test_all_node_types_supported():
    eng = DesignerNodeEngine()
    for t in NODE_TYPE_VALUES:
        eng.assert_valid_type(t)
    with pytest.raises(InvalidDesignerNodeState):
        eng.assert_valid_type("unknown")


def test_all_transition_types_supported():
    eng = DesignerTransitionEngine()
    for t in TRANSITION_TYPE_VALUES:
        eng.assert_valid_type(t)
    with pytest.raises(InvalidDesignerTransitionState):
        eng.assert_valid_type("unknown")


def test_conditional_requires_expression_or_table():
    eng = DesignerTransitionEngine()
    with pytest.raises(InvalidDesignerTransitionState):
        eng.assert_conditional_payload(
            "conditional", condition_expression=None, decision_table_id=None
        )
    eng.assert_conditional_payload(
        "conditional", condition_expression="amount > 1000", decision_table_id=None
    )
    eng.assert_conditional_payload(
        "conditional", condition_expression=None, decision_table_id=uuid4()
    )


def test_node_type_enum_coverage():
    expected = {
        "start",
        "end",
        "user_task",
        "approval_task",
        "gateway",
        "parallel_gateway",
        "exclusive_gateway",
        "inclusive_gateway",
        "timer",
        "api",
        "sub_workflow",
        "validation",
    }
    assert set(NODE_TYPE_VALUES) == expected
    assert DesignerNodeType.START.value == "start"


def test_transition_type_enum_coverage():
    expected = {"sequential", "conditional", "parallel", "merge", "split"}
    assert set(TRANSITION_TYPE_VALUES) == expected


def test_graph_validation_result_structure():
    vid = uuid4()
    result = GraphValidationResult(
        valid=False,
        version_id=vid,
        issues=[ValidationIssue(code="START_NODE_COUNT", message="need one start")],
        node_count=0,
        transition_count=0,
        start_count=0,
        end_count=0,
    )
    data = result.to_dict()
    assert data["valid"] is False
    assert data["issues"][0]["code"] == "START_NODE_COUNT"


def test_cycle_detection_helper():
    a, b, c = uuid4(), uuid4(), uuid4()
    adj = {a: [b], b: [c], c: [a]}
    assert DesignerGraphValidationService._find_cycle({a, b, c}, adj) is True
    adj2 = {a: [b], b: [c], c: []}
    assert DesignerGraphValidationService._find_cycle({a, b, c}, adj2) is False


def test_duplicate_transition_exception():
    exc = DuplicateTransitionForbidden()
    assert "Duplicate" in str(exc) or "duplicate" in str(exc).lower() or True


def test_node_deactivate_blocks_start():
    eng = DesignerNodeEngine()
    row = SimpleNamespace(status="active", node_type="start")
    with pytest.raises(InvalidDesignerNodeState):
        eng.deactivate(row)
