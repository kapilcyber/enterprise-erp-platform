"""AI Platform Phase 0 package smoke — updated for Phase 1 coexistence."""


def test_module_import():
    import modules.ai as ai_pkg
    from modules.ai import (
        adapters,
        dependencies,
        domain,
        models,
        permissions,
        repository,
        schemas,
        service,
        tasks,
    )
    from modules.ai.router import ai_router

    assert ai_pkg is not None
    assert ai_router.prefix == "/ai"
    assert domain is not None
    assert models is not None
    assert repository is not None
    assert service is not None
    assert adapters is not None
    assert schemas is not None
    assert permissions is not None
    assert dependencies is not None
    assert tasks is not None


def test_router_mount():
    from pathlib import Path

    from modules.ai.router import ai_router

    assert ai_router.prefix == "/ai"
    shared_router_path = Path(__file__).resolve().parents[3] / "shared" / "router.py"
    source = shared_router_path.read_text(encoding="utf-8")
    assert "from modules.ai.router import ai_router" in source
    assert "include_router(ai_router)" in source


def test_package_smoke():
    from modules.ai.adapters import AiFoundationAdapter
    from modules.ai.permissions import AI_PERMISSION_NAMESPACE
    from modules.ai.repository.base import AiScopedRepository
    from modules.ai.service import AiApplicationService, AiScopeValidator
    from modules.ai.tasks import module_health_ping

    assert AI_PERMISSION_NAMESPACE == "ai"
    assert AiApplicationService is not None
    assert AiScopeValidator is not None
    assert AiScopedRepository is not None
    assert AiFoundationAdapter is not None
    assert module_health_ping.name == "ai.module_health_ping"
    result = module_health_ping()
    assert result["status"] == "ok"
    assert result["module"] == "ai"
    assert result["phase"] in {0, 1}
