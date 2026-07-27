"""AI Platform Phase 4 module import / mount smoke tests."""

import inspect
from pathlib import Path


def test_phase4_models_export_34():
    from modules.ai import models

    assert len(models.__all__) == 34
    assert models.AiEvaluation is not None
    assert models.AiFeedback is not None
    assert models.AiMultimodalProfile is not None


def test_phase3_subset_still_present():
    from modules.ai import models

    phase3 = {"AiAgent", "AiTool", "AiSkill"}
    assert phase3.issubset(set(models.__all__))


def test_no_runtime_execution_on_phase4_services():
    from modules.ai.service.evaluation_service import EvaluationService
    from modules.ai.service.feedback_service import FeedbackService
    from modules.ai.service.multimodal_profile_service import MultimodalProfileService

    forbidden = {
        "invoke",
        "execute",
        "run",
        "orchestrate",
        "ocr",
        "speech",
        "vision",
        "transcribe",
        "synthesize",
    }
    for svc in (EvaluationService, FeedbackService, MultimodalProfileService):
        methods = {m for m in dir(svc) if not m.startswith("_")}
        assert methods.isdisjoint(forbidden), svc.__name__


def test_alembic_phase4_chain():
    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    expected = [
        "0555_ai_evaluation.py",
        "0556_ai_feedback.py",
        "0557_ai_multimodal_profile.py",
        "0558_seed_ai_phase4_permissions.py",
    ]
    for name in expected:
        assert (versions / name).exists(), name


def test_application_service_wires_phase4():
    from modules.ai.service.application_service import AiApplicationService

    src = inspect.getsource(AiApplicationService.__init__)
    for attr in ("evaluations", "feedbacks", "multimodal_profiles"):
        assert f"self.{attr}" in src


def test_phase4_tasks_registered():
    from modules.ai import tasks

    assert hasattr(tasks, "evaluation_stale_metadata_sweep")


def test_hardening_router_has_no_invoke_routes():
    from modules.ai.routers.hardening import (
        evaluations_router,
        feedbacks_router,
        multimodal_profiles_router,
    )

    for router in (evaluations_router, feedbacks_router, multimodal_profiles_router):
        for route in router.routes:
            path = getattr(route, "path", "")
            assert "/invoke" not in path
            assert "/execute" not in path
            assert "/ocr" not in path
            assert "/speech" not in path
            assert "/vision" not in path
