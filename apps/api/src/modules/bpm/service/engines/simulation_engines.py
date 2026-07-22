"""Simulation engines — Phase 5 (no business mutation / no runtime instances)."""

from datetime import datetime, timezone

from modules.bpm.domain.enums import SIMULATION_STATUS_VALUES, SimulationStatus, VersionStatus
from modules.bpm.domain.exceptions import InvalidSimulationRunState, SimulationNotAllowed


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SimulationRunEngine:
    def assert_status(self, status: str) -> None:
        if status not in SIMULATION_STATUS_VALUES:
            raise InvalidSimulationRunState(f"Unsupported simulation status: {status}")

    def assert_simulatable(self, version) -> None:
        if version.status not in {
            VersionStatus.DRAFT.value,
            VersionStatus.PUBLISHED.value,
        }:
            raise SimulationNotAllowed(
                f"Simulation allowed only on Draft or Published versions; got '{version.status}'"
            )

    def begin(self, row) -> None:
        if row.status not in {
            SimulationStatus.PENDING.value,
            SimulationStatus.FAILED.value,
            SimulationStatus.COMPLETED.value,
        }:
            raise InvalidSimulationRunState(
                "Only pending, completed, or failed simulations can be (re)run"
            )
        row.status = SimulationStatus.RUNNING.value
        row.started_at = _utcnow()
        row.completed_at = None
        row.duration_ms = 0
        row.warnings_json = None
        row.errors_json = None
        row.execution_trace_json = None
        row.result_summary_json = None

    def complete(self, row, *, duration_ms: int) -> None:
        if row.status != SimulationStatus.RUNNING.value:
            raise InvalidSimulationRunState("Only running simulations can complete")
        row.status = SimulationStatus.COMPLETED.value
        row.duration_ms = max(0, int(duration_ms))
        row.completed_at = _utcnow()

    def fail(self, row, *, duration_ms: int) -> None:
        if row.status != SimulationStatus.RUNNING.value:
            raise InvalidSimulationRunState("Only running simulations can fail")
        row.status = SimulationStatus.FAILED.value
        row.duration_ms = max(0, int(duration_ms))
        row.completed_at = _utcnow()

    def cancel(self, row) -> None:
        if row.status in {
            SimulationStatus.COMPLETED.value,
            SimulationStatus.CANCELLED.value,
        }:
            raise InvalidSimulationRunState("Terminal simulation cannot be cancelled")
        row.status = SimulationStatus.CANCELLED.value
        row.completed_at = _utcnow()
