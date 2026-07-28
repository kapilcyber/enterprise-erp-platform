"""API Developer Portal domain exceptions — Phase 1."""


class DevportalDomainError(Exception):
    """Base domain error for API Developer Portal."""


class InvalidDeveloperAccountState(DevportalDomainError):
    pass


class InvalidDeveloperInviteState(DevportalDomainError):
    pass


class InvalidPortalSessionState(DevportalDomainError):
    pass


class InvalidApplicationState(DevportalDomainError):
    pass


class InvalidApiProductVersionState(DevportalDomainError):
    pass


class PublishedApiProductVersionImmutable(DevportalDomainError):
    def __init__(self, message: str = "Published API product versions are immutable") -> None:
        super().__init__(message)


class HubBindingRequired(DevportalDomainError):
    pass


class InvalidPlanState(DevportalDomainError):
    pass


class PublishedPlanImmutable(DevportalDomainError):
    def __init__(self, message: str = "Published plans are immutable") -> None:
        super().__init__(message)


class InvalidSubscriptionState(DevportalDomainError):
    pass


class InvalidEntitlementState(DevportalDomainError):
    pass


class SubscriptionBindingError(DevportalDomainError):
    pass


class InvalidDocumentationEntryState(DevportalDomainError):
    pass


class PublishedDocumentationImmutable(DevportalDomainError):
    def __init__(self, message: str = "Published documentation entries are immutable") -> None:
        super().__init__(message)


class InvalidOpenApiArtifactState(DevportalDomainError):
    pass


class InvalidSandboxEnvironmentState(DevportalDomainError):
    pass


class InvalidTryitSessionState(DevportalDomainError):
    pass


class TryitInvokeForbidden(DevportalDomainError):
    def __init__(
        self,
        message: str = "Try-it sessions are metadata only — live API invoke is forbidden",
    ) -> None:
        super().__init__(message)


class DocumentationEntryTypeError(DevportalDomainError):
    pass


class InvalidPortalReportState(DevportalDomainError):
    pass


class PortalReportTypeError(DevportalDomainError):
    pass


class PortalReportProjectionStale(DevportalDomainError):
    def __init__(
        self,
        message: str = "Portal report Hub usage projection is missing or stale",
    ) -> None:
        super().__init__(message)


class AnalyticsWarehouseForbidden(DevportalDomainError):
    def __init__(
        self,
        message: str = (
            "Developer Portal owns operational report metadata only — "
            "Analytics remains the enterprise reporting SoR"
        ),
    ) -> None:
        super().__init__(message)
