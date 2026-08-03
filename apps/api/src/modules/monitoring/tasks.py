"""Monitoring Celery task shell — Phase 0 (no business jobs)."""

from workers.celery_app import celery_app


@celery_app.task(name="monitoring.module_health_ping")
def module_health_ping() -> dict:
    """Idempotent module registration ping — no DB / APM / SIEM side effects."""
    return {"status": "ok", "module": "monitoring", "phase": 0}
