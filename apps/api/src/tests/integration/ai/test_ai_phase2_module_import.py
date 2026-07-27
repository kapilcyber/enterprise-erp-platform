"""AI Platform Phase 2 module import / mount / ownership smoke tests."""

from uuid import uuid4


def test_phase2_models_export_26():
    from modules.ai import models

    assert len(models.__all__) >= 26
    assert models.AiKnowledgeBase is not None
    assert models.AiKnowledgeSource is not None
    assert models.AiKnowledgeChunk is not None
    assert models.AiEmbedding is not None
    assert models.AiVectorIndex is not None


def test_phase1_subset_still_present():
    from modules.ai import models

    phase1 = {
        "AiProvider",
        "AiModel",
        "AiCacheEntry",
        "AiAssistant",
    }
    assert phase1.issubset(set(models.__all__))


def test_no_live_rag_methods_on_knowledge_services():
    from modules.ai.service.embedding_service import EmbeddingService
    from modules.ai.service.knowledge_base_service import KnowledgeBaseService
    from modules.ai.service.knowledge_ingestion_service import KnowledgeIngestionService

    forbidden = {
        "retrieve",
        "semantic_search",
        "embed",
        "vector_search",
        "reason",
        "long_term_recall",
    }
    for svc in (KnowledgeBaseService, EmbeddingService, KnowledgeIngestionService):
        methods = {m for m in dir(svc) if not m.startswith("_")}
        assert methods.isdisjoint(forbidden), svc.__name__


def test_document_port_exists():
    from modules.ai.adapters import AiDocumentAdapter

    adapter = AiDocumentAdapter(db=None)  # type: ignore[arg-type]
    doc_id = uuid4()
    assert adapter.resolve_document_ref(None, doc_id) == doc_id  # type: ignore[arg-type]


def test_alembic_phase2_chain():
    from pathlib import Path

    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    expected = [
        "0543_ai_knowledge_base.py",
        "0544_ai_knowledge_source.py",
        "0545_ai_knowledge_chunk.py",
        "0546_ai_embedding.py",
        "0547_ai_vector_index.py",
        "0548_seed_ai_phase2_permissions.py",
    ]
    for name in expected:
        assert (versions / name).exists(), name


def test_application_service_wires_phase2():
    import inspect

    from modules.ai.service.application_service import AiApplicationService

    src = inspect.getsource(AiApplicationService.__init__)
    for attr in (
        "knowledge_bases",
        "knowledge_sources",
        "knowledge_chunks",
        "embeddings",
        "vector_indexes",
        "knowledge_ingestion",
    ):
        assert f"self.{attr}" in src


def test_phase2_tasks_registered():
    from modules.ai import tasks

    assert hasattr(tasks, "knowledge_ingestion_metadata_sweep")
    assert hasattr(tasks, "embedding_metadata_rebuild_sweep")
