"""BPM Phase 3A integration import / route smoke tests."""


def test_import_phase3a_models():
    from modules.bpm import models

    assert models.BpmAssignmentRule is not None
    assert models.BpmEscalationPolicy is not None
    assert models.BpmSlaPolicy is not None
    assert len(models.__all__) == 20


def test_import_phase3a_services():
    from modules.bpm.service import (
        AssignmentRuleService,
        BpmApplicationService,
        EscalationPolicyService,
        SlaPolicyService,
    )

    assert AssignmentRuleService is not None
    assert EscalationPolicyService is not None
    assert SlaPolicyService is not None
    assert BpmApplicationService is not None


def test_router_includes_governance_paths():
    from modules.bpm.router import bpm_router

    assert bpm_router.prefix == "/bpm"
    paths = [getattr(r, "path", "") or "" for r in bpm_router.routes]
    assert any("assignment-rules" in p for p in paths)
    assert any("escalation-policies" in p for p in paths)
    assert any("sla-policies" in p for p in paths)


def test_application_service_has_governance():
    import inspect

    from modules.bpm.service.application_service import BpmApplicationService

    src = inspect.getsource(BpmApplicationService.__init__)
    assert "AssignmentRuleService" in src
    assert "EscalationPolicyService" in src
    assert "SlaPolicyService" in src


def test_no_runtime_models_in_phase3a():
    from modules.bpm import models

    names = set(models.__all__)
    assert "BpmSimulationRun" in names
    # Phase 3B comms models are present after Phase 3B
    assert "BpmWorkflowTrigger" in names
    assert "BpmNotificationTemplate" in names
    # Phase 4 runtime models are present after Phase 4
    assert "BpmWorkflowInstance" in names
    assert "BpmWorkflowTask" in names
    assert "BpmWorkflowHistory" in names
    assert "BpmTaskDelegation" in names
