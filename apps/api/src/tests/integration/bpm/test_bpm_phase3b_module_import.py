"""BPM Phase 3B integration import / route smoke tests."""


def test_import_phase3b_models():
    from modules.bpm import models

    assert models.BpmWorkflowTrigger is not None
    assert models.BpmNotificationTemplate is not None
    assert len(models.__all__) == 20


def test_import_phase3b_services():
    from modules.bpm.service import (
        BpmApplicationService,
        NotificationTemplateService,
        WorkflowTriggerService,
    )

    assert WorkflowTriggerService is not None
    assert NotificationTemplateService is not None
    assert BpmApplicationService is not None


def test_router_includes_comms_paths():
    from modules.bpm.router import bpm_router

    assert bpm_router.prefix == "/bpm"
    paths = [getattr(r, "path", "") or "" for r in bpm_router.routes]
    joined = " ".join(paths)
    assert any("triggers" in p for p in paths)
    assert any("notification-templates" in p for p in paths)
    assert "enable" in joined


def test_application_service_has_comms():
    import inspect

    from modules.bpm.service.application_service import BpmApplicationService

    src = inspect.getsource(BpmApplicationService.__init__)
    assert "WorkflowTriggerService" in src
    assert "NotificationTemplateService" in src


def test_no_runtime_or_simulation_in_phase3b():
    from modules.bpm import models

    names = set(models.__all__)
    assert "BpmSimulationRun" in names
    # Phase 4 runtime models are present after Phase 4
    assert "BpmWorkflowInstance" in names
    assert "BpmWorkflowTask" in names
    assert "BpmWorkflowHistory" in names
    assert "BpmTaskDelegation" in names
