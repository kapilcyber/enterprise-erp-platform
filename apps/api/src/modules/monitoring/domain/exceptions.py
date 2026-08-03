"""Monitoring domain exceptions — Phase 1."""

from core.exceptions import ConflictException


class MonitoringDomainError(Exception):
    """Base domain error for Monitoring / Observability."""


class MonitoringConflict(ConflictException):
    def __init__(self, message: str = "Monitoring conflict") -> None:
        super().__init__(message)


class TelemetrySoRForbidden(MonitoringDomainError):
    def __init__(
        self,
        message: str = (
            "Monitoring owns observability metadata / control-plane only — "
            "external platforms remain the telemetry SoR"
        ),
    ) -> None:
        super().__init__(message)


class SecretMaterializationForbidden(MonitoringDomainError):
    def __init__(
        self,
        message: str = "External platform secret materialization is forbidden — secret_ref only",
    ) -> None:
        super().__init__(message)


class InvalidObservabilityPolicyVersionState(MonitoringConflict):
    def __init__(self, message: str = "Invalid observability policy version state") -> None:
        super().__init__(message)


class PublishedObservabilityPolicyVersionImmutable(MonitoringConflict):
    def __init__(
        self, message: str = "Published observability policy versions are immutable"
    ) -> None:
        super().__init__(message)


class InvalidMetricDefinitionState(MonitoringConflict):
    def __init__(self, message: str = "Invalid metric definition state") -> None:
        super().__init__(message)


class PublishedMetricDefinitionImmutable(MonitoringConflict):
    def __init__(self, message: str = "Published metric definitions are immutable") -> None:
        super().__init__(message)


class InvalidAssignmentState(MonitoringConflict):
    def __init__(self, message: str = "Invalid service policy assignment state") -> None:
        super().__init__(message)


class InvalidLogTracePolicyState(MonitoringConflict):
    def __init__(self, message: str = "Invalid log/trace policy state") -> None:
        super().__init__(message)


class PublishedLogTracePolicyImmutable(MonitoringConflict):
    def __init__(self, message: str = "Published log/trace policies are immutable") -> None:
        super().__init__(message)


class InvalidAlertRuleState(MonitoringConflict):
    def __init__(self, message: str = "Invalid alert rule state") -> None:
        super().__init__(message)


class PublishedAlertRuleImmutable(MonitoringConflict):
    def __init__(self, message: str = "Published alert rules are immutable") -> None:
        super().__init__(message)


class InvalidAlertRoutingPolicyState(MonitoringConflict):
    def __init__(self, message: str = "Invalid alert routing policy state") -> None:
        super().__init__(message)


class PublishedAlertRoutingPolicyImmutable(MonitoringConflict):
    def __init__(self, message: str = "Published alert routing policies are immutable") -> None:
        super().__init__(message)


class InvalidSloDefinitionState(MonitoringConflict):
    def __init__(self, message: str = "Invalid SLO definition state") -> None:
        super().__init__(message)


class PublishedSloDefinitionImmutable(MonitoringConflict):
    def __init__(self, message: str = "Published SLO definitions are immutable") -> None:
        super().__init__(message)


class InvalidSliDefinitionState(MonitoringConflict):
    def __init__(self, message: str = "Invalid SLI definition state") -> None:
        super().__init__(message)


class PublishedSliDefinitionImmutable(MonitoringConflict):
    def __init__(self, message: str = "Published SLI definitions are immutable") -> None:
        super().__init__(message)


class InvalidDashboardDefinitionState(MonitoringConflict):
    def __init__(self, message: str = "Invalid dashboard definition state") -> None:
        super().__init__(message)


class PublishedDashboardDefinitionImmutable(MonitoringConflict):
    def __init__(self, message: str = "Published dashboard definitions are immutable") -> None:
        super().__init__(message)


class InvalidExternalPlatformBindingState(MonitoringConflict):
    def __init__(self, message: str = "Invalid external platform binding state") -> None:
        super().__init__(message)


class ActiveExternalPlatformBindingImmutable(MonitoringConflict):
    def __init__(self, message: str = "Active external platform bindings are immutable") -> None:
        super().__init__(message)


class InvalidSignalCorrelationState(MonitoringConflict):
    def __init__(self, message: str = "Invalid signal correlation state") -> None:
        super().__init__(message)


class ActiveSignalCorrelationImmutable(MonitoringConflict):
    def __init__(self, message: str = "Active signal correlations are immutable") -> None:
        super().__init__(message)


class InvalidObservabilityReportState(MonitoringConflict):
    def __init__(self, message: str = "Invalid observability report state") -> None:
        super().__init__(message)


class ActiveObservabilityReportImmutable(MonitoringConflict):
    def __init__(self, message: str = "Active observability reports are immutable") -> None:
        super().__init__(message)
