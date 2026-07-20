"""Vendor Portal domain exceptions."""

from core.exceptions import ConflictException


class InvalidPortalAccountState(ConflictException):
    pass

class InvalidSupplierProfileState(ConflictException):
    pass

class InvalidPortalSessionState(ConflictException):
    pass

class InvalidDashboardState(ConflictException):
    pass

class InvalidDashboardWidgetState(ConflictException):
    pass

class InvalidRfqViewState(ConflictException):
    pass

class InvalidQuoteSubmissionState(ConflictException):
    pass

class InvalidPurchaseOrderViewState(ConflictException):
    pass

class InvalidPoAcknowledgementState(ConflictException):
    pass

class InvalidDeliveryScheduleState(ConflictException):
    pass

class InvalidAsnState(ConflictException):
    pass

class InvalidInvoiceSubmissionState(ConflictException):
    pass

class InvalidPaymentStatusState(ConflictException):
    pass

class InvalidDocumentAccessState(ConflictException):
    pass

class InvalidNotificationState(ConflictException):
    pass

class InvalidMessageThreadState(ConflictException):
    pass

class InvalidMessageState(ConflictException):
    pass

class InvalidPreferenceState(ConflictException):
    pass

class InvalidLoginAuditState(ConflictException):
    pass

class InvalidReportState(ConflictException):
    pass
