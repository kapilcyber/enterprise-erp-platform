"""VendorPortalApplicationService facade."""

from sqlalchemy.orm import Session

from modules.vendor_portal.service.asn_service import AsnService
from modules.vendor_portal.service.dashboard_service import DashboardService
from modules.vendor_portal.service.dashboard_widget_service import DashboardWidgetService
from modules.vendor_portal.service.delivery_schedule_service import DeliveryScheduleService
from modules.vendor_portal.service.document_access_service import DocumentAccessService
from modules.vendor_portal.service.invoice_submission_service import InvoiceSubmissionService
from modules.vendor_portal.service.login_audit_service import LoginAuditService
from modules.vendor_portal.service.message_service import MessageService
from modules.vendor_portal.service.message_thread_service import MessageThreadService
from modules.vendor_portal.service.notification_service import NotificationService
from modules.vendor_portal.service.payment_status_service import PaymentStatusService
from modules.vendor_portal.service.po_acknowledgement_service import PoAcknowledgementService
from modules.vendor_portal.service.portal_account_service import PortalAccountService
from modules.vendor_portal.service.portal_session_service import PortalSessionService
from modules.vendor_portal.service.preference_service import PreferenceService
from modules.vendor_portal.service.purchase_order_view_service import PurchaseOrderViewService
from modules.vendor_portal.service.quote_submission_service import QuoteSubmissionService
from modules.vendor_portal.service.report_service import ReportService
from modules.vendor_portal.service.rfq_view_service import RfqViewService
from modules.vendor_portal.service.supplier_profile_service import SupplierProfileService
from modules.vendor_portal.service.vendor_portal_integration_service import (
    VendorPortalIntegrationService,
)


class VendorPortalApplicationService:
    def __init__(self, db: Session) -> None:
        self.portal_account = PortalAccountService(db)
        self.supplier_profile = SupplierProfileService(db)
        self.portal_session = PortalSessionService(db)
        self.dashboard = DashboardService(db)
        self.dashboard_widget = DashboardWidgetService(db)
        self.rfq_view = RfqViewService(db)
        self.quote_submission = QuoteSubmissionService(db)
        self.purchase_order_view = PurchaseOrderViewService(db)
        self.po_acknowledgement = PoAcknowledgementService(db)
        self.delivery_schedule = DeliveryScheduleService(db)
        self.asn = AsnService(db)
        self.invoice_submission = InvoiceSubmissionService(db)
        self.payment_status = PaymentStatusService(db)
        self.document_access = DocumentAccessService(db)
        self.notification = NotificationService(db)
        self.message_thread = MessageThreadService(db)
        self.message = MessageService(db)
        self.preference = PreferenceService(db)
        self.login_audit = LoginAuditService(db)
        self.report = ReportService(db)
        self.integration = VendorPortalIntegrationService(db)
