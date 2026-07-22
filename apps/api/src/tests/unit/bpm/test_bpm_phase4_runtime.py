"""BPM Phase 4 unit tests — runtime engines."""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.bpm.domain.enums import (
    DELEGATION_STATUS_VALUES,
    HISTORY_EVENT_TYPE_VALUES,
    INSTANCE_STATUS_VALUES,
    TASK_STATUS_VALUES,
)
from modules.bpm.domain.exceptions import (
    DraftVersionNotExecutable,
    HistoryAppendOnlyViolation,
    InvalidTaskDelegationState,
    InvalidWorkflowInstanceState,
    InvalidWorkflowTaskState,
)
from modules.bpm.domain.value_objects import BusinessEntityRef, HistoryEventSpec
from modules.bpm.service.engines import (
    TaskDelegationEngine,
    WorkflowHistoryEngine,
    WorkflowInstanceEngine,
    WorkflowTaskEngine,
    WorkflowVersionEngine,
)


def test_instance_lifecycle():
    eng = WorkflowInstanceEngine()
    row = SimpleNamespace(
        status="pending",
        started_at=None,
        completed_at=None,
        suspended_at=None,
        cancel_reason=None,
        failure_reason=None,
    )
    eng.start(row)
    assert row.status == "running"
    eng.suspend(row)
    assert row.status == "suspended"
    eng.resume(row)
    assert row.status == "running"
    eng.complete(row)
    assert row.status == "completed"
    with pytest.raises(InvalidWorkflowInstanceState):
        eng.start(row)


def test_instance_cancel_and_fail():
    eng = WorkflowInstanceEngine()
    row = SimpleNamespace(
        status="running",
        cancel_reason=None,
        failure_reason=None,
        completed_at=None,
        suspended_at=None,
        started_at=None,
    )
    eng.cancel(row, reason="user abort")
    assert row.status == "cancelled"
    row2 = SimpleNamespace(
        status="running",
        cancel_reason=None,
        failure_reason=None,
        completed_at=None,
        suspended_at=None,
        started_at=None,
    )
    eng.fail(row2, reason="error")
    assert row2.status == "failed"


def test_published_only_executable():
    eng = WorkflowVersionEngine()
    with pytest.raises(DraftVersionNotExecutable):
        eng.assert_executable(SimpleNamespace(status="draft"))
    eng.assert_executable(SimpleNamespace(status="published"))


def test_task_assign_claim_complete():
    eng = WorkflowTaskEngine()
    uid = uuid4()
    row = SimpleNamespace(
        status="open",
        assignee_id=None,
        claimed_by=None,
        completed_at=None,
        rejection_reason=None,
    )
    eng.assign(row, uid)
    assert row.status == "assigned"
    eng.claim(row, uid)
    assert row.status == "claimed"
    eng.complete(row)
    assert row.status == "completed"


def test_task_reject_and_release():
    eng = WorkflowTaskEngine()
    uid = uuid4()
    row = SimpleNamespace(
        status="assigned",
        assignee_id=uid,
        claimed_by=None,
        completed_at=None,
        rejection_reason=None,
    )
    eng.claim(row, uid)
    eng.release(row)
    assert row.status == "assigned"
    eng.reject(row, reason="no")
    assert row.status == "rejected"
    with pytest.raises(InvalidWorkflowTaskState):
        eng.complete(row)


def test_history_append_only():
    eng = WorkflowHistoryEngine()
    for t in HISTORY_EVENT_TYPE_VALUES:
        eng.assert_event_type(t)
    with pytest.raises(HistoryAppendOnlyViolation):
        eng.forbid_mutation()


def test_delegation_accept_reject_expire():
    eng = TaskDelegationEngine()
    now = datetime.now(timezone.utc)
    eng.assert_period(now, now + timedelta(days=1))
    with pytest.raises(InvalidTaskDelegationState):
        eng.assert_period(now, now - timedelta(days=1))
    row = SimpleNamespace(
        status="pending", accepted_at=None, rejected_at=None, expired_at=None
    )
    eng.accept(row)
    assert row.status == "accepted"
    row2 = SimpleNamespace(
        status="pending", accepted_at=None, rejected_at=None, expired_at=None
    )
    eng.reject(row2)
    assert row2.status == "rejected"
    row3 = SimpleNamespace(
        status="accepted", accepted_at=None, rejected_at=None, expired_at=None
    )
    eng.expire(row3)
    assert row3.status == "expired"


def test_runtime_enum_coverage():
    assert "running" in INSTANCE_STATUS_VALUES
    assert "claimed" in TASK_STATUS_VALUES
    assert "delegation" in HISTORY_EVENT_TYPE_VALUES
    assert "pending" in DELEGATION_STATUS_VALUES
    ref = BusinessEntityRef(module_code="finance", entity_id=uuid4())
    assert ref.module_code == "finance"
    ev = HistoryEventSpec(event_type="approval", to_status="completed")
    assert ev.event_type == "approval"
