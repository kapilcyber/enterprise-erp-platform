"""AI Platform Phase 4 unit engine smoke tests."""

from types import SimpleNamespace

import pytest

from modules.ai.domain.enums import EvaluationStatus, FeedbackStatus, MultimodalProfileStatus
from modules.ai.domain.exceptions import (
    CompletedEvaluationImmutable,
    InvalidEvaluationState,
    InvalidFeedbackState,
    PublishedMultimodalProfileImmutable,
)
from modules.ai.service.engines import (
    EvaluationEngine,
    EvaluationQualityEngine,
    FeedbackEngine,
    MultimodalProfileEngine,
)


def test_evaluation_completed_immutable():
    engine = EvaluationEngine()
    row = SimpleNamespace(status=EvaluationStatus.COMPLETED.value)
    with pytest.raises(CompletedEvaluationImmutable):
        engine.assert_editable(row)


def test_evaluation_start_from_queued():
    engine = EvaluationEngine()
    row = SimpleNamespace(status=EvaluationStatus.QUEUED.value, started_at=None)
    engine.start(row)
    assert row.status == EvaluationStatus.RUNNING.value
    assert row.started_at is not None


def test_evaluation_complete_requires_running():
    engine = EvaluationEngine()
    row = SimpleNamespace(
        status=EvaluationStatus.QUEUED.value,
        completed_at=None,
        result_summary_json=None,
        metrics_json=None,
    )
    with pytest.raises(InvalidEvaluationState):
        engine.complete(row)


def test_evaluation_quality_stub():
    engine = EvaluationQualityEngine()
    result = engine.summarize_metadata(status=EvaluationStatus.COMPLETED.value, metrics_json="{}")
    assert result["quality_mode"] == "metadata_stub"
    assert result["valid"] is True


def test_feedback_review_from_captured():
    from uuid import uuid4

    engine = FeedbackEngine()
    row = SimpleNamespace(
        status=FeedbackStatus.CAPTURED.value,
        reviewed_at=None,
        reviewed_by=None,
    )
    uid = uuid4()
    engine.review(row, user_id=uid)
    assert row.status == FeedbackStatus.REVIEWED.value
    assert row.reviewed_by == uid


def test_feedback_close_from_reviewed():
    from uuid import uuid4

    engine = FeedbackEngine()
    row = SimpleNamespace(
        status=FeedbackStatus.REVIEWED.value,
        closed_at=None,
        closed_by=None,
    )
    uid = uuid4()
    engine.close(row, user_id=uid)
    assert row.status == FeedbackStatus.CLOSED.value


def test_feedback_closed_not_editable():
    engine = FeedbackEngine()
    row = SimpleNamespace(status=FeedbackStatus.CLOSED.value)
    with pytest.raises(InvalidFeedbackState):
        engine.assert_editable(row)


def test_multimodal_profile_published_immutable():
    engine = MultimodalProfileEngine()
    row = SimpleNamespace(status=MultimodalProfileStatus.PUBLISHED.value)
    with pytest.raises(PublishedMultimodalProfileImmutable):
        engine.assert_editable(row)
