"""BPM Celery task stubs — Phase 1."""

from workers.celery_app import celery_app


@celery_app.task(name="bpm.definition_inventory_snapshot")
def definition_inventory_snapshot() -> dict:
    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.bpm.models import BpmWorkflowDefinition

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(BpmWorkflowDefinition).where(
                    BpmWorkflowDefinition.is_deleted.is_(False)
                )
            ).all()
        )
        return {"status": "ok", "definitions": len(rows)}
    finally:
        db.close()


@celery_app.task(name="bpm.published_version_guard")
def published_version_guard() -> dict:
    """Detect definitions with more than one published version (integrity check)."""
    from collections import defaultdict

    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.bpm.models import BpmWorkflowVersion

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(BpmWorkflowVersion).where(
                    BpmWorkflowVersion.is_deleted.is_(False),
                    BpmWorkflowVersion.status == "published",
                )
            ).all()
        )
        counts: dict = defaultdict(int)
        for row in rows:
            counts[str(row.definition_id)] += 1
        violations = {k: v for k, v in counts.items() if v > 1}
        return {"status": "ok", "published": len(rows), "violations": violations}
    finally:
        db.close()


@celery_app.task(name="bpm.draft_aging_report")
def draft_aging_report() -> dict:
    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.bpm.models import BpmWorkflowVersion

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(BpmWorkflowVersion).where(
                    BpmWorkflowVersion.is_deleted.is_(False),
                    BpmWorkflowVersion.status == "draft",
                )
            ).all()
        )
        return {"status": "ok", "draft_versions": len(rows)}
    finally:
        db.close()
