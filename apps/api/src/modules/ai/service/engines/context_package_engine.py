"""Context package lifecycle engine — expire / purge."""

from modules.ai.domain.enums import ContextPackageStatus
from modules.ai.domain.exceptions import InvalidContextPackageState


class ContextPackageEngine:
    def expire(self, row) -> None:
        if row.status != ContextPackageStatus.ACTIVE.value:
            raise InvalidContextPackageState("Only active context packages can be expired")
        row.status = ContextPackageStatus.EXPIRED.value

    def purge(self, row) -> None:
        if row.status == ContextPackageStatus.PURGED.value:
            raise InvalidContextPackageState("Context package already purged")
        row.status = ContextPackageStatus.PURGED.value
