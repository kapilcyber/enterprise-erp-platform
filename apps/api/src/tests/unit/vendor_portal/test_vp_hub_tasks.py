"""Vendor Portal Celery task name tests."""

from modules.vendor_portal import tasks


def test_task_names():
    assert tasks.session_expiry_sweeper.name == "vendor_portal.session_expiry_sweeper"
    assert tasks.rfq_view_sync.name == "vendor_portal.rfq_view_sync"
    assert tasks.po_view_sync.name == "vendor_portal.po_view_sync"
    assert tasks.payment_status_sync.name == "vendor_portal.payment_status_sync"
    assert tasks.notification_dispatcher.name == "vendor_portal.notification_dispatcher"
    assert tasks.login_audit_retention.name == "vendor_portal.login_audit_retention"
    assert tasks.asn_status_poller.name == "vendor_portal.asn_status_poller"
    assert tasks.quality_issue_poller.name == "vendor_portal.quality_issue_poller"
