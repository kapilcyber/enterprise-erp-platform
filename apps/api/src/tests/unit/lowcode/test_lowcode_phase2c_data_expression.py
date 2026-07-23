"""Low-Code Phase 2C data source / expression unit tests."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.lowcode.domain.exceptions import (
    InvalidDataSourceState,
    InvalidExpressionBindingState,
    InvalidExpressionState,
    PublishedExpressionImmutable,
)
from modules.lowcode.service.engines.data_source_engine import DataSourceEngine
from modules.lowcode.service.engines.expression_binding_engine import (
    ExpressionBindingEngine,
)
from modules.lowcode.service.engines.expression_engine import ExpressionEngine


def test_data_source_operations_validation():
    eng = DataSourceEngine()
    eng.assert_allowed_operations("read,lookup")
    eng.assert_allowed_operations("read, write, lookup")
    with pytest.raises(InvalidDataSourceState):
        eng.assert_allowed_operations("execute")
    with pytest.raises(InvalidDataSourceState):
        eng.assert_module_contract("", "Party")


def test_data_source_activate_retire():
    row = SimpleNamespace(status="draft")
    eng = DataSourceEngine()
    eng.activate(row)
    assert row.status == "active"
    eng.retire(row)
    assert row.status == "retired"
    with pytest.raises(InvalidDataSourceState):
        eng.assert_editable(row)


def test_expression_kind_validation():
    eng = ExpressionEngine()
    for kind in (
        "visibility",
        "required",
        "enable",
        "disable",
        "default",
        "calculate",
    ):
        eng.assert_valid_kind(kind)
    with pytest.raises(InvalidExpressionState):
        eng.assert_valid_kind("workflow_route")


def test_expression_publish_retire_immutable():
    row = SimpleNamespace(
        status="draft",
        expression_kind="visibility",
        expression_body="amount > 0",
        published_at=None,
        published_by=None,
        retired_at=None,
        retired_by=None,
    )
    eng = ExpressionEngine()
    user_id = uuid4()
    eng.publish(row, user_id=user_id)
    assert row.status == "published"
    with pytest.raises(PublishedExpressionImmutable):
        eng.assert_editable(row)
    eng.retire(row, user_id=user_id)
    assert row.status == "retired"
    with pytest.raises(InvalidExpressionState):
        eng.assert_editable(row)


def test_expression_binding_target_normalization():
    eng = ExpressionBindingEngine()
    fv = uuid4()
    sec = uuid4()
    fld = uuid4()
    page = uuid4()

    assert eng.normalize_targets(
        target_type="form_version",
        form_version_id=fv,
        section_id=None,
        field_id=None,
        page_version_id=None,
    )["form_version_id"] == fv

    assert eng.normalize_targets(
        target_type="section",
        form_version_id=fv,
        section_id=sec,
        field_id=None,
        page_version_id=None,
    )["section_id"] == sec

    assert eng.normalize_targets(
        target_type="field",
        form_version_id=fv,
        section_id=sec,
        field_id=fld,
        page_version_id=None,
    )["field_id"] == fld

    assert eng.normalize_targets(
        target_type="page_version",
        form_version_id=None,
        section_id=None,
        field_id=None,
        page_version_id=page,
    )["page_version_id"] == page

    with pytest.raises(InvalidExpressionBindingState):
        eng.normalize_targets(
            target_type="form_version",
            form_version_id=fv,
            section_id=sec,
            field_id=None,
            page_version_id=None,
        )

    with pytest.raises(InvalidExpressionBindingState):
        eng.assert_valid_target_type("business_rule")
