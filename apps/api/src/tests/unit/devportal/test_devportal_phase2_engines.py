"""Unit tests — Developer Portal Phase 2 engines."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.devportal.domain.exceptions import (
    InvalidPlanState,
    PublishedPlanImmutable,
    SubscriptionBindingError,
)
from modules.devportal.service.engines import (
    EntitlementEngine,
    PlanLifecycleEngine,
    SubscriptionEligibilityEngine,
    SubscriptionLifecycleEngine,
)


def test_plan_publish_immutable():
    engine = PlanLifecycleEngine()
    user = uuid4()
    row = SimpleNamespace(
        status="draft",
        published_at=None,
        published_by=None,
        retired_at=None,
        retired_by=None,
    )
    engine.publish(row, user_id=user)
    assert row.status == "published"
    with pytest.raises(PublishedPlanImmutable):
        engine.assert_editable(row)


def test_plan_retire_from_published():
    engine = PlanLifecycleEngine()
    user = uuid4()
    row = SimpleNamespace(
        status="published",
        published_at=None,
        published_by=None,
        retired_at=None,
        retired_by=None,
    )
    engine.retire(row, user_id=user)
    assert row.status == "retired"
    with pytest.raises(InvalidPlanState):
        engine.assert_editable(row)


def test_subscription_lifecycle():
    engine = SubscriptionLifecycleEngine()
    row = SimpleNamespace(status="draft", workflow_status=None)
    engine.submit(row)
    engine.approve(row)
    engine.activate(row)
    assert row.status == "active"
    engine.suspend(row)
    assert row.status == "suspended"


def test_subscription_requires_published_plan_and_version():
    engine = SubscriptionEligibilityEngine()
    with pytest.raises(SubscriptionBindingError):
        engine.assert_binding_ok(
            plan=SimpleNamespace(status="draft"),
            product_version=SimpleNamespace(status="published"),
            application=SimpleNamespace(id=uuid4()),
        )
    engine.assert_binding_ok(
        plan=SimpleNamespace(status="published"),
        product_version=SimpleNamespace(status="published"),
        application=SimpleNamespace(id=uuid4()),
    )


def test_entitlement_metadata_lifecycle():
    engine = EntitlementEngine()
    row = SimpleNamespace(status="active")
    engine.suspend(row)
    assert row.status == "suspended"
    engine.activate(row)
    assert row.status == "active"
    engine.retire(row)
    assert row.status == "retired"
