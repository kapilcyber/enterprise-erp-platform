"""FormDefinition lifecycle engine."""

from modules.lowcode.domain.enums import DefinitionStatus
from modules.lowcode.domain.exceptions import InvalidDefinitionState


class FormDefinitionEngine:
    def activate(self, row) -> None:
        if row.status == DefinitionStatus.ACTIVE.value:
            raise InvalidDefinitionState("Definition already active")
        if row.status == DefinitionStatus.RETIRED.value:
            raise InvalidDefinitionState("Retired definitions cannot be activated")
        row.status = DefinitionStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status == DefinitionStatus.RETIRED.value:
            raise InvalidDefinitionState("Definition already retired")
        row.status = DefinitionStatus.RETIRED.value
