"""AI Platform Phase 3 module import / mount / ownership smoke tests."""

import inspect
from pathlib import Path


def test_phase3_models_export_31():
    from modules.ai import models

    assert len(models.__all__) >= 31
    assert models.AiTool is not None
    assert models.AiToolVersion is not None
    assert models.AiSkill is not None
    assert models.AiAgent is not None
    assert models.AiAgentVersion is not None


def test_phase2_subset_still_present():
    from modules.ai import models

    phase2 = {
        "AiKnowledgeBase",
        "AiVectorIndex",
    }
    assert phase2.issubset(set(models.__all__))


def test_no_agent_runtime_methods_on_phase3_services():
    from modules.ai.service.agent_design_service import AgentDesignService
    from modules.ai.service.agent_service import AgentService
    from modules.ai.service.agent_version_service import AgentVersionService
    from modules.ai.service.tool_registry_service import ToolRegistryService

    forbidden = {
        "invoke",
        "execute",
        "run",
        "orchestrate",
        "call_tool",
        "reason",
        "autonomous_run",
    }
    for svc in (
        AgentService,
        AgentVersionService,
        ToolRegistryService,
        AgentDesignService,
    ):
        methods = {m for m in dir(svc) if not m.startswith("_")}
        assert methods.isdisjoint(forbidden), svc.__name__


def test_bpm_and_business_module_ports_exist():
    from uuid import uuid4

    from modules.ai.adapters import AiBpmAdapter, AiBusinessModuleAdapter

    bpm = AiBpmAdapter(db=None)  # type: ignore[arg-type]
    mod = AiBusinessModuleAdapter(db=None)  # type: ignore[arg-type]
    ref = uuid4()
    assert bpm.resolve_bpm_definition_ref(None, ref) == ref  # type: ignore[arg-type]
    assert mod.resolve_contract_key(None, "sales.order.create") == "sales.order.create"  # type: ignore[arg-type]


def test_alembic_phase3_chain():
    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    expected = [
        "0549_ai_tool.py",
        "0550_ai_tool_version.py",
        "0551_ai_skill.py",
        "0552_ai_agent.py",
        "0553_ai_agent_version.py",
        "0554_seed_ai_phase3_permissions.py",
    ]
    for name in expected:
        assert (versions / name).exists(), name


def test_application_service_wires_phase3():
    from modules.ai.service.application_service import AiApplicationService

    src = inspect.getsource(AiApplicationService.__init__)
    for attr in (
        "tools",
        "tool_versions",
        "skills",
        "agents",
        "agent_versions",
        "tool_registry",
        "agent_design",
    ):
        assert f"self.{attr}" in src


def test_phase3_tasks_registered():
    from modules.ai import tasks

    assert hasattr(tasks, "published_tool_version_guard")
    assert hasattr(tasks, "published_agent_version_guard")


def test_agents_router_has_no_invoke_routes():
    from modules.ai.routers.agents import agent_versions_router, agents_router

    for router in (agents_router, agent_versions_router):
        for route in router.routes:
            path = getattr(route, "path", "")
            assert "/invoke" not in path
            assert "/execute" not in path
