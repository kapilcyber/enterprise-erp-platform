"""Entitlement metadata engine — no runtime / gateway enforcement."""

from modules.devportal.domain.enums import EntitlementStatus
from modules.devportal.domain.exceptions import InvalidEntitlementState


class EntitlementEngine:
    def suspend(self, row) -> None:
        if row.status != EntitlementStatus.ACTIVE.value:
            raise InvalidEntitlementState("Only active entitlements can be suspended")
        row.status = EntitlementStatus.SUSPENDED.value

    def activate(self, row) -> None:
        if row.status not in {
            EntitlementStatus.SUSPENDED.value,
            EntitlementStatus.RETIRED.value,
        }:
            raise InvalidEntitlementState("Entitlement cannot be activated from current status")
        row.status = EntitlementStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status == EntitlementStatus.RETIRED.value:
            raise InvalidEntitlementState("Entitlement already retired")
        row.status = EntitlementStatus.RETIRED.value
