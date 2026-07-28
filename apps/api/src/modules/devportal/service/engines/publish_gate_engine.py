"""Publish gate — pure policy helpers for API product version publishability."""

from modules.devportal.domain.enums import ApiProductVersionStatus
from modules.devportal.domain.value_objects import ValidationIssue


class PublishGateEngine:
    def validate_draft_for_publish(self, row) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if row.status != ApiProductVersionStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="NOT_DRAFT",
                    message="Only draft versions can be published",
                    field="status",
                )
            )
        if not getattr(row, "version_label", None):
            issues.append(
                ValidationIssue(
                    code="MISSING_VERSION_LABEL",
                    message="version_label is required",
                    field="version_label",
                )
            )
        if not getattr(row, "product_id", None):
            issues.append(
                ValidationIssue(
                    code="MISSING_PRODUCT",
                    message="product_id is required",
                    field="product_id",
                )
            )
        return issues
