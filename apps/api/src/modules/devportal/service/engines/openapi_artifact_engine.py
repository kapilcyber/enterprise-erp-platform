"""OpenAPI artifact reference consistency — metadata only; Document remains SoR."""

from modules.devportal.domain.enums import OpenApiArtifactStatus
from modules.devportal.domain.exceptions import InvalidOpenApiArtifactState
from modules.devportal.domain.value_objects import ValidationIssue


class OpenApiArtifactEngine:
    def validate_reference(self, *, document_id, product_version_id) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if document_id is None:
            issues.append(
                ValidationIssue(
                    code="MISSING_DOCUMENT_ID",
                    message="document_id UUID is required (Document Management SoR)",
                    field="document_id",
                )
            )
        if product_version_id is None:
            issues.append(
                ValidationIssue(
                    code="MISSING_PRODUCT_VERSION",
                    message="product_version_id is required",
                    field="product_version_id",
                )
            )
        return issues

    def retire(self, row) -> None:
        if row.status == OpenApiArtifactStatus.RETIRED.value:
            raise InvalidOpenApiArtifactState("OpenAPI artifact reference already retired")
        row.status = OpenApiArtifactStatus.RETIRED.value

    def activate(self, row) -> None:
        if row.status != OpenApiArtifactStatus.RETIRED.value:
            raise InvalidOpenApiArtifactState("Only retired artifacts can be reactivated")
        row.status = OpenApiArtifactStatus.ACTIVE.value
