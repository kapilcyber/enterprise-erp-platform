"""Low-Code document numbering."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.lowcode.domain.enums import LowcodeEntityType
from modules.lowcode.repository.code_sequence_repository import CodeSequenceRepository


class LowcodeNumberService:
    def __init__(self, db: Session) -> None:
        self._seq = CodeSequenceRepository(db)

    def generate(
        self, entity: LowcodeEntityType, company_id: UUID, model, code_column: str
    ) -> str:
        return self._seq.next_code(entity, company_id, model, code_column)
