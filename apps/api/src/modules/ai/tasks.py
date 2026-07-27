"""AI Platform Celery task shells — Phase 1 + Phase 2 (idempotent, no provider SDK)."""

from workers.celery_app import celery_app


@celery_app.task(name="ai.module_health_ping")
def module_health_ping() -> dict:
    """Idempotent module registration ping — no DB / provider / LLM side effects."""
    return {"status": "ok", "module": "ai", "phase": 1}


@celery_app.task(name="ai.published_prompt_guard")
def published_prompt_guard() -> dict:
    """Detect prompt templates with more than one published version (integrity check)."""
    from collections import defaultdict

    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.ai.domain.enums import PromptVersionStatus
    from modules.ai.models import AiPromptVersion

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(AiPromptVersion).where(
                    AiPromptVersion.status == PromptVersionStatus.PUBLISHED.value,
                    AiPromptVersion.is_deleted.is_(False),
                )
            ).all()
        )
        counts: dict[str, int] = defaultdict(int)
        for row in rows:
            counts[str(row.template_id)] += 1
        violations = {k: v for k, v in counts.items() if v > 1}
        return {"status": "ok", "violations": violations, "published": len(rows)}
    finally:
        db.close()


@celery_app.task(name="ai.session_expiry_sweep")
def session_expiry_sweep() -> dict:
    """Report open sessions past expires_at — metadata sweep only (no provider calls)."""
    from datetime import datetime, timezone

    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.ai.domain.enums import SessionStatus
    from modules.ai.models import AiSession

    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        rows = list(
            db.scalars(
                select(AiSession).where(
                    AiSession.status == SessionStatus.OPEN.value,
                    AiSession.is_deleted.is_(False),
                    AiSession.expires_at.is_not(None),
                    AiSession.expires_at < now,
                )
            ).all()
        )
        return {"status": "ok", "expired_candidates": len(rows)}
    finally:
        db.close()


@celery_app.task(name="ai.cache_expiry_sweep")
def cache_expiry_sweep() -> dict:
    """Report active cache entries past expires_at — metadata sweep only."""
    from datetime import datetime, timezone

    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.ai.domain.enums import CacheEntryStatus
    from modules.ai.models import AiCacheEntry

    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        rows = list(
            db.scalars(
                select(AiCacheEntry).where(
                    AiCacheEntry.status == CacheEntryStatus.CREATED.value,
                    AiCacheEntry.is_deleted.is_(False),
                    AiCacheEntry.expires_at.is_not(None),
                    AiCacheEntry.expires_at < now,
                )
            ).all()
        )
        return {"status": "ok", "expired_candidates": len(rows)}
    finally:
        db.close()


@celery_app.task(name="ai.knowledge_ingestion_metadata_sweep")
def knowledge_ingestion_metadata_sweep(knowledge_base_id: str) -> dict:
    """Metadata ingestion sweep stub — flip statuses safely, no provider SDK."""
    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.ai.domain.enums import VectorIndexStatus
    from modules.ai.models import AiVectorIndex

    db = SessionLocal()
    try:
        indexes = list(
            db.scalars(
                select(AiVectorIndex).where(
                    AiVectorIndex.knowledge_base_id == knowledge_base_id,
                    AiVectorIndex.is_deleted.is_(False),
                    AiVectorIndex.status == VectorIndexStatus.REBUILDING.value,
                )
            ).all()
        )
        activated = 0
        for index in indexes:
            index.status = VectorIndexStatus.ACTIVE.value
            activated += 1
        if activated:
            db.commit()
        return {
            "status": "ok",
            "knowledge_base_id": knowledge_base_id,
            "indexes_activated": activated,
        }
    finally:
        db.close()


@celery_app.task(name="ai.embedding_metadata_rebuild_sweep")
def embedding_metadata_rebuild_sweep() -> dict:
    """Report embedding metadata candidates for rebuild — no provider SDK."""
    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.ai.domain.enums import EmbeddingStatus
    from modules.ai.models import AiEmbedding

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(AiEmbedding).where(
                    AiEmbedding.status == EmbeddingStatus.CREATED.value,
                    AiEmbedding.is_deleted.is_(False),
                )
            ).all()
        )
        return {"status": "ok", "rebuild_candidates": len(rows)}
    finally:
        db.close()


@celery_app.task(name="ai.published_tool_version_guard")
def published_tool_version_guard() -> dict:
    """Detect tools with more than one published version (integrity check)."""
    from collections import defaultdict

    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.ai.domain.enums import ToolVersionStatus
    from modules.ai.models import AiToolVersion

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(AiToolVersion).where(
                    AiToolVersion.status == ToolVersionStatus.PUBLISHED.value,
                    AiToolVersion.is_deleted.is_(False),
                )
            ).all()
        )
        counts: dict[str, int] = defaultdict(int)
        for row in rows:
            counts[str(row.tool_id)] += 1
        violations = {k: v for k, v in counts.items() if v > 1}
        return {"status": "ok", "violations": violations, "published": len(rows)}
    finally:
        db.close()


@celery_app.task(name="ai.published_agent_version_guard")
def published_agent_version_guard() -> dict:
    """Detect agents with more than one published version (integrity check)."""
    from collections import defaultdict

    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.ai.domain.enums import AgentVersionStatus
    from modules.ai.models import AiAgentVersion

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(AiAgentVersion).where(
                    AiAgentVersion.status == AgentVersionStatus.PUBLISHED.value,
                    AiAgentVersion.is_deleted.is_(False),
                )
            ).all()
        )
        counts: dict[str, int] = defaultdict(int)
        for row in rows:
            counts[str(row.agent_id)] += 1
        violations = {k: v for k, v in counts.items() if v > 1}
        return {"status": "ok", "violations": violations, "published": len(rows)}
    finally:
        db.close()


@celery_app.task(name="ai.evaluation_stale_metadata_sweep")
def evaluation_stale_metadata_sweep() -> dict:
    """Report evaluations stuck in running state (metadata integrity check only)."""
    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.ai.domain.enums import EvaluationStatus
    from modules.ai.models import AiEvaluation

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(AiEvaluation).where(
                    AiEvaluation.status == EvaluationStatus.RUNNING.value,
                    AiEvaluation.is_deleted.is_(False),
                )
            ).all()
        )
        return {"status": "ok", "running_count": len(rows), "mode": "metadata_only"}
    finally:
        db.close()
