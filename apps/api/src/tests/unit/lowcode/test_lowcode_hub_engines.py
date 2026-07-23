"""Low-Code engine unit tests — Phase 1."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.lowcode.domain.exceptions import (
    InvalidVersionState,
    PublishedVersionImmutable,
)
from modules.lowcode.service.engines.form_category_engine import FormCategoryEngine
from modules.lowcode.service.engines.form_definition_engine import FormDefinitionEngine
from modules.lowcode.service.engines.form_version_engine import FormVersionEngine


def test_category_activate_deactivate():
    row = SimpleNamespace(status="inactive")
    eng = FormCategoryEngine()
    eng.activate(row)
    assert row.status == "active"
    eng.deactivate(row)
    assert row.status == "inactive"


def test_definition_activate_retire():
    row = SimpleNamespace(status="draft")
    eng = FormDefinitionEngine()
    eng.activate(row)
    assert row.status == "active"
    eng.retire(row)
    assert row.status == "retired"


def test_version_publish_retire():
    row = SimpleNamespace(
        status="draft",
        published_at=None,
        published_by=None,
        retired_at=None,
        retired_by=None,
    )
    eng = FormVersionEngine()
    user_id = uuid4()
    eng.publish(row, user_id=user_id)
    assert row.status == "published"
    assert row.published_by == user_id
    eng.retire(row, user_id=user_id)
    assert row.status == "retired"


def test_published_immutable():
    row = SimpleNamespace(status="published")
    eng = FormVersionEngine()
    with pytest.raises(PublishedVersionImmutable):
        eng.assert_editable(row)


def test_retired_readonly():
    row = SimpleNamespace(status="retired")
    eng = FormVersionEngine()
    with pytest.raises(InvalidVersionState):
        eng.assert_editable(row)


def test_draft_editable():
    row = SimpleNamespace(status="draft")
    FormVersionEngine().assert_editable(row)
