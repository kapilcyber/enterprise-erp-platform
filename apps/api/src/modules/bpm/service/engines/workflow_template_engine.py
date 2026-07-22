"""WorkflowTemplate lifecycle engine."""

from modules.bpm.domain.enums import TemplateStatus
from modules.bpm.domain.exceptions import InvalidTemplateState


class WorkflowTemplateEngine:
    def activate(self, row) -> None:
        if row.status not in {TemplateStatus.DRAFT.value, TemplateStatus.RETIRED.value}:
            raise InvalidTemplateState("Only draft or retired templates can be activated")
        row.status = TemplateStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status != TemplateStatus.ACTIVE.value:
            raise InvalidTemplateState("Only active templates can be retired")
        row.status = TemplateStatus.RETIRED.value
