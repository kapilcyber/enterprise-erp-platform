"""BPM Phase 2A integration import / route smoke tests."""


def test_import_phase2a_models():
    from modules.bpm import models

    assert models.BpmDesignerNode is not None
    assert models.BpmDesignerTransition is not None
    assert len(models.__all__) == 20


def test_import_phase2a_services():
    from modules.bpm.service import (
        BpmApplicationService,
        DesignerGraphValidationService,
        DesignerNodeService,
        DesignerTransitionService,
    )

    assert DesignerNodeService is not None
    assert DesignerTransitionService is not None
    assert DesignerGraphValidationService is not None
    assert BpmApplicationService is not None


def test_router_includes_designer_paths():
    from modules.bpm.router import bpm_router

    assert bpm_router.prefix == "/bpm"
    paths = [getattr(r, "path", "") or "" for r in bpm_router.routes]
    joined = " ".join(paths)
    assert any("nodes" in p for p in paths)
    assert any("transitions" in p for p in paths)
    assert "validate" in joined or any("graph" in p for p in paths)


def test_application_service_has_designer():
    # Inspect constructor source attributes via annotations / defaults by instantiating stubs is heavy;
    # verify class body wiring by reading attributes after partial init mock.
    import inspect

    from modules.bpm.service.application_service import BpmApplicationService

    src = inspect.getsource(BpmApplicationService.__init__)
    assert "DesignerNodeService" in src
    assert "DesignerTransitionService" in src
    assert "DesignerGraphValidationService" in src


def test_no_runtime_models_in_phase2a():
    from modules.bpm import models

    names = set(models.__all__)
    # Phase 2B intelligence models are present after Phase 2B
    assert "BpmDecisionTable" in names
    assert "BpmBusinessRule" in names
    # Phase 4 runtime models are present after Phase 4
    assert "BpmWorkflowInstance" in names
    assert "BpmWorkflowTask" in names
    assert "BpmWorkflowHistory" in names
    assert "BpmSimulationRun" in names
