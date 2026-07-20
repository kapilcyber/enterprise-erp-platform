"""Vendor Portal API route handlers."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.vendor_portal.dependencies import (
    PaginationParams,
    extract_update_fields,
    get_db,
    get_pagination,
    paginate,
    require_permission,
)
from modules.vendor_portal.schemas import (
    AsnCreate,
    AsnResponse,
    AsnUpdate,
    DashboardCreate,
    DashboardResponse,
    DashboardUpdate,
    DashboardWidgetCreate,
    DashboardWidgetResponse,
    DashboardWidgetUpdate,
    DeliveryScheduleCreate,
    DeliveryScheduleResponse,
    DeliveryScheduleUpdate,
    DocumentAccessCreate,
    DocumentAccessResponse,
    DocumentAccessUpdate,
    InvoiceSubmissionCreate,
    InvoiceSubmissionResponse,
    InvoiceSubmissionUpdate,
    LoginAuditCreate,
    LoginAuditResponse,
    LoginAuditUpdate,
    MessageCreate,
    MessageResponse,
    MessageThreadCreate,
    MessageThreadResponse,
    MessageThreadUpdate,
    MessageUpdate,
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
    PaymentStatusCreate,
    PaymentStatusResponse,
    PaymentStatusUpdate,
    PoAcknowledgementCreate,
    PoAcknowledgementResponse,
    PoAcknowledgementUpdate,
    PortalAccountCreate,
    PortalAccountResponse,
    PortalAccountUpdate,
    PortalSessionCreate,
    PortalSessionResponse,
    PortalSessionUpdate,
    PreferenceCreate,
    PreferenceResponse,
    PreferenceUpdate,
    PurchaseOrderViewCreate,
    PurchaseOrderViewResponse,
    PurchaseOrderViewUpdate,
    QuoteSubmissionCreate,
    QuoteSubmissionResponse,
    QuoteSubmissionUpdate,
    ReportCreate,
    ReportResponse,
    ReportUpdate,
    RfqViewCreate,
    RfqViewResponse,
    RfqViewUpdate,
    SupplierProfileCreate,
    SupplierProfileResponse,
    SupplierProfileUpdate,
)
from modules.vendor_portal.service import (
    AsnService,
    DashboardService,
    DashboardWidgetService,
    DeliveryScheduleService,
    DocumentAccessService,
    InvoiceSubmissionService,
    LoginAuditService,
    MessageService,
    MessageThreadService,
    NotificationService,
    PaymentStatusService,
    PoAcknowledgementService,
    PortalAccountService,
    PortalSessionService,
    PreferenceService,
    PurchaseOrderViewService,
    QuoteSubmissionService,
    ReportService,
    RfqViewService,
    SupplierProfileService,
)
from shared.schemas import APIResponse

portal_account_router = APIRouter(prefix="/portal-accounts", tags=["Vendor Portal — PortalAccount"])

@portal_account_router.get("", response_model=APIResponse[list[PortalAccountResponse]])
def list_portal_account(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.account:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = PortalAccountService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@portal_account_router.get("/{row_id}", response_model=APIResponse[PortalAccountResponse])
def get_portal_account(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.account:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PortalAccountService(db).get(ctx, row_id))

@portal_account_router.post("", response_model=APIResponse[PortalAccountResponse])
def create_portal_account(
    body: PortalAccountCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.account:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=PortalAccountService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@portal_account_router.patch("/{row_id}", response_model=APIResponse[PortalAccountResponse])
def update_portal_account(
    row_id: UUID,
    body: PortalAccountUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.account:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=PortalAccountService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

@portal_account_router.post("/{row_id}/submit", response_model=APIResponse[PortalAccountResponse])
def submit_portal_account(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.account:submit"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="submit", data=PortalAccountService(db).submit(ctx, row_id))

@portal_account_router.post("/{row_id}/approve", response_model=APIResponse[PortalAccountResponse])
def approve_portal_account(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.account:approve"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="approve", data=PortalAccountService(db).approve(ctx, row_id))

supplier_profile_router = APIRouter(prefix="/supplier-profiles", tags=["Vendor Portal — SupplierProfile"])  # noqa: E501

@supplier_profile_router.get("", response_model=APIResponse[list[SupplierProfileResponse]])
def list_supplier_profile(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.profile:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = SupplierProfileService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@supplier_profile_router.get("/{row_id}", response_model=APIResponse[SupplierProfileResponse])
def get_supplier_profile(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.profile:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=SupplierProfileService(db).get(ctx, row_id))

@supplier_profile_router.post("", response_model=APIResponse[SupplierProfileResponse])
def create_supplier_profile(
    body: SupplierProfileCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.profile:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=SupplierProfileService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@supplier_profile_router.patch("/{row_id}", response_model=APIResponse[SupplierProfileResponse])
def update_supplier_profile(
    row_id: UUID,
    body: SupplierProfileUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.profile:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=SupplierProfileService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

@supplier_profile_router.post("/{row_id}/submit", response_model=APIResponse[SupplierProfileResponse])  # noqa: E501
def submit_supplier_profile(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.profile:submit"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="submit", data=SupplierProfileService(db).submit(ctx, row_id))

@supplier_profile_router.post("/{row_id}/approve", response_model=APIResponse[SupplierProfileResponse])  # noqa: E501
def approve_supplier_profile(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.profile:approve"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="approve", data=SupplierProfileService(db).approve(ctx, row_id))

portal_session_router = APIRouter(prefix="/portal-sessions", tags=["Vendor Portal — PortalSession"])

@portal_session_router.get("", response_model=APIResponse[list[PortalSessionResponse]])
def list_portal_session(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.session:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = PortalSessionService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@portal_session_router.get("/{row_id}", response_model=APIResponse[PortalSessionResponse])
def get_portal_session(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.session:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PortalSessionService(db).get(ctx, row_id))

@portal_session_router.post("", response_model=APIResponse[PortalSessionResponse])
def create_portal_session(
    body: PortalSessionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.session:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=PortalSessionService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@portal_session_router.patch("/{row_id}", response_model=APIResponse[PortalSessionResponse])
def update_portal_session(
    row_id: UUID,
    body: PortalSessionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.session:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=PortalSessionService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

dashboard_router = APIRouter(prefix="/dashboards", tags=["Vendor Portal — Dashboard"])

@dashboard_router.get("", response_model=APIResponse[list[DashboardResponse]])
def list_dashboard(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.dashboard:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = DashboardService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@dashboard_router.get("/{row_id}", response_model=APIResponse[DashboardResponse])
def get_dashboard(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.dashboard:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=DashboardService(db).get(ctx, row_id))

@dashboard_router.post("", response_model=APIResponse[DashboardResponse])
def create_dashboard(
    body: DashboardCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.dashboard:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=DashboardService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@dashboard_router.patch("/{row_id}", response_model=APIResponse[DashboardResponse])
def update_dashboard(
    row_id: UUID,
    body: DashboardUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.dashboard:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=DashboardService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

dashboard_widget_router = APIRouter(prefix="/dashboard-widgets", tags=["Vendor Portal — DashboardWidget"])  # noqa: E501

@dashboard_widget_router.get("", response_model=APIResponse[list[DashboardWidgetResponse]])
def list_dashboard_widget(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.widget:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = DashboardWidgetService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@dashboard_widget_router.get("/{row_id}", response_model=APIResponse[DashboardWidgetResponse])
def get_dashboard_widget(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.widget:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=DashboardWidgetService(db).get(ctx, row_id))

@dashboard_widget_router.post("", response_model=APIResponse[DashboardWidgetResponse])
def create_dashboard_widget(
    body: DashboardWidgetCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.widget:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=DashboardWidgetService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@dashboard_widget_router.patch("/{row_id}", response_model=APIResponse[DashboardWidgetResponse])
def update_dashboard_widget(
    row_id: UUID,
    body: DashboardWidgetUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.widget:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=DashboardWidgetService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

rfq_view_router = APIRouter(prefix="/rfq-views", tags=["Vendor Portal — RfqView"])

@rfq_view_router.get("", response_model=APIResponse[list[RfqViewResponse]])
def list_rfq_view(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.rfq_view:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = RfqViewService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@rfq_view_router.get("/{row_id}", response_model=APIResponse[RfqViewResponse])
def get_rfq_view(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.rfq_view:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=RfqViewService(db).get(ctx, row_id))

@rfq_view_router.post("", response_model=APIResponse[RfqViewResponse])
def create_rfq_view(
    body: RfqViewCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.rfq_view:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=RfqViewService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@rfq_view_router.patch("/{row_id}", response_model=APIResponse[RfqViewResponse])
def update_rfq_view(
    row_id: UUID,
    body: RfqViewUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.rfq_view:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=RfqViewService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

quote_submission_router = APIRouter(prefix="/quote-submissions", tags=["Vendor Portal — QuoteSubmission"])  # noqa: E501

@quote_submission_router.get("", response_model=APIResponse[list[QuoteSubmissionResponse]])
def list_quote_submission(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.quote_submission:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = QuoteSubmissionService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@quote_submission_router.get("/{row_id}", response_model=APIResponse[QuoteSubmissionResponse])
def get_quote_submission(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.quote_submission:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=QuoteSubmissionService(db).get(ctx, row_id))

@quote_submission_router.post("", response_model=APIResponse[QuoteSubmissionResponse])
def create_quote_submission(
    body: QuoteSubmissionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.quote_submission:create"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=QuoteSubmissionService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@quote_submission_router.patch("/{row_id}", response_model=APIResponse[QuoteSubmissionResponse])
def update_quote_submission(
    row_id: UUID,
    body: QuoteSubmissionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.quote_submission:update"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=QuoteSubmissionService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

@quote_submission_router.post("/{row_id}/submit", response_model=APIResponse[QuoteSubmissionResponse])  # noqa: E501
def submit_quote_submission(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.quote_submission:submit"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="submit", data=QuoteSubmissionService(db).submit(ctx, row_id))

@quote_submission_router.post("/{row_id}/approve", response_model=APIResponse[QuoteSubmissionResponse])  # noqa: E501
def approve_quote_submission(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.quote_submission:approve"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="approve", data=QuoteSubmissionService(db).approve(ctx, row_id))

purchase_order_view_router = APIRouter(prefix="/purchase-order-views", tags=["Vendor Portal — PurchaseOrderView"])  # noqa: E501

@purchase_order_view_router.get("", response_model=APIResponse[list[PurchaseOrderViewResponse]])
def list_purchase_order_view(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.purchase_order_view:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = PurchaseOrderViewService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@purchase_order_view_router.get("/{row_id}", response_model=APIResponse[PurchaseOrderViewResponse])
def get_purchase_order_view(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.purchase_order_view:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PurchaseOrderViewService(db).get(ctx, row_id))

@purchase_order_view_router.post("", response_model=APIResponse[PurchaseOrderViewResponse])
def create_purchase_order_view(
    body: PurchaseOrderViewCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.purchase_order_view:create"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=PurchaseOrderViewService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@purchase_order_view_router.patch("/{row_id}", response_model=APIResponse[PurchaseOrderViewResponse])  # noqa: E501
def update_purchase_order_view(
    row_id: UUID,
    body: PurchaseOrderViewUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.purchase_order_view:update"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=PurchaseOrderViewService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

po_acknowledgement_router = APIRouter(prefix="/po-acknowledgements", tags=["Vendor Portal — PoAcknowledgement"])  # noqa: E501

@po_acknowledgement_router.get("", response_model=APIResponse[list[PoAcknowledgementResponse]])
def list_po_acknowledgement(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.po_acknowledgement:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = PoAcknowledgementService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@po_acknowledgement_router.get("/{row_id}", response_model=APIResponse[PoAcknowledgementResponse])
def get_po_acknowledgement(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.po_acknowledgement:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PoAcknowledgementService(db).get(ctx, row_id))

@po_acknowledgement_router.post("", response_model=APIResponse[PoAcknowledgementResponse])
def create_po_acknowledgement(
    body: PoAcknowledgementCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.po_acknowledgement:create"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=PoAcknowledgementService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@po_acknowledgement_router.patch("/{row_id}", response_model=APIResponse[PoAcknowledgementResponse])
def update_po_acknowledgement(
    row_id: UUID,
    body: PoAcknowledgementUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.po_acknowledgement:update"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=PoAcknowledgementService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

@po_acknowledgement_router.post("/{row_id}/submit", response_model=APIResponse[PoAcknowledgementResponse])  # noqa: E501
def submit_po_acknowledgement(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.po_acknowledgement:submit"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="submit", data=PoAcknowledgementService(db).submit(ctx, row_id))

@po_acknowledgement_router.post("/{row_id}/approve", response_model=APIResponse[PoAcknowledgementResponse])  # noqa: E501
def approve_po_acknowledgement(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.po_acknowledgement:approve"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="approve", data=PoAcknowledgementService(db).approve(ctx, row_id))

delivery_schedule_router = APIRouter(prefix="/delivery-schedules", tags=["Vendor Portal — DeliverySchedule"])  # noqa: E501

@delivery_schedule_router.get("", response_model=APIResponse[list[DeliveryScheduleResponse]])
def list_delivery_schedule(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.delivery_schedule:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = DeliveryScheduleService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@delivery_schedule_router.get("/{row_id}", response_model=APIResponse[DeliveryScheduleResponse])
def get_delivery_schedule(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.delivery_schedule:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=DeliveryScheduleService(db).get(ctx, row_id))

@delivery_schedule_router.post("", response_model=APIResponse[DeliveryScheduleResponse])
def create_delivery_schedule(
    body: DeliveryScheduleCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.delivery_schedule:create"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=DeliveryScheduleService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@delivery_schedule_router.patch("/{row_id}", response_model=APIResponse[DeliveryScheduleResponse])
def update_delivery_schedule(
    row_id: UUID,
    body: DeliveryScheduleUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.delivery_schedule:update"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=DeliveryScheduleService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

asn_router = APIRouter(prefix="/asns", tags=["Vendor Portal — Asn"])

@asn_router.get("", response_model=APIResponse[list[AsnResponse]])
def list_asn(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.asn:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = AsnService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@asn_router.get("/{row_id}", response_model=APIResponse[AsnResponse])
def get_asn(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.asn:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=AsnService(db).get(ctx, row_id))

@asn_router.post("", response_model=APIResponse[AsnResponse])
def create_asn(
    body: AsnCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.asn:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=AsnService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@asn_router.patch("/{row_id}", response_model=APIResponse[AsnResponse])
def update_asn(
    row_id: UUID,
    body: AsnUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.asn:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=AsnService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

@asn_router.post("/{row_id}/submit", response_model=APIResponse[AsnResponse])
def submit_asn(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.asn:submit"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="submit", data=AsnService(db).submit(ctx, row_id))

@asn_router.post("/{row_id}/approve", response_model=APIResponse[AsnResponse])
def approve_asn(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.asn:approve"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="approve", data=AsnService(db).approve(ctx, row_id))

invoice_submission_router = APIRouter(prefix="/invoice-submissions", tags=["Vendor Portal — InvoiceSubmission"])  # noqa: E501

@invoice_submission_router.get("", response_model=APIResponse[list[InvoiceSubmissionResponse]])
def list_invoice_submission(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.invoice_submission:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = InvoiceSubmissionService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@invoice_submission_router.get("/{row_id}", response_model=APIResponse[InvoiceSubmissionResponse])
def get_invoice_submission(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.invoice_submission:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=InvoiceSubmissionService(db).get(ctx, row_id))

@invoice_submission_router.post("", response_model=APIResponse[InvoiceSubmissionResponse])
def create_invoice_submission(
    body: InvoiceSubmissionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.invoice_submission:create"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=InvoiceSubmissionService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@invoice_submission_router.patch("/{row_id}", response_model=APIResponse[InvoiceSubmissionResponse])
def update_invoice_submission(
    row_id: UUID,
    body: InvoiceSubmissionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.invoice_submission:update"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=InvoiceSubmissionService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

@invoice_submission_router.post("/{row_id}/submit", response_model=APIResponse[InvoiceSubmissionResponse])  # noqa: E501
def submit_invoice_submission(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.invoice_submission:submit"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="submit", data=InvoiceSubmissionService(db).submit(ctx, row_id))

@invoice_submission_router.post("/{row_id}/approve", response_model=APIResponse[InvoiceSubmissionResponse])  # noqa: E501
def approve_invoice_submission(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.invoice_submission:approve"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="approve", data=InvoiceSubmissionService(db).approve(ctx, row_id))

payment_status_router = APIRouter(prefix="/payment-statuses", tags=["Vendor Portal — PaymentStatus"])  # noqa: E501

@payment_status_router.get("", response_model=APIResponse[list[PaymentStatusResponse]])
def list_payment_status(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.payment_status:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = PaymentStatusService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@payment_status_router.get("/{row_id}", response_model=APIResponse[PaymentStatusResponse])
def get_payment_status(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.payment_status:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PaymentStatusService(db).get(ctx, row_id))

@payment_status_router.post("", response_model=APIResponse[PaymentStatusResponse])
def create_payment_status(
    body: PaymentStatusCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.payment_status:create"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=PaymentStatusService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@payment_status_router.patch("/{row_id}", response_model=APIResponse[PaymentStatusResponse])
def update_payment_status(
    row_id: UUID,
    body: PaymentStatusUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.payment_status:update"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=PaymentStatusService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

document_access_router = APIRouter(prefix="/document-accesses", tags=["Vendor Portal — DocumentAccess"])  # noqa: E501

@document_access_router.get("", response_model=APIResponse[list[DocumentAccessResponse]])
def list_document_access(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.document_access:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = DocumentAccessService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@document_access_router.get("/{row_id}", response_model=APIResponse[DocumentAccessResponse])
def get_document_access(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.document_access:read"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=DocumentAccessService(db).get(ctx, row_id))

@document_access_router.post("", response_model=APIResponse[DocumentAccessResponse])
def create_document_access(
    body: DocumentAccessCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.document_access:create"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=DocumentAccessService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@document_access_router.patch("/{row_id}", response_model=APIResponse[DocumentAccessResponse])
def update_document_access(
    row_id: UUID,
    body: DocumentAccessUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.document_access:update"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=DocumentAccessService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

@document_access_router.post("/{row_id}/submit", response_model=APIResponse[DocumentAccessResponse])
def submit_document_access(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.document_access:submit"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="submit", data=DocumentAccessService(db).submit(ctx, row_id))

@document_access_router.post("/{row_id}/approve", response_model=APIResponse[DocumentAccessResponse])  # noqa: E501
def approve_document_access(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.document_access:approve"))],  # noqa: E501
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="approve", data=DocumentAccessService(db).approve(ctx, row_id))

notification_router = APIRouter(prefix="/notifications", tags=["Vendor Portal — Notification"])

@notification_router.get("", response_model=APIResponse[list[NotificationResponse]])
def list_notification(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.notification:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = NotificationService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@notification_router.get("/{row_id}", response_model=APIResponse[NotificationResponse])
def get_notification(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.notification:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=NotificationService(db).get(ctx, row_id))

@notification_router.post("", response_model=APIResponse[NotificationResponse])
def create_notification(
    body: NotificationCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.notification:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=NotificationService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@notification_router.patch("/{row_id}", response_model=APIResponse[NotificationResponse])
def update_notification(
    row_id: UUID,
    body: NotificationUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.notification:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=NotificationService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

message_thread_router = APIRouter(prefix="/message-threads", tags=["Vendor Portal — MessageThread"])

@message_thread_router.get("", response_model=APIResponse[list[MessageThreadResponse]])
def list_message_thread(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.thread:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = MessageThreadService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@message_thread_router.get("/{row_id}", response_model=APIResponse[MessageThreadResponse])
def get_message_thread(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.thread:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=MessageThreadService(db).get(ctx, row_id))

@message_thread_router.post("", response_model=APIResponse[MessageThreadResponse])
def create_message_thread(
    body: MessageThreadCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.thread:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=MessageThreadService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@message_thread_router.patch("/{row_id}", response_model=APIResponse[MessageThreadResponse])
def update_message_thread(
    row_id: UUID,
    body: MessageThreadUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.thread:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=MessageThreadService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

message_router = APIRouter(prefix="/messages", tags=["Vendor Portal — Message"])

@message_router.get("", response_model=APIResponse[list[MessageResponse]])
def list_message(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.message:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = MessageService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@message_router.get("/{row_id}", response_model=APIResponse[MessageResponse])
def get_message(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.message:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=MessageService(db).get(ctx, row_id))

@message_router.post("", response_model=APIResponse[MessageResponse])
def create_message(
    body: MessageCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.message:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=MessageService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@message_router.patch("/{row_id}", response_model=APIResponse[MessageResponse])
def update_message(
    row_id: UUID,
    body: MessageUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.message:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=MessageService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

preference_router = APIRouter(prefix="/preferences", tags=["Vendor Portal — Preference"])

@preference_router.get("", response_model=APIResponse[list[PreferenceResponse]])
def list_preference(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.preference:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = PreferenceService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@preference_router.get("/{row_id}", response_model=APIResponse[PreferenceResponse])
def get_preference(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.preference:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PreferenceService(db).get(ctx, row_id))

@preference_router.post("", response_model=APIResponse[PreferenceResponse])
def create_preference(
    body: PreferenceCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.preference:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=PreferenceService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@preference_router.patch("/{row_id}", response_model=APIResponse[PreferenceResponse])
def update_preference(
    row_id: UUID,
    body: PreferenceUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.preference:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=PreferenceService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

login_audit_router = APIRouter(prefix="/login-audits", tags=["Vendor Portal — LoginAudit"])

@login_audit_router.get("", response_model=APIResponse[list[LoginAuditResponse]])
def list_login_audit(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.login_audit:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = LoginAuditService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@login_audit_router.get("/{row_id}", response_model=APIResponse[LoginAuditResponse])
def get_login_audit(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.login_audit:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=LoginAuditService(db).get(ctx, row_id))

@login_audit_router.post("", response_model=APIResponse[LoginAuditResponse])
def create_login_audit(
    body: LoginAuditCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.login_audit:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=LoginAuditService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@login_audit_router.patch("/{row_id}", response_model=APIResponse[LoginAuditResponse])
def update_login_audit(
    row_id: UUID,
    body: LoginAuditUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.login_audit:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=LoginAuditService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501

report_router = APIRouter(prefix="/reports", tags=["Vendor Portal — Report"])

@report_router.get("", response_model=APIResponse[list[ReportResponse]])
def list_report(
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.report:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    company_id: UUID | None = None,
):
    items = ReportService(db).list(ctx, company_id=company_id)
    return APIResponse(message="OK", data=paginate(items, pagination))

@report_router.get("/{row_id}", response_model=APIResponse[ReportResponse])
def get_report(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.report:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=ReportService(db).get(ctx, row_id))

@report_router.post("", response_model=APIResponse[ReportResponse])
def create_report(
    body: ReportCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.report:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Created", data=ReportService(db).create(ctx, **body.model_dump(exclude_none=True)))  # noqa: E501

@report_router.patch("/{row_id}", response_model=APIResponse[ReportResponse])
def update_report(
    row_id: UUID,
    body: ReportUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("vendor_portal.report:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Updated", data=ReportService(db).update(ctx, row_id, **extract_update_fields(body)))  # noqa: E501
