"""Vendor Portal document number service."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.vendor_portal.domain.enums import VendorPortalEntityType
from modules.vendor_portal.repository.code_sequence_repository import CodeSequenceRepository


class VendorPortalNumberService:
    def __init__(self, db: Session) -> None:
        self._seq = CodeSequenceRepository(db)

    def generate(
        self,
        entity_type: VendorPortalEntityType,
        company_id: UUID,
        model,
        field: str,
    ) -> str:
        return self._seq.next_code(entity_type, company_id, model, field)
