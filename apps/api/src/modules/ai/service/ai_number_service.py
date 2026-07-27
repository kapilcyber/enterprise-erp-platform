"""AI Platform document numbering."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.ai.domain.enums import AiEntityType
from modules.ai.repository.code_sequence_repository import CodeSequenceRepository


class AiNumberService:
    def __init__(self, db: Session) -> None:
        self._seq = CodeSequenceRepository(db)

    def generate(
        self, entity: AiEntityType, company_id: UUID, model, code_column: str
    ) -> str:
        return self._seq.next_code(entity, company_id, model, code_column)
