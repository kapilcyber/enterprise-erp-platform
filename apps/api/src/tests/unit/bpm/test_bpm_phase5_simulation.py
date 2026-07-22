"""BPM Phase 5 unit tests — simulation engine + graph task generation polish."""

from types import SimpleNamespace

import pytest

from modules.bpm.domain.enums import SIMULATION_STATUS_VALUES
from modules.bpm.domain.exceptions import InvalidSimulationRunState, SimulationNotAllowed
from modules.bpm.domain.value_objects import SimulationResultSummary
from modules.bpm.service.engines import SimulationRunEngine
from modules.bpm.service.graph_driven_task_generation_service import (
    _PASS_THROUGH,
    _TASK_NODE_TYPES,
)


def test_simulation_status_values():
    assert "pending" in SIMULATION_STATUS_VALUES
    assert "running" in SIMULATION_STATUS_VALUES
    assert "completed" in SIMULATION_STATUS_VALUES
    assert "failed" in SIMULATION_STATUS_VALUES


def test_simulation_allowed_draft_or_published_only():
    eng = SimulationRunEngine()
    eng.assert_simulatable(SimpleNamespace(status="draft"))
    eng.assert_simulatable(SimpleNamespace(status="published"))
    with pytest.raises(SimulationNotAllowed):
        eng.assert_simulatable(SimpleNamespace(status="retired"))


def test_simulation_lifecycle_complete():
    eng = SimulationRunEngine()
    row = SimpleNamespace(
        status="pending",
        started_at=None,
        completed_at=None,
        duration_ms=0,
        warnings_json=None,
        errors_json=None,
        execution_trace_json=None,
        result_summary_json=None,
    )
    eng.begin(row)
    assert row.status == "running"
    eng.complete(row, duration_ms=42)
    assert row.status == "completed"
    assert row.duration_ms == 42
    assert row.completed_at is not None


def test_simulation_lifecycle_fail_and_cancel():
    eng = SimulationRunEngine()
    row = SimpleNamespace(
        status="pending",
        started_at=None,
        completed_at=None,
        duration_ms=0,
        warnings_json=None,
        errors_json=None,
        execution_trace_json=None,
        result_summary_json=None,
    )
    eng.begin(row)
    eng.fail(row, duration_ms=10)
    assert row.status == "failed"
    row2 = SimpleNamespace(status="pending", completed_at=None)
    eng.cancel(row2)
    assert row2.status == "cancelled"
    with pytest.raises(InvalidSimulationRunState):
        eng.cancel(row2)


def test_simulation_result_summary():
    summary = SimulationResultSummary(
        valid=True,
        nodes_visited=3,
        transitions_evaluated=2,
        decision_tables_evaluated=1,
        business_rules_evaluated=1,
        variables_resolved=2,
        warning_count=0,
        error_count=0,
        duration_ms=5,
    )
    d = summary.to_dict()
    assert d["valid"] is True
    assert d["nodes_visited"] == 3


def test_graph_task_node_type_sets():
    assert "user_task" in _TASK_NODE_TYPES
    assert "approval_task" in _TASK_NODE_TYPES
    assert "start" in _PASS_THROUGH
    assert "end" not in _PASS_THROUGH


def test_transition_condition_simulation_helper():
    from modules.bpm.service.simulation_run_service import SimulationRunService

    svc = SimulationRunService.__new__(SimulationRunService)
    t = SimpleNamespace(
        transition_type="conditional",
        condition_expression="amount==100",
        condition_json=None,
    )
    ok, detail = svc._evaluate_transition(t, {"amount": "100"})
    assert ok is True
    assert "condition" in detail
    ok2, _ = svc._evaluate_transition(t, {"amount": "50"})
    assert ok2 is False


def test_code_prefix_simulation():
    from modules.bpm.domain.enums import CODE_PREFIXES, BpmEntityType

    prefix, width, _ = CODE_PREFIXES[BpmEntityType.SIMULATION_RUN]
    assert prefix == "SIM-"
    assert width == 6
