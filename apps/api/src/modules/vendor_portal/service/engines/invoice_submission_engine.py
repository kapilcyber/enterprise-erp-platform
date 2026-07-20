"""VpInvoiceSubmission lifecycle engine."""

from modules.vendor_portal.domain.enums import InvoiceSubmissionStatus
from modules.vendor_portal.domain.exceptions import InvalidInvoiceSubmissionState


class InvoiceSubmissionEngine:

    def submit(self, row) -> None:
        if row.status != InvoiceSubmissionStatus.DRAFT.value:
            raise InvalidInvoiceSubmissionState("Only draft rows can be submitted")
        row.status = InvoiceSubmissionStatus.SUBMITTED.value

    def approve(self, row) -> None:
        if row.status != InvoiceSubmissionStatus.SUBMITTED.value:
            raise InvalidInvoiceSubmissionState("Only submitted rows can be accepted")
        row.status = InvoiceSubmissionStatus.ACCEPTED.value

