"""BPM Phase 1.5 value objects — validation / compare / page results."""

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class ValidationIssue:
    code: str
    message: str
    severity: str = "error"  # error | warning
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
class FieldDiff:
    field: str
    left: Any
    right: Any


@dataclass
class VersionComparisonResult:
    left_version_id: UUID
    right_version_id: UUID
    same_definition: bool
    differences: list[FieldDiff] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "left_version_id": str(self.left_version_id),
            "right_version_id": str(self.right_version_id),
            "same_definition": self.same_definition,
            "difference_count": len(self.differences),
            "differences": [
                {"field": d.field, "left": d.left, "right": d.right} for d in self.differences
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


@dataclass
class BpmDashboardSummary:
    categories: int
    templates: int
    definitions: int
    draft_versions: int
    published_versions: int
    retired_versions: int

    def to_dict(self) -> dict[str, int]:
        return {
            "categories": self.categories,
            "templates": self.templates,
            "definitions": self.definitions,
            "draft": self.draft_versions,
            "published": self.published_versions,
            "retired": self.retired_versions,
        }


@dataclass
class TemplateImportValidationResult:
    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    payload: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "issues": [
                {"code": i.code, "message": i.message, "severity": i.severity, "field": i.field}
                for i in self.issues
            ],
            "payload": self.payload,
        }


@dataclass
class GraphValidationResult:
    valid: bool
    version_id: UUID
    issues: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)
    node_count: int = 0
    transition_count: int = 0
    start_count: int = 0
    end_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "version_id": str(self.version_id),
            "node_count": self.node_count,
            "transition_count": self.transition_count,
            "start_count": self.start_count,
            "end_count": self.end_count,
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
class AssignmentTargetRef:
    """UUID-only cross-module assignment target (Security / Org / Master Employee)."""

    target_type: str
    target_id: UUID | None = None
    fallback_assignee_id: UUID | None = None


@dataclass
class EscalationLevelSpec:
    level: int
    delay_minutes: int
    target_type: str
    target_id: UUID | None = None
    reason: str | None = None
    retry_count: int = 0


@dataclass
class SlaThresholdSpec:
    warning_threshold_minutes: int
    breach_threshold_minutes: int
    timezone: str
    holiday_calendar_id: UUID | None = None


@dataclass
class TriggerBindingSpec:
    """Definition-owned trigger capability with optional version implementation binding."""

    definition_id: UUID
    version_id: UUID | None
    trigger_type: str
    event_name: str | None = None
    module_code: str | None = None
    entity_type: str | None = None


@dataclass
class NotificationContentSpec:
    """WHAT content for Foundation Notification delivery (no delivery engine)."""

    template_type: str
    subject: str | None = None
    body: str | None = None
    variables_json: str | None = None
    localization_json: str | None = None


@dataclass
class BusinessEntityRef:
    """UUID-only business reference — business module remains SoR."""

    module_code: str
    entity_id: UUID
    entity_type: str | None = None


@dataclass
class HistoryEventSpec:
    event_type: str
    from_status: str | None = None
    to_status: str | None = None
    actor_id: UUID | None = None
    message: str | None = None
    payload_json: str | None = None


@dataclass
class DelegationPeriodSpec:
    original_assignee_id: UUID
    delegate_assignee_id: UUID
    effective_from: Any
    effective_to: Any | None = None
    reason: str | None = None


@dataclass
class SimulationResultSummary:
    valid: bool
    nodes_visited: int
    transitions_evaluated: int
    decision_tables_evaluated: int
    business_rules_evaluated: int
    variables_resolved: int
    warning_count: int
    error_count: int
    duration_ms: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "nodes_visited": self.nodes_visited,
            "transitions_evaluated": self.transitions_evaluated,
            "decision_tables_evaluated": self.decision_tables_evaluated,
            "business_rules_evaluated": self.business_rules_evaluated,
            "variables_resolved": self.variables_resolved,
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "duration_ms": self.duration_ms,
        }
