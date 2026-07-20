"""Vendor Portal integration service — UUID peers only; Finance PostingService only."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.vendor_portal.adapters.analytics_port import VendorPortalAnalyticsAdapter
from modules.vendor_portal.adapters.document_port import VendorPortalDocumentAdapter
from modules.vendor_portal.adapters.finance_port import VendorPortalFinanceAdapter
from modules.vendor_portal.adapters.foundation_port import VendorPortalFoundationAdapter
from modules.vendor_portal.adapters.integration_port import VendorPortalIntegrationAdapter
from modules.vendor_portal.adapters.inventory_port import VendorPortalInventoryAdapter
from modules.vendor_portal.adapters.master_data_port import VendorPortalMasterDataAdapter
from modules.vendor_portal.adapters.organization_port import VendorPortalOrganizationAdapter
from modules.vendor_portal.adapters.procurement_port import VendorPortalProcurementAdapter
from modules.vendor_portal.adapters.quality_port import VendorPortalQualityAdapter


class VendorPortalIntegrationService:
    def __init__(self, db: Session) -> None:
        self.master = VendorPortalMasterDataAdapter(db)
        self.org = VendorPortalOrganizationAdapter(db)
        self.procurement = VendorPortalProcurementAdapter(db)
        self.inventory = VendorPortalInventoryAdapter(db)
        self.finance = VendorPortalFinanceAdapter(db)
        self.quality = VendorPortalQualityAdapter(db)
        self.document = VendorPortalDocumentAdapter(db)
        self.analytics = VendorPortalAnalyticsAdapter(db)
        self.integration = VendorPortalIntegrationAdapter(db)
        self.foundation = VendorPortalFoundationAdapter(db)

    def resolve_vendor(self, ctx: TenantContext, vendor_id: UUID):
        return self.master.get_vendor(ctx, vendor_id)

    def resolve_proc_rfq(self, ctx: TenantContext, rfq_id: UUID | None) -> UUID | None:
        return self.procurement.resolve_rfq_ref(ctx, rfq_id)

    def resolve_inventory_receipt(self, ctx: TenantContext, receipt_id: UUID | None) -> UUID | None:
        return self.inventory.resolve_receipt_ref(ctx, receipt_id)

    def resolve_quality_ncr(self, ctx: TenantContext, ncr_id: UUID | None) -> UUID | None:
        return self.quality.resolve_ncr_ref(ctx, ncr_id)

    def resolve_document(self, ctx: TenantContext, document_id: UUID | None) -> UUID | None:
        return self.document.resolve_document_uuid(ctx, document_id)
