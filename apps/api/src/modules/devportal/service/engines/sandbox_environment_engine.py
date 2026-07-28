"""Sandbox environment lifecycle — metadata only; no runtime provisioning."""

from modules.devportal.domain.enums import SandboxEnvironmentStatus
from modules.devportal.domain.exceptions import InvalidSandboxEnvironmentState


class SandboxEnvironmentEngine:
    def activate(self, row) -> None:
        if row.status not in {
            SandboxEnvironmentStatus.DRAFT.value,
            SandboxEnvironmentStatus.RETIRED.value,
        }:
            raise InvalidSandboxEnvironmentState(
                "Sandbox cannot be activated from current status"
            )
        row.status = SandboxEnvironmentStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status == SandboxEnvironmentStatus.RETIRED.value:
            raise InvalidSandboxEnvironmentState("Sandbox already retired")
        row.status = SandboxEnvironmentStatus.RETIRED.value
