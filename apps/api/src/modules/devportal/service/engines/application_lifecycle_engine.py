"""Application registration lifecycle — Draft → Submit → Approve → Active / Suspend → Retire."""

from modules.devportal.domain.enums import ApplicationStatus
from modules.devportal.domain.exceptions import InvalidApplicationState


class ApplicationLifecycleEngine:
    def submit(self, row) -> None:
        if row.status != ApplicationStatus.DRAFT.value:
            raise InvalidApplicationState("Only draft applications can be submitted")
        row.status = ApplicationStatus.SUBMITTED.value
        row.workflow_status = "pending"

    def approve(self, row) -> None:
        if row.status != ApplicationStatus.SUBMITTED.value:
            raise InvalidApplicationState("Only submitted applications can be approved")
        row.status = ApplicationStatus.APPROVED.value
        row.workflow_status = "approved"

    def activate(self, row) -> None:
        if row.status not in {
            ApplicationStatus.APPROVED.value,
            ApplicationStatus.SUSPENDED.value,
        }:
            raise InvalidApplicationState("Application cannot be activated from current status")
        row.status = ApplicationStatus.ACTIVE.value

    def suspend(self, row) -> None:
        if row.status not in {
            ApplicationStatus.ACTIVE.value,
            ApplicationStatus.APPROVED.value,
        }:
            raise InvalidApplicationState("Application cannot be suspended from current status")
        row.status = ApplicationStatus.SUSPENDED.value

    def retire(self, row) -> None:
        if row.status == ApplicationStatus.RETIRED.value:
            raise InvalidApplicationState("Application already retired")
        row.status = ApplicationStatus.RETIRED.value
