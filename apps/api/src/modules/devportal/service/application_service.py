"""API Developer Portal application façade — Phase 1."""

from sqlalchemy.orm import Session

from modules.devportal.service.api_product_environment_service import (
    ApiProductEnvironmentService,
)
from modules.devportal.service.api_product_service import ApiProductService
from modules.devportal.service.api_product_version_service import ApiProductVersionService
from modules.devportal.service.developer_account_service import DeveloperAccountService
from modules.devportal.service.developer_application_service import ApplicationService
from modules.devportal.service.developer_invite_service import DeveloperInviteService
from modules.devportal.service.developer_membership_service import DeveloperMembershipService
from modules.devportal.service.developer_organization_service import (
    DeveloperOrganizationService,
)
from modules.devportal.service.developer_team_service import DeveloperTeamService
from modules.devportal.service.documentation_entry_service import DocumentationEntryService
from modules.devportal.service.entitlement_service import EntitlementService
from modules.devportal.service.openapi_artifact_reference_service import (
    OpenapiArtifactReferenceService,
)
from modules.devportal.service.plan_service import PlanService
from modules.devportal.service.portal_report_service import PortalReportService
from modules.devportal.service.portal_session_service import PortalSessionService
from modules.devportal.service.publish_validation_service import PublishValidationService
from modules.devportal.service.sandbox_environment_service import SandboxEnvironmentService
from modules.devportal.service.subscription_service import SubscriptionService
from modules.devportal.service.tryit_session_service import TryitSessionService


class DevportalApplicationService:
    def __init__(self, db: Session) -> None:
        self.organizations = DeveloperOrganizationService(db)
        self.teams = DeveloperTeamService(db)
        self.accounts = DeveloperAccountService(db)
        self.memberships = DeveloperMembershipService(db)
        self.invites = DeveloperInviteService(db)
        self.sessions = PortalSessionService(db)
        self.applications = ApplicationService(db)
        self.api_products = ApiProductService(db)
        self.api_product_versions = ApiProductVersionService(db)
        self.api_product_environments = ApiProductEnvironmentService(db)
        self.plans = PlanService(db)
        self.subscriptions = SubscriptionService(db)
        self.entitlements = EntitlementService(db)
        self.documentation_entries = DocumentationEntryService(db)
        self.openapi_artifact_references = OpenapiArtifactReferenceService(db)
        self.sandbox_environments = SandboxEnvironmentService(db)
        self.tryit_sessions = TryitSessionService(db)
        self.reports = PortalReportService(db)
        self.publish_validation = PublishValidationService(db)
