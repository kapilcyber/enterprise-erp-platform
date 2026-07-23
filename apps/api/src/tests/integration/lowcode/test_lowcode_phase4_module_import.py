"""Low-Code Phase 4 module import smoke tests."""


def test_phase4_models_exported():
    from modules.lowcode import models

    assert models.LcPublishHistory is not None
    assert models.LcRuntimeSubmission is not None
    assert models.LcPreviewSession is not None
    assert len(models.__all__) == 18


def test_phase4_services_exported():
    from modules.lowcode.service import (
        PreviewSessionService,
        PublishHistoryService,
        RuntimeSubmissionService,
    )

    assert PublishHistoryService is not None
    assert RuntimeSubmissionService is not None
    assert PreviewSessionService is not None


def test_phase4_routers_mounted():
    from modules.lowcode.router import lowcode_router

    paths = [getattr(r, "path", "") for r in lowcode_router.routes]
    assert any("publish-history" in p for p in paths)
    assert any("runtime-submissions" in p for p in paths)
    assert any("preview-sessions" in p for p in paths)


def test_application_service_wires_phase4():
    from unittest.mock import MagicMock

    from modules.lowcode.service.application_service import LowcodeApplicationService

    app = LowcodeApplicationService(MagicMock())
    assert app.publish_history is not None
    assert app.runtime_submissions is not None
    assert app.preview_sessions is not None


def test_phase4_migrations_chain():
    from pathlib import Path

    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    assert (versions / "0516_lc_publish_history.py").exists()
    assert (versions / "0517_lc_runtime_submission.py").exists()
    assert (versions / "0518_lc_preview_session.py").exists()
    assert (versions / "0519_seed_lowcode_phase4_permissions.py").exists()
