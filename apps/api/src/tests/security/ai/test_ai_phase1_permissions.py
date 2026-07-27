"""AI Platform Phase 1 permission constant security smoke tests."""

from modules.ai.permissions import (
    AI_AUDITOR_PERMISSIONS,
    AI_CONSUMER_PERMISSIONS,
    AI_PERMISSIONS,
    AI_PLATFORM_ADMIN_PERMISSIONS,
    AI_PROMPT_ENGINEER_PERMISSIONS,
    AI_PUBLISHER_PERMISSIONS,
)


def test_permission_codes_use_ai_namespace():
    for code, resource, _action, module in AI_PERMISSIONS:
        assert code.startswith("ai.")
        assert resource.startswith("ai.")
        assert module == "ai"
        assert ":" in code


def test_admin_has_all_permissions():
    all_codes = {p[0] for p in AI_PERMISSIONS}
    assert set(AI_PLATFORM_ADMIN_PERMISSIONS) == all_codes


def test_auditor_is_read_heavy():
    assert all(":read" in p or ":audit" in p for p in AI_AUDITOR_PERMISSIONS)


def test_prompt_engineer_cannot_publish():
    assert not any(":publish" in p for p in AI_PROMPT_ENGINEER_PERMISSIONS)
    assert not any(":retire" in p for p in AI_PROMPT_ENGINEER_PERMISSIONS)


def test_publisher_has_publish():
    assert any(":publish" in p for p in AI_PUBLISHER_PERMISSIONS)


def test_consumer_has_invoke():
    assert "ai.invoke:invoke" in AI_CONSUMER_PERMISSIONS or any(
        "invoke" in p for p in AI_CONSUMER_PERMISSIONS
    )


def test_no_peer_module_permission_codes():
    blob = " ".join(p[0] for p in AI_PERMISSIONS)
    assert "foundation." not in blob
    assert "bpm." not in blob
    assert "lowcode." not in blob
