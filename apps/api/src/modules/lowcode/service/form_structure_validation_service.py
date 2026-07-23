"""Form structure validation — Phase 2A."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.domain.value_objects import StructureValidationResult, ValidationIssue
from modules.lowcode.repository.form_field_repository import FormFieldRepository
from modules.lowcode.repository.form_section_repository import FormSectionRepository
from modules.lowcode.repository.form_version_repository import FormVersionRepository


class FormStructureValidationService:
    def __init__(self, db: Session) -> None:
        self._versions = FormVersionRepository(db)
        self._sections = FormSectionRepository(db)
        self._fields = FormFieldRepository(db)

    def validate(self, ctx: TenantContext, form_version_id: UUID) -> StructureValidationResult:
        version = self._versions.get(ctx, form_version_id)
        if version is None:
            raise NotFoundException("Form version not found")

        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []

        sections = self._sections.list_by_version(ctx, form_version_id)
        fields = self._fields.list_by_version(ctx, form_version_id)
        section_ids = {s.id for s in sections}

        keys: dict[str, UUID] = {}
        for f in fields:
            if f.display_order < 0:
                issues.append(
                    ValidationIssue(
                        code="FIELD_DISPLAY_ORDER",
                        message=f"Field '{f.field_key}' has invalid display_order",
                        field=f.field_key,
                    )
                )
            if f.field_key in keys:
                issues.append(
                    ValidationIssue(
                        code="DUPLICATE_FIELD_KEY",
                        message=f"Duplicate field_key '{f.field_key}'",
                        field=f.field_key,
                    )
                )
            else:
                keys[f.field_key] = f.id
            if f.section_id is not None and f.section_id not in section_ids:
                issues.append(
                    ValidationIssue(
                        code="ORPHAN_SECTION_REF",
                        message=f"Field '{f.field_key}' references missing/deleted section",
                        field=f.field_key,
                    )
                )

        for s in sections:
            if s.display_order < 0:
                issues.append(
                    ValidationIssue(
                        code="SECTION_DISPLAY_ORDER",
                        message=f"Section '{s.section_code}' has invalid display_order",
                        field=s.section_code,
                    )
                )

        if not fields:
            warnings.append(
                ValidationIssue(
                    code="NO_FIELDS",
                    message="Form version has no fields yet",
                    severity="warning",
                )
            )

        return StructureValidationResult(
            valid=len(issues) == 0,
            form_version_id=form_version_id,
            issues=issues,
            warnings=warnings,
        )
