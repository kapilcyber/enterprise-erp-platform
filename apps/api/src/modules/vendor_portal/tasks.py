"""Vendor Portal Celery tasks per ERD_24."""

from workers.celery_app import celery_app


@celery_app.task(name="vendor_portal.session_expiry_sweeper")
def session_expiry_sweeper() -> dict:
    return {"ok": True, "task": "vendor_portal.session_expiry_sweeper"}


@celery_app.task(name="vendor_portal.rfq_view_sync")
def rfq_view_sync() -> dict:
    return {"ok": True, "task": "vendor_portal.rfq_view_sync"}


@celery_app.task(name="vendor_portal.po_view_sync")
def po_view_sync() -> dict:
    return {"ok": True, "task": "vendor_portal.po_view_sync"}


@celery_app.task(name="vendor_portal.payment_status_sync")
def payment_status_sync() -> dict:
    return {"ok": True, "task": "vendor_portal.payment_status_sync"}


@celery_app.task(name="vendor_portal.notification_dispatcher")
def notification_dispatcher() -> dict:
    return {"ok": True, "task": "vendor_portal.notification_dispatcher"}


@celery_app.task(name="vendor_portal.login_audit_retention")
def login_audit_retention() -> dict:
    return {"ok": True, "task": "vendor_portal.login_audit_retention"}


@celery_app.task(name="vendor_portal.asn_status_poller")
def asn_status_poller() -> dict:
    return {"ok": True, "task": "vendor_portal.asn_status_poller"}


@celery_app.task(name="vendor_portal.quality_issue_poller")
def quality_issue_poller() -> dict:
    return {"ok": True, "task": "vendor_portal.quality_issue_poller"}
