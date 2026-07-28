"""Portal session metadata lifecycle — never replaces Foundation Auth sessions."""

from modules.devportal.domain.enums import PortalSessionStatus
from modules.devportal.domain.exceptions import InvalidPortalSessionState


class PortalSessionEngine:
    def expire(self, row) -> None:
        if row.status != PortalSessionStatus.ACTIVE.value:
            raise InvalidPortalSessionState("Only active portal sessions can expire")
        row.status = PortalSessionStatus.EXPIRED.value

    def revoke(self, row) -> None:
        if row.status == PortalSessionStatus.REVOKED.value:
            raise InvalidPortalSessionState("Portal session already revoked")
        row.status = PortalSessionStatus.REVOKED.value
