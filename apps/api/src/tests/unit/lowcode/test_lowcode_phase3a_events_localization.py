"""Low-Code Phase 3A event handler / localization unit tests."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.lowcode.domain.exceptions import (
    InvalidEventHandlerState,
    InvalidLocalizationEntryState,
    PublishedLocalizationImmutable,
)
from modules.lowcode.service.engines.event_handler_engine import EventHandlerEngine
from modules.lowcode.service.engines.localization_entry_engine import (
    LocalizationEntryEngine,
)


def test_event_types_supported():
    eng = EventHandlerEngine()
    for t in (
        "onLoad",
        "onChange",
        "onFocus",
        "onBlur",
        "onValidate",
        "onSubmit",
        "onCancel",
        "custom",
    ):
        eng.assert_valid_event_type(t)
    with pytest.raises(InvalidEventHandlerState):
        eng.assert_valid_event_type("onWorkflowRoute")


def test_custom_event_name_rules():
    eng = EventHandlerEngine()
    eng.assert_custom_name("custom", "myEvent")
    with pytest.raises(InvalidEventHandlerState):
        eng.assert_custom_name("custom", None)
    with pytest.raises(InvalidEventHandlerState):
        eng.assert_custom_name("onLoad", "x")


def test_event_handler_target_normalization():
    eng = EventHandlerEngine()
    fv = uuid4()
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
        target_type="field",
        form_version_id=fv,
        section_id=None,
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
    with pytest.raises(InvalidEventHandlerState):
        eng.normalize_targets(
            target_type="form_version",
            form_version_id=fv,
            section_id=uuid4(),
            field_id=None,
            page_version_id=None,
        )


def test_localization_owner_and_lifecycle():
    eng = LocalizationEntryEngine()
    eng.assert_valid_owner_type("form")
    eng.assert_valid_owner_type("field")
    eng.assert_valid_owner_type("section")
    eng.assert_valid_owner_type("component")
    eng.assert_valid_owner_type("page")
    with pytest.raises(InvalidLocalizationEntryState):
        eng.assert_valid_owner_type("workflow")

    fv = uuid4()
    owner_ref, cols = eng.resolve_owner_refs(
        owner_type="form",
        form_version_id=fv,
        section_id=None,
        field_id=None,
        component_id=None,
        page_version_id=None,
    )
    assert owner_ref == fv
    assert cols["form_version_id"] == fv

    row = SimpleNamespace(
        status="draft",
        published_at=None,
        published_by=None,
        retired_at=None,
        retired_by=None,
    )
    eng.assert_editable(row)
    user_id = uuid4()
    eng.publish(row, user_id=user_id)
    assert row.status == "published"
    with pytest.raises(PublishedLocalizationImmutable):
        eng.assert_editable(row)
    eng.retire(row, user_id=user_id)
    assert row.status == "retired"
    with pytest.raises(InvalidLocalizationEntryState):
        eng.assert_editable(row)
