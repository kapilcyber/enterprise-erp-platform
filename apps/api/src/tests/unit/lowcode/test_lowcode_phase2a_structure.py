"""Low-Code Phase 2A form structure unit tests."""

from types import SimpleNamespace

import pytest

from modules.lowcode.domain.exceptions import (
    DuplicateFieldKeyForbidden,
    InvalidFieldState,
    InvalidSectionState,
    PublishedVersionImmutable,
)
from modules.lowcode.service.engines.form_field_engine import FormFieldEngine
from modules.lowcode.service.engines.form_section_engine import FormSectionEngine
from modules.lowcode.service.engines.form_version_engine import FormVersionEngine


def test_section_display_order_rejects_negative():
    with pytest.raises(InvalidSectionState):
        FormSectionEngine().assert_display_order(-1)


def test_section_display_order_ok():
    FormSectionEngine().assert_display_order(0)
    FormSectionEngine().assert_display_order(10)


def test_field_type_validation():
    eng = FormFieldEngine()
    eng.assert_valid_type("text")
    with pytest.raises(InvalidFieldState):
        eng.assert_valid_type("not_a_type")


def test_field_key_validation():
    eng = FormFieldEngine()
    eng.assert_field_key("customer_name")
    with pytest.raises(InvalidFieldState):
        eng.assert_field_key("CustomerName")
    with pytest.raises(InvalidFieldState):
        eng.assert_field_key("1bad")


def test_field_display_order_rejects_negative():
    with pytest.raises(InvalidFieldState):
        FormFieldEngine().assert_display_order(-5)


def test_draft_version_editable_for_structure():
    FormVersionEngine().assert_editable(SimpleNamespace(status="draft"))


def test_published_version_blocks_structure_edits():
    with pytest.raises(PublishedVersionImmutable):
        FormVersionEngine().assert_editable(SimpleNamespace(status="published"))


def test_duplicate_field_key_exception_message():
    exc = DuplicateFieldKeyForbidden()
    assert "unique" in str(exc).lower() or "Field key" in str(exc)
