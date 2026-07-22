"""Publish validation service — Phase 1.5."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import CategoryStatus, TemplateStatus, VersionStatus
from modules.bpm.domain.value_objects import PublishValidationResult, ValidationIssue
from modules.bpm.repository.workflow_category_repository import WorkflowCategoryRepository
from modules.bpm.repository.workflow_definition_repository import WorkflowDefinitionRepository
from modules.bpm.repository.workflow_template_repository import WorkflowTemplateRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.foundation.domain.value_objects import TenantContext


class PublishValidationService:
    """Validate a draft version before publish. Returns structured result (no side effects)."""

    def __init__(self, db: Session) -> None:
        self._versions = WorkflowVersionRepository(db)
        self._definitions = WorkflowDefinitionRepository(db)
        self._templates = WorkflowTemplateRepository(db)
        self._categories = WorkflowCategoryRepository(db)

    def validate(self, ctx: TenantContext, version_id: UUID) -> PublishValidationResult:
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")

        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []

        # Version state
        if version.status != VersionStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="VERSION_NOT_DRAFT",
                    message=f"Only draft versions can be published (current={version.status})",
                    field="status",
                )
            )

        definition = self._definitions.get(ctx, version.definition_id)
        if definition is None:
            issues.append(
                ValidationIssue(
                    code="DEFINITION_INVALID",
                    message="Definition not found or archived",
                    field="definition_id",
                )
            )
            return PublishValidationResult(
                valid=False,
                version_id=version.id,
                definition_id=version.definition_id,
                issues=issues,
                warnings=warnings,
            )

        # Exactly one published — warn if another exists (publish will retire it)
        published_count = self._versions.count_published(ctx, definition.id)
        if published_count > 1:
            issues.append(
                ValidationIssue(
                    code="MULTIPLE_PUBLISHED",
                    message="Definition already has more than one published version",
                    field="definition_id",
                )
            )
        elif published_count == 1:
            warnings.append(
                ValidationIssue(
                    code="PRIOR_PUBLISHED_WILL_RETIRE",
                    message="Existing published version will be retired on publish",
                    severity="warning",
                    field="definition_id",
                )
            )

        # Template dependency
        if definition.template_id:
            template = self._templates.get(ctx, definition.template_id)
            if template is None:
                issues.append(
                    ValidationIssue(
                        code="TEMPLATE_INVALID",
                        message="Linked template not found or archived",
                        field="template_id",
                    )
                )
            else:
                if template.status == TemplateStatus.RETIRED.value:
                    warnings.append(
                        ValidationIssue(
                            code="TEMPLATE_RETIRED",
                            message="Linked template is retired",
                            severity="warning",
                            field="template_id",
                        )
                    )
                if template.category_id:
                    category = self._categories.get(ctx, template.category_id)
                    if category is None:
                        issues.append(
                            ValidationIssue(
                                code="CATEGORY_INVALID",
                                message="Linked category not found or archived",
                                field="category_id",
                            )
                        )
                    elif category.status == CategoryStatus.INACTIVE.value:
                        warnings.append(
                            ValidationIssue(
                                code="CATEGORY_INACTIVE",
                                message="Linked category is inactive",
                                severity="warning",
                                field="category_id",
                            )
                        )

        # Ownership
        if definition.owner_employee_id is None:
            warnings.append(
                ValidationIssue(
                    code="OWNERSHIP_MISSING",
                    message="Definition has no owner_employee_id",
                    severity="warning",
                    field="owner_employee_id",
                )
            )

        # Module / entity binding
        if not definition.module_code or not definition.entity_type:
            issues.append(
                ValidationIssue(
                    code="DEPENDENCY_MODULE_ENTITY",
                    message="Definition requires module_code and entity_type",
                    field="module_code",
                )
            )

        return PublishValidationResult(
            valid=len(issues) == 0,
            version_id=version.id,
            definition_id=definition.id,
            issues=issues,
            warnings=warnings,
        )
