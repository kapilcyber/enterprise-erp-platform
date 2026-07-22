"""BPM document numbering."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.bpm.domain.enums import BpmEntityType
from modules.bpm.repository.code_sequence_repository import CodeSequenceRepository


class BpmNumberService:
    def __init__(self, db: Session) -> None:
        self._seq = CodeSequenceRepository(db)

    def generate(self, entity: BpmEntityType, company_id: UUID, model, code_column: str) -> str:
        return self._seq.next_code(entity, company_id, model, code_column)
