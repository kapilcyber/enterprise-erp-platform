"""AiProvider lifecycle engine — activate / suspend / retire."""

from modules.ai.domain.enums import ProviderStatus
from modules.ai.domain.exceptions import InvalidProviderState


class ProviderEngine:
    def activate(self, row) -> None:
        if row.status == ProviderStatus.RETIRED.value:
            raise InvalidProviderState("Retired providers cannot be activated")
        if row.status == ProviderStatus.ACTIVE.value:
            raise InvalidProviderState("Provider already active")
        row.status = ProviderStatus.ACTIVE.value

    def suspend(self, row) -> None:
        if row.status != ProviderStatus.ACTIVE.value:
            raise InvalidProviderState("Only active providers can be suspended")
        row.status = ProviderStatus.SUSPENDED.value

    def retire(self, row) -> None:
        if row.status == ProviderStatus.RETIRED.value:
            raise InvalidProviderState("Provider already retired")
        row.status = ProviderStatus.RETIRED.value
