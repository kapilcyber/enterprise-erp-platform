"""BPM integration service — consume Foundation Security, Master Employee, Org, Analytics, Hub."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.bpm.adapters.analytics_port import BpmAnalyticsAdapter
from modules.bpm.adapters.foundation_port import BpmFoundationAdapter
from modules.bpm.adapters.integration_port import BpmIntegrationAdapter
from modules.bpm.adapters.master_data_port import BpmMasterDataAdapter
from modules.bpm.adapters.organization_port import BpmOrganizationAdapter
from modules.foundation.domain.value_objects import TenantContext


class BpmIntegrationService:
    def __init__(self, db: Session) -> None:
        self._master = BpmMasterDataAdapter(db)
        self._org = BpmOrganizationAdapter(db)
        self._foundation = BpmFoundationAdapter(db)
        self._analytics = BpmAnalyticsAdapter(db)
        self._integration = BpmIntegrationAdapter(db)

    def get_employee(self, ctx: TenantContext, employee_id: UUID):
        return self._master.get_employee(ctx, employee_id)

    def get_department(self, ctx: TenantContext, department_id: UUID):
        return self._org.get_department(ctx, department_id)

    def resolve_role_ref(self, ctx: TenantContext, role_id: UUID | None) -> UUID | None:
        return self._foundation.resolve_role_ref(ctx, role_id)

    def analytics_report_ref(
        self, ctx: TenantContext, bi_report_ref_id: UUID | None
    ) -> UUID | None:
        return self._analytics.resolve_report_ref(ctx, bi_report_ref_id)

    def integration_connector_ref(
        self, ctx: TenantContext, int_connector_id: UUID | None
    ) -> UUID | None:
        return self._integration.resolve_connector_ref(ctx, int_connector_id)
