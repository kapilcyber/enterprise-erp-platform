"""Agent catalog lifecycle engine — activate / deactivate."""

from modules.ai.domain.enums import AgentStatus
from modules.ai.domain.exceptions import InvalidAgentState


class AgentEngine:
    def activate(self, row) -> None:
        if row.status == AgentStatus.ACTIVE.value:
            raise InvalidAgentState("Agent already active")
        row.status = AgentStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status != AgentStatus.ACTIVE.value:
            raise InvalidAgentState("Only active agents can be deactivated")
        row.status = AgentStatus.INACTIVE.value
