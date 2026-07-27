"""Vector index lifecycle engine — start rebuild / activate / retire."""

from modules.ai.domain.enums import VectorIndexStatus
from modules.ai.domain.exceptions import InvalidVectorIndexState


class VectorIndexEngine:
    def start_rebuild(self, row) -> None:
        if row.status == VectorIndexStatus.RETIRED.value:
            raise InvalidVectorIndexState("Retired vector indexes cannot be rebuilt")
        row.status = VectorIndexStatus.REBUILDING.value

    def activate(self, row) -> None:
        if row.status == VectorIndexStatus.RETIRED.value:
            raise InvalidVectorIndexState("Retired vector indexes cannot be activated")
        row.status = VectorIndexStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status == VectorIndexStatus.RETIRED.value:
            raise InvalidVectorIndexState("Vector index is already retired")
        row.status = VectorIndexStatus.RETIRED.value
