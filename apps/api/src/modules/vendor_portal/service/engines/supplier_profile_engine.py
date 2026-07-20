"""VpSupplierProfile lifecycle engine."""

from modules.vendor_portal.domain.enums import SupplierProfileStatus
from modules.vendor_portal.domain.exceptions import InvalidSupplierProfileState


class SupplierProfileEngine:

    def submit(self, row) -> None:
        if row.status != SupplierProfileStatus.DRAFT.value:
            raise InvalidSupplierProfileState("Only draft rows can be submitted")
        row.status = SupplierProfileStatus.SUBMITTED.value

    def approve(self, row) -> None:
        if row.status != SupplierProfileStatus.SUBMITTED.value:
            raise InvalidSupplierProfileState("Only submitted rows can be approved")
        row.status = SupplierProfileStatus.APPROVED.value

