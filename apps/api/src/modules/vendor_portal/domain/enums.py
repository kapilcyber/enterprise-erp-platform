"""Vendor Portal domain enums per ERD_24."""

from enum import Enum


class PortalAccountStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    ACTIVE = "active"
    LOCKED = "locked"
    SUSPENDED = "suspended"
    RETIRED = "retired"

class SupplierProfileStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    ACTIVE = "active"
    INACTIVE = "inactive"

class PortalSessionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"

class DashboardStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"

class DashboardWidgetStatus(str, Enum):
    ACTIVE = "active"
    HIDDEN = "hidden"

class RfqViewStatus(str, Enum):
    VISIBLE = "visible"
    HIDDEN = "hidden"
    STALE = "stale"
    CLOSED = "closed"

class QuoteSubmissionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class PurchaseOrderViewStatus(str, Enum):
    VISIBLE = "visible"
    HIDDEN = "hidden"
    STALE = "stale"
    CLOSED = "closed"

class PoAcknowledgementStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"

class DeliveryScheduleStatus(str, Enum):
    PLANNED = "planned"
    CONFIRMED = "confirmed"
    PARTIALLY_SHIPPED = "partially_shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AsnStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    IN_TRANSIT = "in_transit"
    RECEIVED_SNAPSHOT = "received_snapshot"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class InvoiceSubmissionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class PaymentStatusStatus(str, Enum):
    VISIBLE = "visible"
    PENDING_SNAPSHOT = "pending_snapshot"
    PAID_SNAPSHOT = "paid_snapshot"
    PARTIAL_SNAPSHOT = "partial_snapshot"
    OVERDUE_SNAPSHOT = "overdue_snapshot"
    STALE = "stale"
    HIDDEN = "hidden"

class DocumentAccessStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"

class NotificationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

class MessageThreadStatus(str, Enum):
    OPEN = "open"
    WAITING = "waiting"
    CLOSED = "closed"

class MessageStatus(str, Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    DELETED = "deleted"

class PreferenceStatus(str, Enum):
    ACTIVE = "active"

class LoginAuditStatus(str, Enum):
    RECORDED = "recorded"

class ReportStatus(str, Enum):
    DRAFT = "draft"
    FINALIZED = "finalized"

class VendorPortalEntityType(str, Enum):
    PORTAL_ACCOUNT = "portal_account"
    SUPPLIER_PROFILE = "supplier_profile"
    PORTAL_SESSION = "portal_session"
    DASHBOARD = "dashboard"
    RFQ_VIEW = "rfq_view"
    QUOTE_SUBMISSION = "quote_submission"
    PURCHASE_ORDER_VIEW = "purchase_order_view"
    PO_ACKNOWLEDGEMENT = "po_acknowledgement"
    DELIVERY_SCHEDULE = "delivery_schedule"
    ASN = "asn"
    INVOICE_SUBMISSION = "invoice_submission"
    PAYMENT_STATUS = "payment_status"
    DOCUMENT_ACCESS = "document_access"
    NOTIFICATION = "notification"
    MESSAGE_THREAD = "message_thread"
    MESSAGE = "message"
    LOGIN_AUDIT = "login_audit"

CODE_PREFIXES: dict[VendorPortalEntityType, tuple[str, int, bool]] = {
    VendorPortalEntityType.PORTAL_ACCOUNT: ("ACC-", 6, True),
    VendorPortalEntityType.SUPPLIER_PROFILE: ("PRF-", 6, True),
    VendorPortalEntityType.PORTAL_SESSION: ("SES-", 6, True),
    VendorPortalEntityType.DASHBOARD: ("DSH-", 6, True),
    VendorPortalEntityType.RFQ_VIEW: ("RFQ-", 6, True),
    VendorPortalEntityType.QUOTE_SUBMISSION: ("QTE-", 6, True),
    VendorPortalEntityType.PURCHASE_ORDER_VIEW: ("POV-", 6, True),
    VendorPortalEntityType.PO_ACKNOWLEDGEMENT: ("ACK-", 6, True),
    VendorPortalEntityType.DELIVERY_SCHEDULE: ("DLS-", 6, True),
    VendorPortalEntityType.ASN: ("ASN-", 6, True),
    VendorPortalEntityType.INVOICE_SUBMISSION: ("INV-", 6, True),
    VendorPortalEntityType.PAYMENT_STATUS: ("PAY-", 6, True),
    VendorPortalEntityType.DOCUMENT_ACCESS: ("DOC-", 6, True),
    VendorPortalEntityType.NOTIFICATION: ("NTF-", 6, True),
    VendorPortalEntityType.MESSAGE_THREAD: ("THR-", 6, True),
    VendorPortalEntityType.MESSAGE: ("MSG-", 6, True),
    VendorPortalEntityType.LOGIN_AUDIT: ("AUD-", 6, True),
}
