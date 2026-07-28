"""Developer account lifecycle engine — Draft → Submit → Approve → Active / Lock / Suspend → Retire."""  # noqa: E501

from modules.devportal.domain.enums import DeveloperAccountStatus
from modules.devportal.domain.exceptions import InvalidDeveloperAccountState


class AccountLifecycleEngine:
    def submit(self, row) -> None:
        if row.status != DeveloperAccountStatus.DRAFT.value:
            raise InvalidDeveloperAccountState("Only draft accounts can be submitted")
        row.status = DeveloperAccountStatus.SUBMITTED.value
        row.workflow_status = "pending"

    def approve(self, row) -> None:
        if row.status != DeveloperAccountStatus.SUBMITTED.value:
            raise InvalidDeveloperAccountState("Only submitted accounts can be approved")
        row.status = DeveloperAccountStatus.APPROVED.value
        row.workflow_status = "approved"

    def activate(self, row) -> None:
        if row.status not in {
            DeveloperAccountStatus.APPROVED.value,
            DeveloperAccountStatus.SUSPENDED.value,
            DeveloperAccountStatus.LOCKED.value,
        }:
            raise InvalidDeveloperAccountState("Account cannot be activated from current status")
        row.status = DeveloperAccountStatus.ACTIVE.value

    def lock(self, row) -> None:
        if row.status != DeveloperAccountStatus.ACTIVE.value:
            raise InvalidDeveloperAccountState("Only active accounts can be locked")
        row.status = DeveloperAccountStatus.LOCKED.value

    def suspend(self, row) -> None:
        if row.status not in {
            DeveloperAccountStatus.ACTIVE.value,
            DeveloperAccountStatus.APPROVED.value,
        }:
            raise InvalidDeveloperAccountState("Account cannot be suspended from current status")
        row.status = DeveloperAccountStatus.SUSPENDED.value

    def retire(self, row) -> None:
        if row.status == DeveloperAccountStatus.RETIRED.value:
            raise InvalidDeveloperAccountState("Account already retired")
        row.status = DeveloperAccountStatus.RETIRED.value
