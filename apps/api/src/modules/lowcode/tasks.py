"""Low-Code Celery task stubs — Phase 1."""

from workers.celery_app import celery_app


@celery_app.task(name="lowcode.form_inventory_snapshot")
def form_inventory_snapshot() -> dict:
    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.lowcode.models import LcFormDefinition

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(LcFormDefinition).where(LcFormDefinition.is_deleted.is_(False))
            ).all()
        )
        return {"status": "ok", "definitions": len(rows)}
    finally:
        db.close()


@celery_app.task(name="lowcode.published_version_guard")
def published_version_guard() -> dict:
    """Detect definitions with more than one published version (integrity check)."""
    from collections import defaultdict

    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.lowcode.domain.enums import VersionStatus
    from modules.lowcode.models import LcFormVersion

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(LcFormVersion).where(
                    LcFormVersion.status == VersionStatus.PUBLISHED.value,
                    LcFormVersion.is_deleted.is_(False),
                )
            ).all()
        )
        counts: dict = defaultdict(int)
        for r in rows:
            counts[str(r.definition_id)] += 1
        violations = {k: v for k, v in counts.items() if v > 1}
        return {"status": "ok", "violations": violations, "published": len(rows)}
    finally:
        db.close()


@celery_app.task(name="lowcode.draft_aging_report")
def draft_aging_report() -> dict:
    from sqlalchemy import select

    from database.session import SessionLocal
    from modules.lowcode.domain.enums import VersionStatus
    from modules.lowcode.models import LcFormVersion

    db = SessionLocal()
    try:
        rows = list(
            db.scalars(
                select(LcFormVersion).where(
                    LcFormVersion.status == VersionStatus.DRAFT.value,
                    LcFormVersion.is_deleted.is_(False),
                )
            ).all()
        )
        return {"status": "ok", "drafts": len(rows)}
    finally:
        db.close()
