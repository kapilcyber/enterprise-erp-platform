"""API Developer Portal domain enums — Phase 1–3."""

from enum import Enum


class DeveloperAccountStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    ACTIVE = "active"
    LOCKED = "locked"
    SUSPENDED = "suspended"
    RETIRED = "retired"


DEVELOPER_ACCOUNT_STATUS_VALUES = tuple(s.value for s in DeveloperAccountStatus)


class DeveloperInviteStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    SENT = "sent"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
    REVOKED = "revoked"


DEVELOPER_INVITE_STATUS_VALUES = tuple(s.value for s in DeveloperInviteStatus)


class PortalSessionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


PORTAL_SESSION_STATUS_VALUES = tuple(s.value for s in PortalSessionStatus)


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"


APPLICATION_STATUS_VALUES = tuple(s.value for s in ApplicationStatus)


class ApiProductVersionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


API_PRODUCT_VERSION_STATUS_VALUES = tuple(s.value for s in ApiProductVersionStatus)


class RegistryStatus(str, Enum):
    ACTIVE = "active"
    RETIRED = "retired"


REGISTRY_STATUS_VALUES = tuple(s.value for s in RegistryStatus)


class MembershipStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"


MEMBERSHIP_STATUS_VALUES = tuple(s.value for s in MembershipStatus)


class PlanStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


PLAN_STATUS_VALUES = tuple(s.value for s in PlanStatus)


class SubscriptionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"


SUBSCRIPTION_STATUS_VALUES = tuple(s.value for s in SubscriptionStatus)


class EntitlementStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"


ENTITLEMENT_STATUS_VALUES = tuple(s.value for s in EntitlementStatus)


class DocumentationEntryType(str, Enum):
    GUIDE = "guide"
    TUTORIAL = "tutorial"
    CHANGELOG = "changelog"
    RELEASE_NOTES = "release_notes"


DOCUMENTATION_ENTRY_TYPE_VALUES = tuple(t.value for t in DocumentationEntryType)


class DocumentationEntryStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


DOCUMENTATION_ENTRY_STATUS_VALUES = tuple(s.value for s in DocumentationEntryStatus)


class OpenApiArtifactStatus(str, Enum):
    ACTIVE = "active"
    RETIRED = "retired"


OPENAPI_ARTIFACT_STATUS_VALUES = tuple(s.value for s in OpenApiArtifactStatus)


class SandboxEnvironmentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


SANDBOX_ENVIRONMENT_STATUS_VALUES = tuple(s.value for s in SandboxEnvironmentStatus)


class TryitSessionStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    EXPIRED = "expired"


TRYIT_SESSION_STATUS_VALUES = tuple(s.value for s in TryitSessionStatus)


class PortalReportType(str, Enum):
    ACTIVE_DEVELOPERS = "active_developers"
    APPLICATIONS = "applications"
    SUBSCRIPTIONS = "subscriptions"
    CATALOG_PUBLISHES = "catalog_publishes"
    SESSION_METRICS = "session_metrics"
    HUB_USAGE = "hub_usage"


PORTAL_REPORT_TYPE_VALUES = tuple(t.value for t in PortalReportType)


class PortalReportStatus(str, Enum):
    DRAFT = "draft"
    FINALIZED = "finalized"
    RETIRED = "retired"


PORTAL_REPORT_STATUS_VALUES = tuple(s.value for s in PortalReportStatus)
