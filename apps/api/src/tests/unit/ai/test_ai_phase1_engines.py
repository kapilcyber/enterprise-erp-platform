"""AI Platform Phase 1 unit engine smoke tests."""

from types import SimpleNamespace

import pytest

from modules.ai.domain.enums import PromptVersionStatus, ProviderStatus
from modules.ai.domain.exceptions import InvalidProviderState, PublishedPromptVersionImmutable
from modules.ai.service.engines import (
    CacheEligibilityEngine,
    PromptVersionEngine,
    ProviderEngine,
    ProviderFailoverEngine,
)


def test_provider_engine_suspend_activate():
    engine = ProviderEngine()
    row = SimpleNamespace(status=ProviderStatus.ACTIVE.value)
    engine.suspend(row)
    assert row.status == ProviderStatus.SUSPENDED.value
    engine.activate(row)
    assert row.status == ProviderStatus.ACTIVE.value


def test_provider_engine_invalid_double_activate():
    engine = ProviderEngine()
    row = SimpleNamespace(status=ProviderStatus.ACTIVE.value)
    with pytest.raises(InvalidProviderState):
        engine.activate(row)


def test_prompt_version_published_immutable():
    engine = PromptVersionEngine()
    row = SimpleNamespace(status=PromptVersionStatus.PUBLISHED.value)
    with pytest.raises(PublishedPromptVersionImmutable):
        engine.assert_editable(row)


def test_cache_eligibility_never_bypasses_guardrails():
    engine = CacheEligibilityEngine()
    assert engine.is_eligible(guardrails_required=True, moderation_required=False) is False
    assert engine.is_eligible(guardrails_required=False, moderation_required=True) is False
    assert engine.is_eligible(guardrails_required=False, moderation_required=False) is True


def test_provider_failover_stub():
    engine = ProviderFailoverEngine()
    result = engine.resolve_fallback([], primary_provider_id=None, primary_model_id=None)
    assert isinstance(result, dict)
    assert result.get("degraded") is True
