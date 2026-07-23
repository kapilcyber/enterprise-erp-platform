"""Low-Code Phase 4 publish history / runtime submission / preview unit tests."""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.lowcode.domain.exceptions import (
    InvalidPreviewSessionState,
    InvalidPublishHistoryState,
    InvalidRuntimeSubmissionState,
)
from modules.lowcode.service.engines.preview_session_engine import PreviewSessionEngine
from modules.lowcode.service.engines.publish_history_engine import PublishHistoryEngine
from modules.lowcode.service.engines.runtime_submission_engine import (
    RuntimeSubmissionEngine,
)


def test_publish_history_actions_and_targets():
    eng = PublishHistoryEngine()
    eng.assert_valid_action("publish")
    eng.assert_valid_action("retire")
    with pytest.raises(InvalidPublishHistoryState):
        eng.assert_valid_action("approve")

    form_id = uuid4()
    targets = eng.normalize_targets(
        artifact_kind="form",
        form_definition_id=form_id,
        page_definition_id=None,
    )
    assert targets["form_definition_id"] == form_id
    assert targets["page_definition_id"] is None

    page_id = uuid4()
    targets = eng.normalize_targets(
        artifact_kind="page",
        form_definition_id=None,
        page_definition_id=page_id,
    )
    assert targets["page_definition_id"] == page_id

    with pytest.raises(InvalidPublishHistoryState):
        eng.normalize_targets(
            artifact_kind="form",
            form_definition_id=None,
            page_definition_id=None,
        )
    with pytest.raises(InvalidPublishHistoryState):
        eng.normalize_targets(
            artifact_kind="form",
            form_definition_id=form_id,
            page_definition_id=page_id,
        )


def test_runtime_submission_correlation_rules():
    eng = RuntimeSubmissionEngine()
    eng.assert_valid_status("received")
    eng.assert_valid_status("validated")
    eng.assert_valid_status("failed")
    eng.assert_valid_status("handoff")
    eng.assert_valid_status("cancelled")
    with pytest.raises(InvalidRuntimeSubmissionState):
        eng.assert_valid_status("posted")

    eng.assert_module_context("finance", uuid4())
    with pytest.raises(InvalidRuntimeSubmissionState):
        eng.assert_module_context("", uuid4())
    with pytest.raises(InvalidRuntimeSubmissionState):
        eng.assert_module_context("finance", None)

    eng.assert_correlation_id("corr-1")
    with pytest.raises(InvalidRuntimeSubmissionState):
        eng.assert_correlation_id("  ")

    eng.assert_version_target(form_version_id=uuid4(), page_version_id=None)
    with pytest.raises(InvalidRuntimeSubmissionState):
        eng.assert_version_target(form_version_id=None, page_version_id=None)


def test_preview_session_mode_and_lifecycle():
    eng = PreviewSessionEngine()
    eng.assert_valid_mode("draft")
    eng.assert_valid_mode("published")
    with pytest.raises(InvalidPreviewSessionState):
        eng.assert_valid_mode("live")

    eng.assert_mode_matches_version("draft", "draft")
    eng.assert_mode_matches_version("published", "published")
    with pytest.raises(InvalidPreviewSessionState):
        eng.assert_mode_matches_version("draft", "published")
    with pytest.raises(InvalidPreviewSessionState):
        eng.assert_mode_matches_version("published", "draft")

    with pytest.raises(InvalidPreviewSessionState):
        eng.assert_version_target(form_version_id=None, page_version_id=None)

    row = SimpleNamespace(
        status="active",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        closed_at=None,
    )
    eng.assert_active(row)
    eng.expire(row)
    assert row.status == "expired"
    eng.close(row)
    assert row.status == "closed"
    assert row.closed_at is not None
    with pytest.raises(InvalidPreviewSessionState):
        eng.close(row)
