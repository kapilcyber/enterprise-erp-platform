"""Subscription eligibility — metadata binding rules only (not Hub/gateway enforcement)."""

from modules.devportal.domain.enums import ApiProductVersionStatus, PlanStatus
from modules.devportal.domain.exceptions import SubscriptionBindingError
from modules.devportal.domain.value_objects import ValidationIssue


class SubscriptionEligibilityEngine:
    def validate_binding(self, *, plan, product_version, application) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if plan is None:
            issues.append(
                ValidationIssue(code="MISSING_PLAN", message="plan_id is required", field="plan_id")
            )
        elif plan.status != PlanStatus.PUBLISHED.value:
            issues.append(
                ValidationIssue(
                    code="PLAN_NOT_PUBLISHED",
                    message="Subscription requires a published plan",
                    field="plan_id",
                )
            )
        if product_version is None:
            issues.append(
                ValidationIssue(
                    code="MISSING_PRODUCT_VERSION",
                    message="product_version_id is required",
                    field="product_version_id",
                )
            )
        elif product_version.status != ApiProductVersionStatus.PUBLISHED.value:
            issues.append(
                ValidationIssue(
                    code="PRODUCT_VERSION_NOT_PUBLISHED",
                    message="Subscription requires a published API product version",
                    field="product_version_id",
                )
            )
        if application is None:
            issues.append(
                ValidationIssue(
                    code="MISSING_APPLICATION",
                    message="application_id is required",
                    field="application_id",
                )
            )
        return issues

    def assert_binding_ok(self, *, plan, product_version, application) -> None:
        issues = self.validate_binding(
            plan=plan, product_version=product_version, application=application
        )
        if issues:
            raise SubscriptionBindingError("; ".join(i.code for i in issues))
