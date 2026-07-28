"""Developer invite lifecycle — approval workflow metadata; Foundation executes workflow."""

from modules.devportal.domain.enums import DeveloperInviteStatus
from modules.devportal.domain.exceptions import InvalidDeveloperInviteState


class InviteLifecycleEngine:
    def submit(self, row) -> None:
        if row.status != DeveloperInviteStatus.DRAFT.value:
            raise InvalidDeveloperInviteState("Only draft invites can be submitted for approval")
        row.status = DeveloperInviteStatus.SUBMITTED.value
        row.workflow_status = "pending"

    def approve(self, row) -> None:
        if row.status != DeveloperInviteStatus.SUBMITTED.value:
            raise InvalidDeveloperInviteState("Only submitted invites can be approved")
        row.status = DeveloperInviteStatus.APPROVED.value
        row.workflow_status = "approved"

    def mark_sent(self, row) -> None:
        if row.status != DeveloperInviteStatus.APPROVED.value:
            raise InvalidDeveloperInviteState("Only approved invites can be marked sent")
        row.status = DeveloperInviteStatus.SENT.value

    def accept(self, row) -> None:
        if row.status != DeveloperInviteStatus.SENT.value:
            raise InvalidDeveloperInviteState("Only sent invites can be accepted")
        row.status = DeveloperInviteStatus.ACCEPTED.value

    def expire(self, row) -> None:
        if row.status not in {
            DeveloperInviteStatus.SENT.value,
            DeveloperInviteStatus.APPROVED.value,
            DeveloperInviteStatus.SUBMITTED.value,
        }:
            raise InvalidDeveloperInviteState("Invite cannot expire from current status")
        row.status = DeveloperInviteStatus.EXPIRED.value

    def revoke(self, row) -> None:
        if row.status in {
            DeveloperInviteStatus.ACCEPTED.value,
            DeveloperInviteStatus.REVOKED.value,
            DeveloperInviteStatus.EXPIRED.value,
        }:
            raise InvalidDeveloperInviteState("Invite cannot be revoked from current status")
        row.status = DeveloperInviteStatus.REVOKED.value
