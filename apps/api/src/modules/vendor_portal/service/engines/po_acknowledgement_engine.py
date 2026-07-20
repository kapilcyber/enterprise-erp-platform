"""VpPoAcknowledgement lifecycle engine."""

from modules.vendor_portal.domain.enums import PoAcknowledgementStatus
from modules.vendor_portal.domain.exceptions import InvalidPoAcknowledgementState


class PoAcknowledgementEngine:

    def submit(self, row) -> None:
        if row.status != PoAcknowledgementStatus.DRAFT.value:
            raise InvalidPoAcknowledgementState("Only draft rows can be submitted")
        row.status = PoAcknowledgementStatus.SUBMITTED.value

    def approve(self, row) -> None:
        if row.status != PoAcknowledgementStatus.SUBMITTED.value:
            raise InvalidPoAcknowledgementState("Only submitted rows can be acknowledged")
        row.status = PoAcknowledgementStatus.ACKNOWLEDGED.value

