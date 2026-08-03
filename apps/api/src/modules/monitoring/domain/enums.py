"""Monitoring domain enums — Phase 1."""

from enum import Enum


class PolicyScopeLevel(str, Enum):
    PLATFORM = "platform"
    TENANT = "tenant"
    COMPANY = "company"
    MODULE = "module"


POLICY_SCOPE_LEVEL_VALUES = tuple(s.value for s in PolicyScopeLevel)


class ObservabilityPolicyStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


OBSERVABILITY_POLICY_STATUS_VALUES = tuple(s.value for s in ObservabilityPolicyStatus)


class ObservabilityPolicyVersionStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"
    RETIRED = "retired"


OBSERVABILITY_POLICY_VERSION_STATUS_VALUES = tuple(
    s.value for s in ObservabilityPolicyVersionStatus
)


class EnvironmentClass(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    SANDBOX = "sandbox"


ENVIRONMENT_CLASS_VALUES = tuple(s.value for s in EnvironmentClass)


class MonitoredRegistryStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    RETIRED = "retired"


MONITORED_REGISTRY_STATUS_VALUES = tuple(s.value for s in MonitoredRegistryStatus)


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"
    OTHER = "other"


METRIC_TYPE_VALUES = tuple(s.value for s in MetricType)


class MetricDefinitionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


METRIC_DEFINITION_STATUS_VALUES = tuple(s.value for s in MetricDefinitionStatus)


class HealthCheckKind(str, Enum):
    HTTP = "http"
    TCP = "tcp"
    GRPC = "grpc"
    CUSTOM = "custom"
    OTHER = "other"


HEALTH_CHECK_KIND_VALUES = tuple(s.value for s in HealthCheckKind)


class HealthCheckStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


HEALTH_CHECK_STATUS_VALUES = tuple(s.value for s in HealthCheckStatus)


class AssignmentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    RETIRED = "retired"


ASSIGNMENT_STATUS_VALUES = tuple(s.value for s in AssignmentStatus)


class SignalKind(str, Enum):
    LOG = "log"
    TRACE = "trace"
    BOTH = "both"


SIGNAL_KIND_VALUES = tuple(s.value for s in SignalKind)


class LogTracePolicyStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


LOG_TRACE_POLICY_STATUS_VALUES = tuple(s.value for s in LogTracePolicyStatus)


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    FATAL = "fatal"


ALERT_SEVERITY_VALUES = tuple(s.value for s in AlertSeverity)


class AlertRuleStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"
    RETIRED = "retired"


ALERT_RULE_STATUS_VALUES = tuple(s.value for s in AlertRuleStatus)


class AlertRoutingPolicyStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"
    RETIRED = "retired"


ALERT_ROUTING_POLICY_STATUS_VALUES = tuple(s.value for s in AlertRoutingPolicyStatus)


class SloDefinitionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


SLO_DEFINITION_STATUS_VALUES = tuple(s.value for s in SloDefinitionStatus)


class SliDefinitionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


SLI_DEFINITION_STATUS_VALUES = tuple(s.value for s in SliDefinitionStatus)


class DashboardDefinitionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


DASHBOARD_DEFINITION_STATUS_VALUES = tuple(s.value for s in DashboardDefinitionStatus)


class PlatformType(str, Enum):
    PROMETHEUS = "prometheus"
    GRAFANA = "grafana"
    LOKI = "loki"
    OTEL = "otel"
    CLOUD_APM = "cloud_apm"
    SIEM = "siem"
    OTHER = "other"


PLATFORM_TYPE_VALUES = tuple(s.value for s in PlatformType)


class ExternalPlatformBindingStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    ACTIVE = "active"
    RETIRED = "retired"


EXTERNAL_PLATFORM_BINDING_STATUS_VALUES = tuple(
    s.value for s in ExternalPlatformBindingStatus
)


class SignalCorrelationStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


SIGNAL_CORRELATION_STATUS_VALUES = tuple(s.value for s in SignalCorrelationStatus)


class ReportKind(str, Enum):
    POLICY_COVERAGE = "policy_coverage"
    BINDING_STATUS = "binding_status"
    ALERT_INVENTORY = "alert_inventory"
    SLO_INVENTORY = "slo_inventory"
    OPERATIONAL = "operational"
    OTHER = "other"


REPORT_KIND_VALUES = tuple(s.value for s in ReportKind)


class ExportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    XLSX = "xlsx"
    PDF = "pdf"


EXPORT_FORMAT_VALUES = tuple(s.value for s in ExportFormat)


class ObservabilityReportStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


OBSERVABILITY_REPORT_STATUS_VALUES = tuple(s.value for s in ObservabilityReportStatus)
