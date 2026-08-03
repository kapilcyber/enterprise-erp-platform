"""Service policy assignment lifecycle — Active ↔ Inactive → Retired."""

from modules.monitoring.domain.enums import AssignmentStatus
from modules.monitoring.domain.exceptions import InvalidAssignmentState


class AssignmentLifecycleEngine:
    def activate(self, row) -> None:
        if row.status == AssignmentStatus.RETIRED.value:
            raise InvalidAssignmentState("Retired assignments cannot be activated")
        row.status = AssignmentStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status == AssignmentStatus.RETIRED.value:
            raise InvalidAssignmentState("Retired assignments cannot be deactivated")
        row.status = AssignmentStatus.INACTIVE.value

    def retire(self, row) -> None:
        if row.status == AssignmentStatus.RETIRED.value:
            raise InvalidAssignmentState("Assignment already retired")
        row.status = AssignmentStatus.RETIRED.value
