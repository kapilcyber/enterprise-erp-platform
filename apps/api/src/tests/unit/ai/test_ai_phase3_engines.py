"""AI Platform Phase 3 unit engine smoke tests."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.ai.domain.enums import ToolVersionStatus
from modules.ai.domain.exceptions import (
    PublishedAgentVersionImmutable,
    PublishedToolVersionImmutable,
    ToolAllowListViolation,
)
from modules.ai.service.engines import (
    AgentOrchestrationLimitsEngine,
    AgentVersionEngine,
    ToolAllowListEngine,
    ToolVersionEngine,
)


def test_tool_version_published_immutable():
    engine = ToolVersionEngine()
    row = SimpleNamespace(status=ToolVersionStatus.PUBLISHED.value)
    with pytest.raises(PublishedToolVersionImmutable):
        engine.assert_editable(row)


def test_agent_version_published_immutable():
    engine = AgentVersionEngine()
    row = SimpleNamespace(status="published")
    with pytest.raises(PublishedAgentVersionImmutable):
        engine.assert_editable(row)


def test_tool_allowlist_rejects_unpublished():
    engine = ToolAllowListEngine()
    tv_id = uuid4()
    lookup = {tv_id: SimpleNamespace(status=ToolVersionStatus.DRAFT.value)}
    with pytest.raises(ToolAllowListViolation):
        engine.validate_tool_version_ids([tv_id], published_lookup=lookup)


def test_tool_allowlist_accepts_published():
    engine = ToolAllowListEngine()
    tv_id = uuid4()
    lookup = {tv_id: SimpleNamespace(status=ToolVersionStatus.PUBLISHED.value)}
    engine.validate_tool_version_ids([tv_id], published_lookup=lookup)


def test_orchestration_limits_stub_valid():
    engine = AgentOrchestrationLimitsEngine()
    result = engine.validate(max_steps=10, max_tokens=4096)
    assert result["valid"] is True
    assert result["limits_mode"] == "metadata_stub"


def test_orchestration_limits_stub_rejects_excessive_steps():
    engine = AgentOrchestrationLimitsEngine()
    result = engine.validate(max_steps=500, max_tokens=None)
    assert result["valid"] is False
    assert any(i["code"] == "MAX_STEPS_EXCEEDS_CEILING" for i in result["issues"])
