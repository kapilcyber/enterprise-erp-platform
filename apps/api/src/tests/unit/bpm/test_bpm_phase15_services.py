"""BPM Phase 1.5 unit tests — publish validation, compare, import, dashboard."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.bpm.domain.exceptions import PublishedVersionImmutable
from modules.bpm.domain.value_objects import (
    FieldDiff,
    PublishValidationResult,
    TemplateImportValidationResult,
    ValidationIssue,
    VersionComparisonResult,
)
from modules.bpm.service.engines.workflow_version_engine import WorkflowVersionEngine
from modules.bpm.service.template_import_export_service import TemplateImportExportService
from modules.bpm.service.version_comparison_service import _COMPARE_FIELDS


def test_publish_validation_result_structure():
    vid = uuid4()
    did = uuid4()
    result = PublishValidationResult(
        valid=False,
        version_id=vid,
        definition_id=did,
        issues=[ValidationIssue(code="VERSION_NOT_DRAFT", message="bad", field="status")],
        warnings=[ValidationIssue(code="OWNERSHIP_MISSING", message="warn", severity="warning")],
    )
    data = result.to_dict()
    assert data["valid"] is False
    assert data["issues"][0]["code"] == "VERSION_NOT_DRAFT"
    assert data["warnings"][0]["severity"] == "warning"


def test_version_comparison_result_structure():
    left = uuid4()
    right = uuid4()
    result = VersionComparisonResult(
        left_version_id=left,
        right_version_id=right,
        same_definition=True,
        differences=[FieldDiff(field="status", left="draft", right="published")],
    )
    data = result.to_dict()
    assert data["difference_count"] == 1
    assert data["same_definition"] is True
    assert "status" in _COMPARE_FIELDS


def test_template_import_validation_requires_name():
    svc = TemplateImportExportService.__new__(TemplateImportExportService)
    # bypass __init__ — call validate logic via private path using a stub scope

    class Stub:
        def resolve_company_id(self, ctx, company_id):
            return company_id or uuid4()

    svc._scope = Stub()
    svc._repo = None
    svc._categories = None
    ctx = SimpleNamespace()
    result = TemplateImportExportService.validate_import(
        svc, ctx, {"schema": "bpm.workflow_template.v1", "status": "draft"}
    )
    assert isinstance(result, TemplateImportValidationResult)
    assert result.valid is False
    assert any(i.code == "NAME_REQUIRED" for i in result.issues)


def test_template_import_validation_ok():
    svc = TemplateImportExportService.__new__(TemplateImportExportService)

    class Stub:
        def resolve_company_id(self, ctx, company_id):
            return uuid4()

    svc._scope = Stub()
    result = TemplateImportExportService.validate_import(
        svc,
        SimpleNamespace(),
        {
            "schema": "bpm.workflow_template.v1",
            "template_name": "PO Approval",
            "status": "draft",
            "module_code": "procurement",
        },
    )
    assert result.valid is True
    assert result.payload["template_name"] == "PO Approval"


def test_published_immutable_still_enforced():
    row = SimpleNamespace(status="published")
    with pytest.raises(PublishedVersionImmutable):
        WorkflowVersionEngine().assert_editable(row)


def test_dashboard_summary_dict_keys():
    from modules.bpm.domain.value_objects import BpmDashboardSummary

    s = BpmDashboardSummary(
        categories=1,
        templates=2,
        definitions=3,
        draft_versions=4,
        published_versions=5,
        retired_versions=6,
    )
    d = s.to_dict()
    assert set(d.keys()) == {
        "categories",
        "templates",
        "definitions",
        "draft",
        "published",
        "retired",
    }
