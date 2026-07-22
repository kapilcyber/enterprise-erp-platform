"""WorkflowDefinition lifecycle engine."""

from modules.bpm.domain.enums import DefinitionStatus
from modules.bpm.domain.exceptions import InvalidDefinitionState


class WorkflowDefinitionEngine:
    def activate(self, row) -> None:
        if row.status not in {DefinitionStatus.DRAFT.value, DefinitionStatus.RETIRED.value}:
            raise InvalidDefinitionState("Only draft or retired definitions can be activated")
        row.status = DefinitionStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status != DefinitionStatus.ACTIVE.value:
            raise InvalidDefinitionState("Only active definitions can be retired")
        row.status = DefinitionStatus.RETIRED.value
