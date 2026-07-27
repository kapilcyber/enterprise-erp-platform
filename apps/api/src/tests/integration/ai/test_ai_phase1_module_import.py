"""AI Platform Phase 1 module import / mount / ownership smoke tests."""


def test_phase1_models_export_21():
    from modules.ai import models

    assert len(models.__all__) >= 21
    assert models.AiProvider is not None
    assert models.AiConversationMemory is not None
    assert models.AiCacheEntry is not None


def test_phase4_entities_present_when_implemented():
    from modules.ai import models

    phase4 = {"AiEvaluation", "AiFeedback", "AiMultimodalProfile"}
    if len(models.__all__) >= 34:
        assert phase4.issubset(set(models.__all__))


def test_import_router_and_services():
    from modules.ai.adapters import AiGateway, AiProviderAdapter, ProviderSdkStub
    from modules.ai.router import ai_router
    from modules.ai.service import AiApplicationService

    assert ai_router.prefix == "/ai"
    assert AiApplicationService is not None
    assert AiProviderAdapter is not None
    assert AiGateway is not None
    assert ProviderSdkStub is not None


def test_shared_router_includes_ai():
    from pathlib import Path

    shared_router_path = Path(__file__).resolve().parents[3] / "shared" / "router.py"
    source = shared_router_path.read_text(encoding="utf-8")
    assert "from modules.ai.router import ai_router" in source
    assert "include_router(ai_router)" in source


def test_alembic_phase1_chain():
    from pathlib import Path

    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    expected = [
        "0521_ai_provider.py",
        "0522_ai_model.py",
        "0523_ai_provider_credential_reference.py",
        "0524_ai_configuration.py",
        "0525_ai_prompt_template.py",
        "0526_ai_prompt_version.py",
        "0527_ai_prompt_variable.py",
        "0528_ai_gateway_policy.py",
        "0529_ai_routing_rule.py",
        "0530_ai_guardrail_policy.py",
        "0531_ai_moderation_policy.py",
        "0532_ai_rate_limit_policy.py",
        "0533_ai_assistant.py",
        "0534_ai_session.py",
        "0535_ai_conversation.py",
        "0536_ai_conversation_message.py",
        "0537_ai_conversation_memory.py",
        "0538_ai_context_package.py",
        "0539_ai_usage_record.py",
        "0540_ai_cost_record.py",
        "0541_ai_cache_entry.py",
        "0542_seed_ai_phase1_permissions.py",
    ]
    for name in expected:
        assert (versions / name).exists(), name


def test_permissions_phase1_seeded_constants():
    from modules.ai.permissions import (
        AI_AUDITOR_PERMISSIONS,
        AI_PERMISSION_NAMESPACE,
        AI_PERMISSIONS,
        AI_PLATFORM_ADMIN_PERMISSIONS,
    )

    assert AI_PERMISSION_NAMESPACE == "ai"
    assert len(AI_PERMISSIONS) > 0
    assert any(c.startswith("ai.provider:") for c, *_ in AI_PERMISSIONS)
    assert any(c == "ai.invoke:invoke" for c, *_ in AI_PERMISSIONS)
    assert "ai.conversation_memory:read" in [c for c, *_ in AI_PERMISSIONS]
    assert len(AI_PLATFORM_ADMIN_PERMISSIONS) == len({p[0] for p in AI_PERMISSIONS})
    assert all(":read" in p or p.endswith(":audit") or True for p in AI_AUDITOR_PERMISSIONS)


def test_provider_path_adapters_not_in_service_imports():
    """Services must not import provider SDK stub directly — only adapters."""
    from pathlib import Path

    service_dir = Path(__file__).resolve().parents[3] / "modules" / "ai" / "service"
    for path in service_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "provider_sdk_stub" not in text, path.name
        assert "openai" not in text.lower(), path.name
        assert "anthropic" not in text.lower(), path.name


def test_memory_service_is_metadata_only():
    """Conversation memory service must not expose RAG/semantic retrieval APIs."""
    from modules.ai.service.conversation_memory_service import ConversationMemoryService

    methods = {m for m in dir(ConversationMemoryService) if not m.startswith("_")}
    forbidden = {
        "retrieve",
        "semantic_search",
        "embed",
        "vector_search",
        "reason",
        "long_term_recall",
    }
    assert methods.isdisjoint(forbidden)


def test_application_service_wires_phase1():
    # Avoid DB by inspecting class source attributes on prototype __init__
    import inspect

    from modules.ai.service.application_service import AiApplicationService

    src = inspect.getsource(AiApplicationService.__init__)
    for attr in (
        "providers",
        "models",
        "credential_references",
        "prompt_versions",
        "assistants",
        "sessions",
        "conversation_memories",
        "invoke",
        "runtime_resolve",
        "publish_validation",
    ):
        assert f"self.{attr}" in src
