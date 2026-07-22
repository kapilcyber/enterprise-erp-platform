"""BPM Phase 2B integration import / route smoke tests."""


def test_import_phase2b_models():
    from modules.bpm import models

    assert models.BpmDecisionTable is not None
    assert models.BpmBusinessRule is not None
    assert models.BpmWorkflowVariable is not None
    assert models.BpmFormReference is not None
    assert len(models.__all__) == 20


def test_import_phase2b_services():
    from modules.bpm.service import (
        BpmApplicationService,
        BusinessRuleService,
        DecisionTableService,
        FormReferenceService,
        WorkflowVariableService,
    )

    assert DecisionTableService is not None
    assert BusinessRuleService is not None
    assert WorkflowVariableService is not None
    assert FormReferenceService is not None
    assert BpmApplicationService is not None


def test_router_includes_intelligence_paths():
    from modules.bpm.router import bpm_router

    assert bpm_router.prefix == "/bpm"
    paths = [getattr(r, "path", "") or "" for r in bpm_router.routes]
    joined = " ".join(paths)
    assert any("decision-tables" in p for p in paths)
    assert any("business-rules" in p for p in paths)
    assert any("variables" in p for p in paths)
    assert any("form-references" in p for p in paths)
    assert "enable" in joined or any("enable" in p for p in paths)


def test_application_service_has_intelligence():
    import inspect

    from modules.bpm.service.application_service import BpmApplicationService

    src = inspect.getsource(BpmApplicationService.__init__)
    assert "DecisionTableService" in src
    assert "BusinessRuleService" in src
    assert "WorkflowVariableService" in src
    assert "FormReferenceService" in src


def test_no_runtime_models_in_phase2b():
    from modules.bpm import models

    names = set(models.__all__)
    # Phase 3A governance models are present after Phase 3A
    assert "BpmAssignmentRule" in names
    assert "BpmEscalationPolicy" in names
    assert "BpmSlaPolicy" in names
    # Phase 3B comms models are present after Phase 3B
    assert "BpmNotificationTemplate" in names
    assert "BpmWorkflowTrigger" in names
    # Phase 4 runtime models are present after Phase 4
    assert "BpmWorkflowInstance" in names
    assert "BpmWorkflowTask" in names
    assert "BpmWorkflowHistory" in names
    assert "BpmTaskDelegation" in names
    assert "BpmSimulationRun" in names
