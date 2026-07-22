"""BPM module import smoke tests — Phase 1."""


def test_import_models():
    from modules.bpm import models

    assert models.BpmWorkflowCategory is not None
    assert models.BpmWorkflowTemplate is not None
    assert models.BpmWorkflowDefinition is not None
    assert models.BpmWorkflowVersion is not None
    assert len(models.__all__) == 20


def test_import_router():
    from modules.bpm.router import bpm_router

    assert bpm_router.prefix == "/bpm"


def test_import_services():
    from modules.bpm.service import BpmApplicationService, BpmIntegrationService, BpmNumberService

    assert BpmApplicationService is not None
    assert BpmIntegrationService is not None
    assert BpmNumberService is not None


def test_phase1_tables_only():
    from modules.bpm.models import __all__

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
    assert set(__all__) == expected
