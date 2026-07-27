"""Prompt template lifecycle engine — activate / deactivate."""

from modules.ai.domain.enums import PromptTemplateStatus
from modules.ai.domain.exceptions import InvalidPromptTemplateState


class PromptTemplateEngine:
    def activate(self, row) -> None:
        if row.status == PromptTemplateStatus.ACTIVE.value:
            raise InvalidPromptTemplateState("Prompt template already active")
        row.status = PromptTemplateStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status != PromptTemplateStatus.ACTIVE.value:
            raise InvalidPromptTemplateState("Only active prompt templates can be deactivated")
        row.status = PromptTemplateStatus.INACTIVE.value
