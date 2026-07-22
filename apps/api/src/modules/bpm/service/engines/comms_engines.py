"""Workflow trigger / notification template engines — Phase 3B."""

import json

from modules.bpm.domain.enums import (
    NOTIFICATION_TEMPLATE_TYPE_VALUES,
    TRIGGER_TYPE_VALUES,
    NotificationTemplateStatus,
    TriggerStatus,
    TriggerType,
)
from modules.bpm.domain.exceptions import (
    InvalidNotificationTemplateState,
    InvalidWorkflowTriggerState,
)


class WorkflowTriggerEngine:
    def assert_valid_type(self, trigger_type: str | None) -> None:
        if not trigger_type or trigger_type not in TRIGGER_TYPE_VALUES:
            raise InvalidWorkflowTriggerState(f"Unsupported trigger type: {trigger_type}")

    def enable(self, row) -> None:
        if row.status == TriggerStatus.ENABLED.value:
            raise InvalidWorkflowTriggerState("Trigger already enabled")
        row.status = TriggerStatus.ENABLED.value

    def disable(self, row) -> None:
        if row.status != TriggerStatus.ENABLED.value:
            raise InvalidWorkflowTriggerState("Only enabled triggers can be disabled")
        row.status = TriggerStatus.DISABLED.value

    def assert_type_payload(
        self,
        trigger_type: str | None,
        *,
        event_name: str | None = None,
        execution_mode_metadata_json: str | None = None,
    ) -> None:
        if not trigger_type:
            raise InvalidWorkflowTriggerState("trigger_type is required")
        if trigger_type == TriggerType.EVENT.value and (
            not event_name or not str(event_name).strip()
        ):
            raise InvalidWorkflowTriggerState("event_name is required for event triggers")
        if trigger_type in (
            TriggerType.SCHEDULE.value,
            TriggerType.WEBHOOK.value,
            TriggerType.MESSAGE_QUEUE.value,
            TriggerType.API.value,
        ):
            if not execution_mode_metadata_json:
                raise InvalidWorkflowTriggerState(
                    f"execution_mode_metadata_json is required for {trigger_type} triggers"
                )
            self.assert_metadata_json(execution_mode_metadata_json)

    def assert_metadata_json(self, metadata_json: str | None) -> None:
        if metadata_json is None:
            return
        try:
            data = json.loads(metadata_json)
        except json.JSONDecodeError as exc:
            raise InvalidWorkflowTriggerState(
                f"Invalid execution_mode_metadata_json: {exc}"
            ) from exc
        if not isinstance(data, dict):
            raise InvalidWorkflowTriggerState(
                "execution_mode_metadata_json must be a JSON object"
            )


class NotificationTemplateEngine:
    def assert_valid_type(self, template_type: str | None) -> None:
        if not template_type or template_type not in NOTIFICATION_TEMPLATE_TYPE_VALUES:
            raise InvalidNotificationTemplateState(
                f"Unsupported template type: {template_type}"
            )

    def enable(self, row) -> None:
        if row.status == NotificationTemplateStatus.ENABLED.value:
            raise InvalidNotificationTemplateState("Notification template already enabled")
        row.status = NotificationTemplateStatus.ENABLED.value

    def disable(self, row) -> None:
        if row.status != NotificationTemplateStatus.ENABLED.value:
            raise InvalidNotificationTemplateState(
                "Only enabled notification templates can be disabled"
            )
        row.status = NotificationTemplateStatus.DISABLED.value

    def assert_content(
        self, template_type: str | None, *, subject: str | None, body: str | None
    ) -> None:
        if not template_type:
            raise InvalidNotificationTemplateState("template_type is required")
        if template_type == "email" and (not subject or not str(subject).strip()):
            raise InvalidNotificationTemplateState("subject is required for email templates")
        if not body or not str(body).strip():
            raise InvalidNotificationTemplateState("body is required")

    def assert_json_field(self, field: str, value: str | None) -> None:
        if value is None:
            return
        try:
            data = json.loads(value)
        except json.JSONDecodeError as exc:
            raise InvalidNotificationTemplateState(f"Invalid {field}: {exc}") from exc
        if not isinstance(data, (dict, list)):
            raise InvalidNotificationTemplateState(f"{field} must be a JSON object or array")
