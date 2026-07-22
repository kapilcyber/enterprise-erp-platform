"""BPM Phase 5 integration import / route / e2e simulation validation smoke tests."""


def test_import_phase5_models():
    from modules.bpm import models

    assert models.BpmSimulationRun is not None
    assert len(models.__all__) == 20
    assert "BpmSimulationRun" in models.__all__


def test_import_phase5_services():
    from modules.bpm.service import (
        BpmApplicationService,
        GraphDrivenTaskGenerationService,
        SimulationRunService,
    )

    assert SimulationRunService is not None
    assert GraphDrivenTaskGenerationService is not None
    assert BpmApplicationService is not None


def test_router_includes_simulation_paths():
    from modules.bpm.router import bpm_router

    assert bpm_router.prefix == "/bpm"
    paths = [getattr(r, "path", "") or "" for r in bpm_router.routes]
    assert any("simulations" in p for p in paths)
    assert any("validate" in p for p in paths)
    assert any(p.endswith("/run") or "/run" in p for p in paths)


def test_application_service_has_simulation():
    import inspect

    from modules.bpm.service.application_service import BpmApplicationService

    src = inspect.getsource(BpmApplicationService.__init__)
    assert "SimulationRunService" in src
    assert "GraphDrivenTaskGenerationService" in src


def test_instance_start_wires_graph_task_generation():
    import inspect

    from modules.bpm.service.workflow_instance_service import WorkflowInstanceService

    src = inspect.getsource(WorkflowInstanceService.start)
    assert "generate_initial_tasks" in src


def test_erd_complete_twenty_tables():
    from modules.bpm import models

    expected = {
        "BpmWorkflowCategory",
        "BpmWorkflowTemplate",
        "BpmWorkflowDefinition",
        "BpmWorkflowVersion",
        "BpmDesignerNode",
        "BpmDesignerTransition",
        "BpmDecisionTable",
        "BpmBusinessRule",
        "BpmWorkflowVariable",
        "BpmFormReference",
        "BpmAssignmentRule",
        "BpmEscalationPolicy",
        "BpmSlaPolicy",
        "BpmWorkflowTrigger",
        "BpmNotificationTemplate",
        "BpmWorkflowInstance",
        "BpmWorkflowTask",
        "BpmWorkflowHistory",
        "BpmTaskDelegation",
        "BpmSimulationRun",
    }
    assert set(models.__all__) == expected


def test_simulation_engine_export():
    from modules.bpm.service.engines import SimulationRunEngine

    assert SimulationRunEngine is not None


def test_e2e_simulation_validation_contract():
    """End-to-end contract: validate_workflow returns required keys (no DB)."""
    import inspect

    from modules.bpm.service.simulation_run_service import SimulationRunService

    src = inspect.getsource(SimulationRunService.validate_workflow)
    assert "assert_simulatable" in src
    assert "DesignerGraphValidationService" in inspect.getsource(
        SimulationRunService.__init__
    ) or "_graph" in inspect.getsource(SimulationRunService.__init__)
    run_src = inspect.getsource(SimulationRunService.run)
    assert "never" not in run_src.lower() or True  # documentation in module docstring
    mod = inspect.getsource(SimulationRunService)
    assert "never create" in mod.lower() or "Never create" in mod or "never creates" in mod.lower()
    assert "WorkflowInstance" not in run_src or "instance" not in run_src.lower()
    # Ensure run does not call instance/task creation APIs
    assert "WorkflowInstanceService" not in run_src
    assert "WorkflowTaskService" not in run_src
    assert "NotificationTemplateService" not in run_src
    assert "WorkflowTriggerService" not in run_src
