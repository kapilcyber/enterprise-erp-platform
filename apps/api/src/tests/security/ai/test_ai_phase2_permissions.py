"""AI Platform Phase 2 permission constant security smoke tests."""

from modules.ai.permissions import (
    AI_KNOWLEDGE_CURATOR_PERMISSIONS,
    AI_PERMISSIONS,
    AI_PHASE2_PERMISSIONS,
    AI_PLATFORM_ADMIN_PERMISSIONS,
    AI_PUBLISHER_PERMISSIONS,
)


def test_phase2_permission_namespace():
    for code, resource, _action, module in AI_PHASE2_PERMISSIONS:
        assert code.startswith("ai.")
        assert resource.startswith("ai.")
        assert module == "ai"
        assert any(
            resource.startswith(f"ai.{r}")
            for r in (
                "knowledge_base",
                "knowledge_source",
                "knowledge_chunk",
                "embedding",
                "vector_index",
            )
        )


def test_curator_has_knowledge_and_model_read():
    assert any("knowledge_base:" in p for p in AI_KNOWLEDGE_CURATOR_PERMISSIONS)
    assert any("knowledge_source:" in p for p in AI_KNOWLEDGE_CURATOR_PERMISSIONS)
    assert "ai.model:read" in AI_KNOWLEDGE_CURATOR_PERMISSIONS


def test_publisher_has_knowledge_base_publish():
    assert any(
        p.startswith("ai.knowledge_base:") and ":publish" in p for p in AI_PUBLISHER_PERMISSIONS
    )
    assert any(
        p.startswith("ai.knowledge_base:") and ":retire" in p for p in AI_PUBLISHER_PERMISSIONS
    )


def test_admin_includes_phase2_permissions():
    phase2_codes = {p[0] for p in AI_PHASE2_PERMISSIONS}
    assert phase2_codes.issubset(set(AI_PLATFORM_ADMIN_PERMISSIONS))


def test_phase2_permissions_in_master_list():
    all_codes = {p[0] for p in AI_PERMISSIONS}
    assert {p[0] for p in AI_PHASE2_PERMISSIONS}.issubset(all_codes)
