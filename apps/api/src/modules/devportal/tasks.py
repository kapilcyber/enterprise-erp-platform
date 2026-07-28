"""API Developer Portal Celery tasks — Phase 0 health ping only."""

from workers.celery_app import celery_app


@celery_app.task(name="devportal.module_health_ping")
def module_health_ping() -> dict:
    """Idempotent module registration ping — no DB / Hub / gateway side effects."""
    return {"status": "ok", "module": "devportal", "phase": 4}
