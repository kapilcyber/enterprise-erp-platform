"""AiModel lifecycle engine — draft → approve → deprecate → retire."""

from modules.ai.domain.enums import ModelStatus
from modules.ai.domain.exceptions import InvalidModelState


class ModelEngine:
    def approve(self, row) -> None:
        if row.status != ModelStatus.DRAFT.value:
            raise InvalidModelState("Only draft models can be approved")
        row.status = ModelStatus.APPROVED.value

    def deprecate(self, row) -> None:
        if row.status != ModelStatus.APPROVED.value:
            raise InvalidModelState("Only approved models can be deprecated")
        row.status = ModelStatus.DEPRECATED.value

    def retire(self, row) -> None:
        if row.status not in {
            ModelStatus.APPROVED.value,
            ModelStatus.DEPRECATED.value,
            ModelStatus.DRAFT.value,
        }:
            raise InvalidModelState("Model cannot be retired from current state")
        row.status = ModelStatus.RETIRED.value
