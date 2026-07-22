"""BPM Phase 4 integration import / route smoke tests."""


def test_import_phase4_models():
    from modules.bpm import models

    assert models.BpmWorkflowInstance is not None
    assert models.BpmWorkflowTask is not None
    assert models.BpmWorkflowHistory is not None
    assert models.BpmTaskDelegation is not None
    assert len(models.__all__) == 20


def test_import_phase4_services():
    from modules.bpm.service import (
        BpmApplicationService,
        TaskDelegationService,
        WorkflowHistoryService,
        WorkflowInstanceService,
        WorkflowTaskService,
    )

    assert WorkflowInstanceService is not None
    assert WorkflowTaskService is not None
    assert WorkflowHistoryService is not None
    assert TaskDelegationService is not None
    assert BpmApplicationService is not None


def test_router_includes_runtime_paths():
    from modules.bpm.router import bpm_router

    assert bpm_router.prefix == "/bpm"
    paths = [getattr(r, "path", "") or "" for r in bpm_router.routes]
    assert any("instances" in p for p in paths)
    assert any("tasks" in p for p in paths)
    assert any("history" in p for p in paths)
    assert any("delegations" in p for p in paths)


def test_application_service_has_runtime():
    import inspect

    from modules.bpm.service.application_service import BpmApplicationService

    src = inspect.getsource(BpmApplicationService.__init__)
    assert "WorkflowInstanceService" in src
    assert "WorkflowTaskService" in src
    assert "WorkflowHistoryService" in src
    assert "TaskDelegationService" in src


def test_simulation_present_after_phase5():
    from modules.bpm import models

    names = set(models.__all__)
    assert "BpmSimulationRun" in names
    assert len(names) == 20
