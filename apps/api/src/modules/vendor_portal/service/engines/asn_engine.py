"""VpAsn lifecycle engine."""

from modules.vendor_portal.domain.enums import AsnStatus
from modules.vendor_portal.domain.exceptions import InvalidAsnState


class AsnEngine:

    def submit(self, row) -> None:
        if row.status != AsnStatus.DRAFT.value:
            raise InvalidAsnState("Only draft rows can be submitted")
        row.status = AsnStatus.SUBMITTED.value

    def approve(self, row) -> None:
        if row.status != AsnStatus.SUBMITTED.value:
            raise InvalidAsnState("Only submitted rows can be approved")
        row.status = AsnStatus.APPROVED.value

