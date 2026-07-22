"""BPM engine unit tests — Phase 1."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.bpm.domain.exceptions import (
    InvalidVersionState,
    PublishedVersionImmutable,
)
from modules.bpm.service.engines.workflow_category_engine import WorkflowCategoryEngine
from modules.bpm.service.engines.workflow_template_engine import WorkflowTemplateEngine
from modules.bpm.service.engines.workflow_version_engine import WorkflowVersionEngine


def test_category_activate_deactivate():
    row = SimpleNamespace(status="inactive")
    eng = WorkflowCategoryEngine()
    eng.activate(row)
    assert row.status == "active"
    eng.deactivate(row)
    assert row.status == "inactive"


def test_template_activate_retire():
    row = SimpleNamespace(status="draft")
    eng = WorkflowTemplateEngine()
    eng.activate(row)
    assert row.status == "active"
    eng.retire(row)
    assert row.status == "retired"


def test_version_publish_retire():
    row = SimpleNamespace(status="draft", published_at=None, published_by=None, retired_at=None, retired_by=None)
    eng = WorkflowVersionEngine()
    user_id = uuid4()
    eng.publish(row, user_id=user_id)
    assert row.status == "published"
    assert row.published_by == user_id
    eng.retire(row, user_id=user_id)
    assert row.status == "retired"


def test_published_immutable():
    row = SimpleNamespace(status="published")
    eng = WorkflowVersionEngine()
    with pytest.raises(PublishedVersionImmutable):
        eng.assert_editable(row)


def test_retired_readonly():
    row = SimpleNamespace(status="retired")
    eng = WorkflowVersionEngine()
    with pytest.raises(InvalidVersionState):
        eng.assert_editable(row)


def test_draft_editable():
    row = SimpleNamespace(status="draft")
    WorkflowVersionEngine().assert_editable(row)
