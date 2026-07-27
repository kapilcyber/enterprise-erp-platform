"""AI Platform Phase 4 permission constant security smoke tests."""

from modules.ai.permissions import (
    AI_PERMISSIONS,
    AI_PHASE4_PERMISSIONS,
    AI_PLATFORM_ADMIN_PERMISSIONS,
    AI_PUBLISHER_PERMISSIONS,
    AI_QUALITY_ANALYST_PERMISSIONS,
)


def test_phase4_permission_namespace():
    for code, resource, _action, module in AI_PHASE4_PERMISSIONS:
        assert code.startswith("ai.")
        assert resource.startswith("ai.")
        assert module == "ai"
        assert any(
            resource.startswith(f"ai.{r}")
            for r in ("evaluation", "feedback", "multimodal_profile")
        )


def test_quality_analyst_has_evaluation_and_feedback_no_publish():
    assert any("evaluation:create" in p for p in AI_QUALITY_ANALYST_PERMISSIONS)
    assert any("feedback:create" in p for p in AI_QUALITY_ANALYST_PERMISSIONS)
    assert not any(":publish" in p for p in AI_QUALITY_ANALYST_PERMISSIONS)
    assert not any(":retire" in p for p in AI_QUALITY_ANALYST_PERMISSIONS)


def test_publisher_has_multimodal_profile_publish():
    assert any(
        p.startswith("ai.multimodal_profile:") and ":publish" in p
        for p in AI_PUBLISHER_PERMISSIONS
    )


def test_admin_includes_phase4_permissions():
    phase4_codes = {p[0] for p in AI_PHASE4_PERMISSIONS}
    assert phase4_codes.issubset(set(AI_PLATFORM_ADMIN_PERMISSIONS))


def test_phase4_permissions_in_master_list():
    all_codes = {p[0] for p in AI_PERMISSIONS}
    assert {p[0] for p in AI_PHASE4_PERMISSIONS}.issubset(all_codes)
