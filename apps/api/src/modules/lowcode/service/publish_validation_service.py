"""Phase 1 publish validation — draft status gate (structure validation later)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.domain.enums import VersionStatus
from modules.lowcode.domain.value_objects import PublishValidationResult, ValidationIssue
from modules.lowcode.repository.form_version_repository import FormVersionRepository


class PublishValidationService:
    def __init__(self, db: Session) -> None:
        self._versions = FormVersionRepository(db)

    def validate(self, ctx: TenantContext, row_id: UUID) -> PublishValidationResult:
        row = self._versions.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Form version not found")
        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []
        if row.status != VersionStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="NOT_DRAFT",
                    message=f"Only draft versions can be published (status={row.status})",
                )
            )
        return PublishValidationResult(
            valid=len(issues) == 0,
            version_id=row.id,
            definition_id=row.definition_id,
            issues=issues,
            warnings=warnings,
        )
