"""BPM Phase 3B unit tests — trigger and notification engines."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.bpm.domain.enums import (
    NOTIFICATION_TEMPLATE_TYPE_VALUES,
    TRIGGER_TYPE_VALUES,
)
from modules.bpm.domain.exceptions import (
    InvalidNotificationTemplateState,
    InvalidWorkflowTriggerState,
)
from modules.bpm.domain.value_objects import NotificationContentSpec, TriggerBindingSpec
from modules.bpm.service.engines import NotificationTemplateEngine, WorkflowTriggerEngine


def test_trigger_types_supported():
    eng = WorkflowTriggerEngine()
    expected = {"manual", "event", "api", "schedule", "webhook", "message_queue"}
    assert set(TRIGGER_TYPE_VALUES) == expected
    for t in TRIGGER_TYPE_VALUES:
        eng.assert_valid_type(t)
    with pytest.raises(InvalidWorkflowTriggerState):
        eng.assert_valid_type("cron")


def test_trigger_enable_disable():
    eng = WorkflowTriggerEngine()
    row = SimpleNamespace(status="disabled")
    eng.enable(row)
    assert row.status == "enabled"
    eng.disable(row)
    assert row.status == "disabled"
    with pytest.raises(InvalidWorkflowTriggerState):
        eng.disable(row)


def test_trigger_type_payload_rules():
    eng = WorkflowTriggerEngine()
    eng.assert_type_payload("manual")
    eng.assert_type_payload("event", event_name="invoice.approved")
    with pytest.raises(InvalidWorkflowTriggerState):
        eng.assert_type_payload("event", event_name="")
    eng.assert_type_payload("api", execution_mode_metadata_json='{"method":"POST"}')
    with pytest.raises(InvalidWorkflowTriggerState):
        eng.assert_type_payload("schedule", execution_mode_metadata_json=None)
    with pytest.raises(InvalidWorkflowTriggerState):
        eng.assert_type_payload("webhook", execution_mode_metadata_json="[]")


def test_notification_template_types():
    eng = NotificationTemplateEngine()
    expected = {"email", "sms", "push", "in_app"}
    assert set(NOTIFICATION_TEMPLATE_TYPE_VALUES) == expected
    for t in NOTIFICATION_TEMPLATE_TYPE_VALUES:
        eng.assert_valid_type(t)
    with pytest.raises(InvalidNotificationTemplateState):
        eng.assert_valid_type("fax")


def test_notification_content_and_enable():
    eng = NotificationTemplateEngine()
    eng.assert_content("email", subject="Hello", body="World")
    with pytest.raises(InvalidNotificationTemplateState):
        eng.assert_content("email", subject="", body="World")
    with pytest.raises(InvalidNotificationTemplateState):
        eng.assert_content("sms", subject=None, body="")
    eng.assert_json_field("variables_json", '["name","amount"]')
    eng.assert_json_field("localization_json", '{"en":{}}')
    with pytest.raises(InvalidNotificationTemplateState):
        eng.assert_json_field("variables_json", "not-json")
    row = SimpleNamespace(status="disabled")
    eng.enable(row)
    assert row.status == "enabled"
    eng.disable(row)
    assert row.status == "disabled"


def test_comms_value_objects():
    trig = TriggerBindingSpec(
        definition_id=uuid4(),
        version_id=None,
        trigger_type="manual",
        module_code="finance",
    )
    assert trig.version_id is None
    ntf = NotificationContentSpec(template_type="email", subject="S", body="B")
    assert ntf.template_type == "email"
