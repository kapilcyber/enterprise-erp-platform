"""Low-Code Phase 2B component unit tests."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.lowcode.domain.exceptions import (
    InvalidComponentState,
    InvalidComponentVersionState,
    PublishedComponentVersionImmutable,
)
from modules.lowcode.service.engines.component_engine import ComponentEngine
from modules.lowcode.service.engines.component_version_engine import ComponentVersionEngine


def test_component_kind_validation():
    eng = ComponentEngine()
    eng.assert_valid_kind("text")
    eng.assert_valid_kind("grid")
    with pytest.raises(InvalidComponentState):
        eng.assert_valid_kind("not_a_kind")


def test_component_activate_retire():
    row = SimpleNamespace(status="draft")
    eng = ComponentEngine()
    eng.activate(row)
    assert row.status == "active"
    eng.retire(row)
    assert row.status == "retired"


def test_component_version_publish_retire():
    row = SimpleNamespace(
        status="draft",
        published_at=None,
        published_by=None,
        retired_at=None,
        retired_by=None,
    )
    eng = ComponentVersionEngine()
    user_id = uuid4()
    eng.publish(row, user_id=user_id)
    assert row.status == "published"
    eng.retire(row, user_id=user_id)
    assert row.status == "retired"


def test_published_component_version_immutable():
    with pytest.raises(PublishedComponentVersionImmutable):
        ComponentVersionEngine().assert_editable(SimpleNamespace(status="published"))


def test_retired_component_version_readonly():
    with pytest.raises(InvalidComponentVersionState):
        ComponentVersionEngine().assert_editable(SimpleNamespace(status="retired"))


def test_draft_component_version_editable():
    ComponentVersionEngine().assert_editable(SimpleNamespace(status="draft"))
