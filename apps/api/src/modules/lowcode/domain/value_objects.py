"""Low-Code value objects — Phase 1 · 2A."""

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class ValidationIssue:
    code: str
    message: str
    severity: str = "error"
    field: str | None = None


@dataclass
class PublishValidationResult:
    valid: bool
    version_id: UUID
    definition_id: UUID
    issues: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "version_id": str(self.version_id),
            "definition_id": str(self.definition_id),
            "issues": [
                {"code": i.code, "message": i.message, "severity": i.severity, "field": i.field}
                for i in self.issues
            ],
            "warnings": [
                {"code": w.code, "message": w.message, "severity": w.severity, "field": w.field}
                for w in self.warnings
            ],
        }


@dataclass
class StructureValidationResult:
    valid: bool
    form_version_id: UUID
    issues: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "form_version_id": str(self.form_version_id),
            "issues": [
                {"code": i.code, "message": i.message, "severity": i.severity, "field": i.field}
                for i in self.issues
            ],
            "warnings": [
                {"code": w.code, "message": w.message, "severity": w.severity, "field": w.field}
                for w in self.warnings
            ],
        }


@dataclass
class PageResult:
    items: list
    total: int
    page: int
    page_size: int
    sort_by: str | None = None
    sort_dir: str = "asc"

    def to_dict(self) -> dict[str, Any]:
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "page_size": self.page_size,
            "sort_by": self.sort_by,
            "sort_dir": self.sort_dir,
        }
