"""Template JSON import/export — Phase 1.5 validation-focused."""

from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.value_objects import TemplateImportValidationResult, ValidationIssue
from modules.bpm.repository.workflow_category_repository import WorkflowCategoryRepository
from modules.bpm.repository.workflow_template_repository import WorkflowTemplateRepository
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.foundation.domain.value_objects import TenantContext

_EXPORT_FIELDS = (
    "template_code",
    "template_name",
    "description",
    "status",
    "module_code",
    "entity_type",
)


class TemplateImportExportService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowTemplateRepository(db)
        self._categories = WorkflowCategoryRepository(db)
        self._scope = BpmScopeValidator(db)

    def export_json(self, ctx: TenantContext, template_id: UUID) -> dict[str, Any]:
        row = self._repo.get(ctx, template_id)
        if row is None:
            raise NotFoundException("Workflow template not found")
        payload = {f: getattr(row, f) for f in _EXPORT_FIELDS}
        payload["schema"] = "bpm.workflow_template.v1"
        payload["category_code"] = None
        if row.category_id:
            cat = self._categories.get(ctx, row.category_id)
            if cat:
                payload["category_code"] = cat.category_code
        return payload

    def validate_import(
        self, ctx: TenantContext, payload: dict[str, Any], company_id: UUID | None = None
    ) -> TemplateImportValidationResult:
        _ = self._scope.resolve_company_id(ctx, company_id)
        issues: list[ValidationIssue] = []

        if not isinstance(payload, dict):
            return TemplateImportValidationResult(
                valid=False,
                issues=[
                    ValidationIssue(
                        code="PAYLOAD_TYPE",
                        message="Import payload must be a JSON object",
                    )
                ],
            )

        schema = payload.get("schema")
        if schema and schema != "bpm.workflow_template.v1":
            issues.append(
                ValidationIssue(
                    code="SCHEMA_UNSUPPORTED",
                    message=f"Unsupported schema: {schema}",
                    field="schema",
                )
            )

        name = payload.get("template_name")
        if not name or not isinstance(name, str) or not name.strip():
            issues.append(
                ValidationIssue(
                    code="NAME_REQUIRED",
                    message="template_name is required",
                    field="template_name",
                )
            )

        status = payload.get("status", "draft")
        if status not in {"draft", "active", "retired"}:
            issues.append(
                ValidationIssue(
                    code="STATUS_INVALID",
                    message=f"Invalid status: {status}",
                    field="status",
                )
            )

        category_code = payload.get("category_code")
        if category_code is not None and not isinstance(category_code, str):
            issues.append(
                ValidationIssue(
                    code="CATEGORY_CODE_TYPE",
                    message="category_code must be a string",
                    field="category_code",
                )
            )

        cleaned = {
            "template_name": name.strip() if isinstance(name, str) else name,
            "description": payload.get("description"),
            "status": status,
            "module_code": payload.get("module_code"),
            "entity_type": payload.get("entity_type"),
            "category_code": category_code,
            "schema": "bpm.workflow_template.v1",
        }
        return TemplateImportValidationResult(
            valid=len(issues) == 0,
            issues=issues,
            payload=cleaned if len(issues) == 0 else None,
        )
