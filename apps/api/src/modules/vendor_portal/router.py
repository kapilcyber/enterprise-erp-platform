"""Vendor Portal module router aggregation."""

from fastapi import APIRouter

from modules.vendor_portal.routers import (
    asn_router,
    dashboard_router,
    dashboard_widget_router,
    delivery_schedule_router,
    document_access_router,
    invoice_submission_router,
    login_audit_router,
    message_router,
    message_thread_router,
    notification_router,
    payment_status_router,
    po_acknowledgement_router,
    portal_account_router,
    portal_session_router,
    preference_router,
    purchase_order_view_router,
    quote_submission_router,
    report_router,
    rfq_view_router,
    supplier_profile_router,
)

vendor_portal_router = APIRouter(prefix="/vendor-portal")
vendor_portal_router.include_router(portal_account_router)
vendor_portal_router.include_router(supplier_profile_router)
vendor_portal_router.include_router(portal_session_router)
vendor_portal_router.include_router(dashboard_router)
vendor_portal_router.include_router(dashboard_widget_router)
vendor_portal_router.include_router(rfq_view_router)
vendor_portal_router.include_router(quote_submission_router)
vendor_portal_router.include_router(purchase_order_view_router)
vendor_portal_router.include_router(po_acknowledgement_router)
vendor_portal_router.include_router(delivery_schedule_router)
vendor_portal_router.include_router(asn_router)
vendor_portal_router.include_router(invoice_submission_router)
vendor_portal_router.include_router(payment_status_router)
vendor_portal_router.include_router(document_access_router)
vendor_portal_router.include_router(notification_router)
vendor_portal_router.include_router(message_thread_router)
vendor_portal_router.include_router(message_router)
vendor_portal_router.include_router(preference_router)
vendor_portal_router.include_router(login_audit_router)
vendor_portal_router.include_router(report_router)
