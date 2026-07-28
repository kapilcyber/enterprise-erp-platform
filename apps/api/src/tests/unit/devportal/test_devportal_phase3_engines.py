"""Unit tests — Developer Portal Phase 3 engines."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.devportal.domain.exceptions import (
    DocumentationEntryTypeError,
    PublishedDocumentationImmutable,
    TryitInvokeForbidden,
)
from modules.devportal.service.engines import (
    DocumentationEntryEngine,
    OpenApiArtifactEngine,
    SandboxEnvironmentEngine,
    TryitSessionEngine,
)


def test_documentation_entry_types_and_publish():
    engine = DocumentationEntryEngine()
    engine.assert_entry_type("guide")
    engine.assert_entry_type("tutorial")
    engine.assert_entry_type("changelog")
    engine.assert_entry_type("release_notes")
    with pytest.raises(DocumentationEntryTypeError):
        engine.assert_entry_type("blog")
    row = SimpleNamespace(
        status="draft",
        published_at=None,
        published_by=None,
        retired_at=None,
        retired_by=None,
    )
    engine.publish(row, user_id=uuid4())
    assert row.status == "published"
    with pytest.raises(PublishedDocumentationImmutable):
        engine.assert_editable(row)


def test_openapi_artifact_requires_document_uuid():
    engine = OpenApiArtifactEngine()
    issues = engine.validate_reference(document_id=None, product_version_id=uuid4())
    assert any(i.code == "MISSING_DOCUMENT_ID" for i in issues)


def test_sandbox_activate_retire():
    engine = SandboxEnvironmentEngine()
    row = SimpleNamespace(status="draft")
    engine.activate(row)
    assert row.status == "active"
    engine.retire(row)
    assert row.status == "retired"


def test_tryit_close_expire_and_invoke_forbidden():
    engine = TryitSessionEngine()
    row = SimpleNamespace(status="active", closed_at=None)
    engine.close(row)
    assert row.status == "closed"
    row2 = SimpleNamespace(status="active", closed_at=None)
    engine.expire(row2)
    assert row2.status == "expired"
    with pytest.raises(TryitInvokeForbidden):
        engine.assert_metadata_only()
