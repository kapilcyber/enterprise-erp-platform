"""VpPortalAccount lifecycle engine."""

from modules.vendor_portal.domain.enums import PortalAccountStatus
from modules.vendor_portal.domain.exceptions import InvalidPortalAccountState


class PortalAccountEngine:

    def submit(self, row) -> None:
        if row.status != PortalAccountStatus.DRAFT.value:
            raise InvalidPortalAccountState("Only draft rows can be submitted")
        row.status = PortalAccountStatus.SUBMITTED.value

    def approve(self, row) -> None:
        if row.status != PortalAccountStatus.SUBMITTED.value:
            raise InvalidPortalAccountState("Only submitted rows can be approved")
        row.status = PortalAccountStatus.APPROVED.value

