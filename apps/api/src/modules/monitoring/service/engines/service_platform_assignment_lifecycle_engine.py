"""Service platform assignment lifecycle — Active ↔ Inactive → Retired."""

from modules.monitoring.domain.enums import AssignmentStatus
from modules.monitoring.domain.exceptions import InvalidAssignmentState


class ServicePlatformAssignmentLifecycleEngine:
    def activate(self, row) -> None:
        if row.status == AssignmentStatus.RETIRED.value:
            raise InvalidAssignmentState("Retired platform assignments cannot be activated")
        row.status = AssignmentStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status == AssignmentStatus.RETIRED.value:
            raise InvalidAssignmentState("Retired platform assignments cannot be deactivated")
        row.status = AssignmentStatus.INACTIVE.value

    def retire(self, row) -> None:
        if row.status == AssignmentStatus.RETIRED.value:
            raise InvalidAssignmentState("Platform assignment already retired")
        row.status = AssignmentStatus.RETIRED.value
