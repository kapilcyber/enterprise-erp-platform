"""AI Platform Phase 3 permission constant security smoke tests."""

from modules.ai.permissions import (
    AI_AGENT_DESIGNER_PERMISSIONS,
    AI_PERMISSIONS,
    AI_PHASE3_PERMISSIONS,
    AI_PLATFORM_ADMIN_PERMISSIONS,
    AI_PUBLISHER_PERMISSIONS,
)


def test_phase3_permission_namespace():
    for code, resource, _action, module in AI_PHASE3_PERMISSIONS:
        assert code.startswith("ai.")
        assert resource.startswith("ai.")
        assert module == "ai"
        assert any(
            resource.startswith(f"ai.{r}")
            for r in ("tool", "tool_version", "skill", "agent", "agent_version")
        )


def test_agent_designer_has_design_perms_no_publish():
    assert any("tool:create" in p for p in AI_AGENT_DESIGNER_PERMISSIONS)
    assert any("skill:create" in p for p in AI_AGENT_DESIGNER_PERMISSIONS)
    assert any("agent:create" in p for p in AI_AGENT_DESIGNER_PERMISSIONS)
    assert not any(":publish" in p for p in AI_AGENT_DESIGNER_PERMISSIONS)
    assert not any(":retire" in p for p in AI_AGENT_DESIGNER_PERMISSIONS)
    assert not any(":validate" in p for p in AI_AGENT_DESIGNER_PERMISSIONS)


def test_publisher_has_tool_and_agent_version_publish():
    assert any(
        p.startswith("ai.tool_version:") and ":publish" in p for p in AI_PUBLISHER_PERMISSIONS
    )
    assert any(
        p.startswith("ai.agent_version:") and ":publish" in p for p in AI_PUBLISHER_PERMISSIONS
    )
    assert any(p.startswith("ai.skill:") and ":publish" in p for p in AI_PUBLISHER_PERMISSIONS)


def test_admin_includes_phase3_permissions():
    phase3_codes = {p[0] for p in AI_PHASE3_PERMISSIONS}
    assert phase3_codes.issubset(set(AI_PLATFORM_ADMIN_PERMISSIONS))


def test_phase3_permissions_in_master_list():
    all_codes = {p[0] for p in AI_PERMISSIONS}
    assert {p[0] for p in AI_PHASE3_PERMISSIONS}.issubset(all_codes)
