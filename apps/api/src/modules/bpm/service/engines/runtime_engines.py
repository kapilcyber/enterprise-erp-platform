"""Runtime engines — instance / task / history / delegation — Phase 4."""

from datetime import datetime, timezone

from modules.bpm.domain.enums import (
    HISTORY_EVENT_TYPE_VALUES,
    TASK_EXECUTION_MODE_VALUES,
    DelegationStatus,
    InstanceStatus,
    TaskStatus,
)
from modules.bpm.domain.exceptions import (
    HistoryAppendOnlyViolation,
    InvalidTaskDelegationState,
    InvalidWorkflowHistoryState,
    InvalidWorkflowInstanceState,
    InvalidWorkflowTaskState,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class WorkflowInstanceEngine:
    def assert_business_ref(self, module_code: str | None, entity_id) -> None:
        if not module_code or not str(module_code).strip():
            raise InvalidWorkflowInstanceState("module_code is required")
        if entity_id is None:
            raise InvalidWorkflowInstanceState("entity_id is required (UUID only)")

    def start(self, row) -> None:
        if row.status != InstanceStatus.PENDING.value:
            raise InvalidWorkflowInstanceState("Only pending instances can be started")
        row.status = InstanceStatus.RUNNING.value
        row.started_at = _utcnow()

    def cancel(self, row, *, reason: str | None = None) -> None:
        if row.status not in {
            InstanceStatus.PENDING.value,
            InstanceStatus.RUNNING.value,
            InstanceStatus.SUSPENDED.value,
        }:
            raise InvalidWorkflowInstanceState(
                "Only pending, running, or suspended instances can be cancelled"
            )
        row.status = InstanceStatus.CANCELLED.value
        row.cancel_reason = reason
        row.completed_at = _utcnow()

    def suspend(self, row) -> None:
        if row.status != InstanceStatus.RUNNING.value:
            raise InvalidWorkflowInstanceState("Only running instances can be suspended")
        row.status = InstanceStatus.SUSPENDED.value
        row.suspended_at = _utcnow()

    def resume(self, row) -> None:
        if row.status != InstanceStatus.SUSPENDED.value:
            raise InvalidWorkflowInstanceState("Only suspended instances can be resumed")
        row.status = InstanceStatus.RUNNING.value
        row.suspended_at = None

    def complete(self, row) -> None:
        if row.status != InstanceStatus.RUNNING.value:
            raise InvalidWorkflowInstanceState("Only running instances can be completed")
        row.status = InstanceStatus.COMPLETED.value
        row.completed_at = _utcnow()

    def fail(self, row, *, reason: str | None = None) -> None:
        if row.status not in {
            InstanceStatus.PENDING.value,
            InstanceStatus.RUNNING.value,
            InstanceStatus.SUSPENDED.value,
        }:
            raise InvalidWorkflowInstanceState("Instance cannot transition to failed")
        row.status = InstanceStatus.FAILED.value
        row.failure_reason = reason
        row.completed_at = _utcnow()


class WorkflowTaskEngine:
    def assert_execution_mode(self, mode: str) -> None:
        if mode not in TASK_EXECUTION_MODE_VALUES:
            raise InvalidWorkflowTaskState(f"Unsupported execution mode: {mode}")

    def assign(self, row, assignee_id) -> None:
        if row.status in {
            TaskStatus.COMPLETED.value,
            TaskStatus.REJECTED.value,
            TaskStatus.CANCELLED.value,
        }:
            raise InvalidWorkflowTaskState("Cannot assign a closed task")
        if assignee_id is None:
            raise InvalidWorkflowTaskState("assignee_id is required")
        row.assignee_id = assignee_id
        row.status = TaskStatus.ASSIGNED.value
        row.claimed_by = None

    def claim(self, row, user_id) -> None:
        if row.status not in {TaskStatus.OPEN.value, TaskStatus.ASSIGNED.value}:
            raise InvalidWorkflowTaskState("Only open or assigned tasks can be claimed")
        row.claimed_by = user_id
        row.assignee_id = user_id
        row.status = TaskStatus.CLAIMED.value

    def release(self, row) -> None:
        if row.status != TaskStatus.CLAIMED.value:
            raise InvalidWorkflowTaskState("Only claimed tasks can be released")
        row.claimed_by = None
        row.status = TaskStatus.ASSIGNED.value if row.assignee_id else TaskStatus.OPEN.value

    def complete(self, row) -> None:
        if row.status not in {TaskStatus.ASSIGNED.value, TaskStatus.CLAIMED.value}:
            raise InvalidWorkflowTaskState("Only assigned or claimed tasks can be completed")
        row.status = TaskStatus.COMPLETED.value
        row.completed_at = _utcnow()

    def reject(self, row, *, reason: str | None = None) -> None:
        if row.status not in {TaskStatus.ASSIGNED.value, TaskStatus.CLAIMED.value}:
            raise InvalidWorkflowTaskState("Only assigned or claimed tasks can be rejected")
        row.status = TaskStatus.REJECTED.value
        row.rejection_reason = reason
        row.completed_at = _utcnow()


class WorkflowHistoryEngine:
    def assert_event_type(self, event_type: str) -> None:
        if event_type not in HISTORY_EVENT_TYPE_VALUES:
            raise InvalidWorkflowHistoryState(f"Unsupported history event type: {event_type}")

    def forbid_mutation(self) -> None:
        raise HistoryAppendOnlyViolation()


class TaskDelegationEngine:
    def assert_period(self, effective_from, effective_to) -> None:
        if effective_from is None:
            raise InvalidTaskDelegationState("effective_from is required")
        if effective_to is not None and effective_to < effective_from:
            raise InvalidTaskDelegationState("effective_to must be >= effective_from")

    def accept(self, row) -> None:
        if row.status != DelegationStatus.PENDING.value:
            raise InvalidTaskDelegationState("Only pending delegations can be accepted")
        row.status = DelegationStatus.ACCEPTED.value
        row.accepted_at = _utcnow()

    def reject(self, row) -> None:
        if row.status != DelegationStatus.PENDING.value:
            raise InvalidTaskDelegationState("Only pending delegations can be rejected")
        row.status = DelegationStatus.REJECTED.value
        row.rejected_at = _utcnow()

    def expire(self, row) -> None:
        if row.status not in {
            DelegationStatus.PENDING.value,
            DelegationStatus.ACCEPTED.value,
        }:
            raise InvalidTaskDelegationState("Delegation cannot be expired from current status")
        row.status = DelegationStatus.EXPIRED.value
        row.expired_at = _utcnow()
