"""Vendor Portal Pydantic schemas."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class PortalAccountCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class PortalAccountUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class PortalAccountResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class SupplierProfileCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class SupplierProfileUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class SupplierProfileResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class PortalSessionCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class PortalSessionUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class PortalSessionResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class DashboardCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class DashboardUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class DashboardResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class DashboardWidgetCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class DashboardWidgetUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class DashboardWidgetResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class RfqViewCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class RfqViewUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class RfqViewResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class QuoteSubmissionCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class QuoteSubmissionUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class QuoteSubmissionResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class PurchaseOrderViewCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class PurchaseOrderViewUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class PurchaseOrderViewResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class PoAcknowledgementCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class PoAcknowledgementUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class PoAcknowledgementResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class DeliveryScheduleCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class DeliveryScheduleUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class DeliveryScheduleResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class AsnCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class AsnUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class AsnResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class InvoiceSubmissionCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class InvoiceSubmissionUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class InvoiceSubmissionResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class PaymentStatusCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class PaymentStatusUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class PaymentStatusResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class DocumentAccessCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class DocumentAccessUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class DocumentAccessResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class NotificationCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class NotificationUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class NotificationResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class MessageThreadCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class MessageThreadUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class MessageThreadResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class MessageCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class MessageUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class MessageResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class PreferenceCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class PreferenceUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class PreferenceResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class LoginAuditCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class LoginAuditUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class LoginAuditResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int

class ReportCreate(BaseModel):
    company_id: UUID | None = None
    status: str | None = None

class ReportUpdate(BaseModel):
    status: str | None = None
    version: int | None = None

class ReportResponse(OrmModel):
    id: UUID
    company_id: UUID
    status: str
    version: int
