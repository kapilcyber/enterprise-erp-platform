"""Evaluation lifecycle engine — metadata transitions only (no runtime execution)."""

from datetime import datetime, timezone

from modules.ai.domain.enums import EvaluationStatus
from modules.ai.domain.exceptions import CompletedEvaluationImmutable, InvalidEvaluationState


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class EvaluationEngine:
    def assert_editable(self, row) -> None:
        if row.status in {
            EvaluationStatus.COMPLETED.value,
            EvaluationStatus.FAILED.value,
        }:
            raise CompletedEvaluationImmutable()
        if row.status == EvaluationStatus.RUNNING.value:
            raise InvalidEvaluationState("Running evaluations are read-only except complete/fail")

    def queue(self, row) -> None:
        if row.status != EvaluationStatus.QUEUED.value:
            raise InvalidEvaluationState("Only queued evaluations can be re-queued")
        row.queued_at = _utcnow()

    def start(self, row) -> None:
        if row.status != EvaluationStatus.QUEUED.value:
            raise InvalidEvaluationState("Only queued evaluations can be started")
        row.status = EvaluationStatus.RUNNING.value
        row.started_at = _utcnow()

    def complete(self, row, *, result_summary_json: str | None = None, metrics_json: str | None = None) -> None:
        if row.status != EvaluationStatus.RUNNING.value:
            raise InvalidEvaluationState("Only running evaluations can be completed")
        row.status = EvaluationStatus.COMPLETED.value
        row.completed_at = _utcnow()
        if result_summary_json is not None:
            row.result_summary_json = result_summary_json
        if metrics_json is not None:
            row.metrics_json = metrics_json

    def fail(self, row, *, failure_reason: str | None = None) -> None:
        if row.status not in {
            EvaluationStatus.QUEUED.value,
            EvaluationStatus.RUNNING.value,
        }:
            raise InvalidEvaluationState("Only queued or running evaluations can fail")
        row.status = EvaluationStatus.FAILED.value
        row.failed_at = _utcnow()
        if failure_reason is not None:
            row.failure_reason = failure_reason
