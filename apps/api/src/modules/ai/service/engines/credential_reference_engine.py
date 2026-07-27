"""Provider credential reference lifecycle — activate / rotate / retire."""

from modules.ai.domain.enums import CredentialReferenceStatus
from modules.ai.domain.exceptions import InvalidCredentialReferenceState


class CredentialReferenceEngine:
    def activate(self, row) -> None:
        if row.status == CredentialReferenceStatus.RETIRED.value:
            raise InvalidCredentialReferenceState(
                "Retired credential references cannot be activated"
            )
        if row.status == CredentialReferenceStatus.ACTIVE.value:
            raise InvalidCredentialReferenceState("Credential reference already active")
        row.status = CredentialReferenceStatus.ACTIVE.value

    def rotate(self, row) -> None:
        if row.status != CredentialReferenceStatus.ACTIVE.value:
            raise InvalidCredentialReferenceState(
                "Only active credential references can be rotated"
            )
        row.status = CredentialReferenceStatus.ROTATED.value

    def retire(self, row) -> None:
        if row.status == CredentialReferenceStatus.RETIRED.value:
            raise InvalidCredentialReferenceState("Credential reference already retired")
        row.status = CredentialReferenceStatus.RETIRED.value
