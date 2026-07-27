"""AI Platform Phase 2 unit engine smoke tests."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.ai.domain.enums import KnowledgeBaseStatus
from modules.ai.domain.exceptions import PublishedKnowledgeBaseImmutable
from modules.ai.service.engines import (
    CitationEngine,
    KnowledgeBaseEngine,
    RagRankingEngine,
)


def test_knowledge_base_published_immutable():
    engine = KnowledgeBaseEngine()
    row = SimpleNamespace(status=KnowledgeBaseStatus.PUBLISHED.value)
    with pytest.raises(PublishedKnowledgeBaseImmutable):
        engine.assert_editable(row)


def test_knowledge_base_publish_retire():
    engine = KnowledgeBaseEngine()
    user_id = uuid4()
    row = SimpleNamespace(
        status=KnowledgeBaseStatus.DRAFT.value,
        published_at=None,
        published_by=None,
        publish_reason=None,
        retired_at=None,
        retired_by=None,
        retire_reason=None,
    )
    engine.publish(row, user_id=user_id, publish_reason="ready")
    assert row.status == KnowledgeBaseStatus.PUBLISHED.value
    assert row.publish_reason == "ready"
    engine.retire(row, user_id=user_id)
    assert row.status == KnowledgeBaseStatus.RETIRED.value


def test_rag_ranking_stub_orders_by_sequence():
    engine = RagRankingEngine()
    chunks = [
        SimpleNamespace(
            id=uuid4(),
            chunk_code="C2",
            sequence_no=2,
            knowledge_source_id=uuid4(),
            content_preview="b",
        ),
        SimpleNamespace(
            id=uuid4(),
            chunk_code="C1",
            sequence_no=1,
            knowledge_source_id=uuid4(),
            content_preview="a",
        ),
    ]
    result = engine.rank_chunks(chunks)
    assert result["retrieval_mode"] == "metadata_stub"
    ranks = [item["sequence_no"] for item in result["ranked_chunks"]]
    assert ranks == [1, 2]


def test_citation_stub_builds_refs():
    engine = CitationEngine()
    chunk_id = uuid4()
    source_id = uuid4()
    document_id = uuid4()
    result = engine.build_citations(
        chunk_id=chunk_id,
        source_id=source_id,
        document_id=document_id,
        chunk_code="AIKC-001",
        source_code="AIKS-001",
    )
    assert len(result["citations"]) == 1
    cite = result["citations"][0]
    assert cite["chunk_id"] == str(chunk_id)
    assert cite["document_id"] == str(document_id)
    assert cite["citation_type"] == "metadata_ref"
