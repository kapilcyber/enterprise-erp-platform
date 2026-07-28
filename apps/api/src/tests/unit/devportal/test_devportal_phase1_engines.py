"""Unit tests — Developer Portal Phase 1 engines."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.devportal.domain.exceptions import (
    InvalidApiProductVersionState,
    InvalidDeveloperAccountState,
    PublishedApiProductVersionImmutable,
)
from modules.devportal.service.engines import (
    AccountLifecycleEngine,
    ApplicationLifecycleEngine,
    InviteLifecycleEngine,
    PortalSessionEngine,
    ProductVersionLifecycleEngine,
    PublishGateEngine,
)


def test_account_submit_approve_activate():
    engine = AccountLifecycleEngine()
    row = SimpleNamespace(status="draft", workflow_status=None)
    engine.submit(row)
    assert row.status == "submitted"
    engine.approve(row)
    assert row.status == "approved"
    engine.activate(row)
    assert row.status == "active"


def test_account_submit_rejects_non_draft():
    engine = AccountLifecycleEngine()
    row = SimpleNamespace(status="active", workflow_status=None)
    with pytest.raises(InvalidDeveloperAccountState):
        engine.submit(row)


def test_invite_approval_then_send():
    engine = InviteLifecycleEngine()
    row = SimpleNamespace(status="draft", workflow_status=None)
    engine.submit(row)
    engine.approve(row)
    engine.mark_sent(row)
    assert row.status == "sent"


def test_application_lifecycle():
    engine = ApplicationLifecycleEngine()
    row = SimpleNamespace(status="draft", workflow_status=None)
    engine.submit(row)
    engine.approve(row)
    engine.activate(row)
    assert row.status == "active"
    engine.suspend(row)
    assert row.status == "suspended"


def test_product_version_publish_immutable():
    engine = ProductVersionLifecycleEngine()
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
    with pytest.raises(PublishedApiProductVersionImmutable):
        engine.assert_editable(row)


def test_product_version_retire_from_published():
    engine = ProductVersionLifecycleEngine()
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
    with pytest.raises(InvalidApiProductVersionState):
        engine.assert_editable(row)


def test_publish_gate_requires_draft():
    gate = PublishGateEngine()
    issues = gate.validate_draft_for_publish(
        SimpleNamespace(status="published", version_label="1.0", product_id=uuid4())
    )
    assert any(i.code == "NOT_DRAFT" for i in issues)


def test_portal_session_expire_revoke():
    engine = PortalSessionEngine()
    row = SimpleNamespace(status="active")
    engine.expire(row)
    assert row.status == "expired"
    row2 = SimpleNamespace(status="active")
    engine.revoke(row2)
    assert row2.status == "revoked"
