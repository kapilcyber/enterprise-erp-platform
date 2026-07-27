"""AiConfiguration lifecycle engine — activate / retire from draft."""

from modules.ai.domain.enums import ConfigurationStatus
from modules.ai.domain.exceptions import InvalidConfigurationState


class ConfigurationEngine:
    def assert_editable(self, row) -> None:
        if row.status == ConfigurationStatus.RETIRED.value:
            raise InvalidConfigurationState("Retired configurations are read-only")
        if row.status == ConfigurationStatus.ACTIVE.value:
            raise InvalidConfigurationState("Active configurations are read-only")

    def activate(self, row) -> None:
        if row.status != ConfigurationStatus.DRAFT.value:
            raise InvalidConfigurationState("Only draft configurations can be activated")
        row.status = ConfigurationStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status != ConfigurationStatus.ACTIVE.value:
            raise InvalidConfigurationState("Only active configurations can be retired")
        row.status = ConfigurationStatus.RETIRED.value
