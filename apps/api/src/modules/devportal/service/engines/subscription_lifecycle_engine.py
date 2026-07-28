"""Subscription lifecycle engine — Draft → Submit → Approve → Active / Suspend → Retire."""

from modules.devportal.domain.enums import SubscriptionStatus
from modules.devportal.domain.exceptions import InvalidSubscriptionState


class SubscriptionLifecycleEngine:
    def submit(self, row) -> None:
        if row.status != SubscriptionStatus.DRAFT.value:
            raise InvalidSubscriptionState("Only draft subscriptions can be submitted")
        row.status = SubscriptionStatus.SUBMITTED.value
        row.workflow_status = "pending"

    def approve(self, row) -> None:
        if row.status != SubscriptionStatus.SUBMITTED.value:
            raise InvalidSubscriptionState("Only submitted subscriptions can be approved")
        row.status = SubscriptionStatus.APPROVED.value
        row.workflow_status = "approved"

    def activate(self, row) -> None:
        if row.status not in {
            SubscriptionStatus.APPROVED.value,
            SubscriptionStatus.SUSPENDED.value,
        }:
            raise InvalidSubscriptionState(
                "Subscription cannot be activated from current status"
            )
        row.status = SubscriptionStatus.ACTIVE.value

    def suspend(self, row) -> None:
        if row.status not in {
            SubscriptionStatus.ACTIVE.value,
            SubscriptionStatus.APPROVED.value,
        }:
            raise InvalidSubscriptionState(
                "Subscription cannot be suspended from current status"
            )
        row.status = SubscriptionStatus.SUSPENDED.value

    def retire(self, row) -> None:
        if row.status == SubscriptionStatus.RETIRED.value:
            raise InvalidSubscriptionState("Subscription already retired")
        row.status = SubscriptionStatus.RETIRED.value
