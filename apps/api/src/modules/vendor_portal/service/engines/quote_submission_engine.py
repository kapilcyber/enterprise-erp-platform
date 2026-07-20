"""VpQuoteSubmission lifecycle engine."""

from modules.vendor_portal.domain.enums import QuoteSubmissionStatus
from modules.vendor_portal.domain.exceptions import InvalidQuoteSubmissionState


class QuoteSubmissionEngine:

    def submit(self, row) -> None:
        if row.status != QuoteSubmissionStatus.DRAFT.value:
            raise InvalidQuoteSubmissionState("Only draft rows can be submitted")
        row.status = QuoteSubmissionStatus.SUBMITTED.value

    def approve(self, row) -> None:
        if row.status != QuoteSubmissionStatus.SUBMITTED.value:
            raise InvalidQuoteSubmissionState("Only submitted rows can be accepted")
        row.status = QuoteSubmissionStatus.ACCEPTED.value

