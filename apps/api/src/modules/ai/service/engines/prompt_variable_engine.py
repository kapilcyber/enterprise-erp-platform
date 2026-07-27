"""PromptVariable lifecycle engine — editable only on draft prompt version."""

from modules.ai.domain.enums import PromptVersionStatus
from modules.ai.domain.exceptions import InvalidPromptVariableState


class PromptVariableEngine:
    def assert_editable_on_draft_version(self, version_status: str) -> None:
        if version_status != PromptVersionStatus.DRAFT.value:
            raise InvalidPromptVariableState(
                "Prompt variables are editable only on draft prompt versions"
            )
