"""Low-Code Phase 3B page definition / version / region unit tests."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.lowcode.domain.exceptions import (
    InvalidPageDefinitionState,
    InvalidPageRegionState,
    InvalidPageVersionState,
    PublishedPageVersionImmutable,
)
from modules.lowcode.service.engines.page_definition_engine import PageDefinitionEngine
from modules.lowcode.service.engines.page_region_engine import PageRegionEngine
from modules.lowcode.service.engines.page_version_engine import PageVersionEngine


def test_page_definition_activate_retire():
    row = SimpleNamespace(status="draft")
    eng = PageDefinitionEngine()
    eng.activate(row)
    assert row.status == "active"
    eng.retire(row)
    assert row.status == "retired"
    with pytest.raises(InvalidPageDefinitionState):
        eng.activate(row)


def test_page_version_publish_retire_immutable():
    row = SimpleNamespace(
        status="draft",
        published_at=None,
        published_by=None,
        retired_at=None,
        retired_by=None,
    )
    eng = PageVersionEngine()
    user_id = uuid4()
    eng.publish(row, user_id=user_id)
    assert row.status == "published"
    with pytest.raises(PublishedPageVersionImmutable):
        eng.assert_editable(row)
    eng.retire(row, user_id=user_id)
    assert row.status == "retired"
    with pytest.raises(InvalidPageVersionState):
        eng.assert_editable(row)


def test_page_region_types():
    eng = PageRegionEngine()
    for t in (
        "header",
        "content",
        "sidebar",
        "footer",
        "modal",
        "tab",
        "wizard_step",
        "custom",
    ):
        eng.assert_valid_type(t)
    with pytest.raises(InvalidPageRegionState):
        eng.assert_valid_type("canvas")
    eng.assert_display_order(0)
    with pytest.raises(InvalidPageRegionState):
        eng.assert_display_order(-1)
