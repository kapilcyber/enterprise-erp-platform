"""PageDefinition lifecycle engine — Phase 3B."""

from modules.lowcode.domain.enums import PageDefinitionStatus
from modules.lowcode.domain.exceptions import InvalidPageDefinitionState


class PageDefinitionEngine:
    def activate(self, row) -> None:
        if row.status == PageDefinitionStatus.ACTIVE.value:
            raise InvalidPageDefinitionState("Page definition already active")
        if row.status == PageDefinitionStatus.RETIRED.value:
            raise InvalidPageDefinitionState("Retired page definitions cannot be activated")
        row.status = PageDefinitionStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status == PageDefinitionStatus.RETIRED.value:
            raise InvalidPageDefinitionState("Page definition already retired")
        row.status = PageDefinitionStatus.RETIRED.value
