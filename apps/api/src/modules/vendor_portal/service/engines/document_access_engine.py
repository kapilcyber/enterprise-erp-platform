"""VpDocumentAccess lifecycle engine."""

from modules.vendor_portal.domain.enums import DocumentAccessStatus
from modules.vendor_portal.domain.exceptions import InvalidDocumentAccessState


class DocumentAccessEngine:

    def submit(self, row) -> None:
        if row.status != DocumentAccessStatus.DRAFT.value:
            raise InvalidDocumentAccessState("Only draft rows can be submitted")
        row.status = DocumentAccessStatus.SUBMITTED.value

    def approve(self, row) -> None:
        if row.status != DocumentAccessStatus.SUBMITTED.value:
            raise InvalidDocumentAccessState("Only submitted rows can be approved")
        row.status = DocumentAccessStatus.APPROVED.value

