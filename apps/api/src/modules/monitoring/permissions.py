"""Monitoring permissions — Phase 1–4 constants (seed not authorized / not implemented)."""

MONITORING_PERMISSION_NAMESPACE = "monitoring"
_MODULE = "monitoring"

_REGISTRY_ACTIONS = ("read", "create", "update", "archive", "restore", "admin")
_PUBLISHABLE_ACTIONS = (
    "read",
    "create",
    "update",
    "publish",
    "retire",
    "archive",
    "restore",
)
_ASSIGNMENT_ACTIONS = (
    "read",
    "create",
    "update",
    "activate",
    "deactivate",
    "retire",
    "archive",
    "restore",
)
_ACTIVATABLE_ACTIONS = (
    "read",
    "create",
    "update",
    "activate",
    "retire",
    "archive",
    "restore",
)
_REPORT_ACTIONS = (
    "read",
    "create",
    "update",
    "activate",
    "mark_archived",
    "archive",
    "restore",
)


def _perms(resource: str, actions: tuple[str, ...]) -> list[tuple[str, str, str, str]]:
    return [
        (
            f"{MONITORING_PERMISSION_NAMESPACE}.{resource}:{action}",
            f"{MONITORING_PERMISSION_NAMESPACE}.{resource}",
            action,
            _MODULE,
        )
        for action in actions
    ]


def _build_permissions() -> list[tuple[str, str, str, str]]:
    perms: list[tuple[str, str, str, str]] = []
    perms.extend(_perms("observability_policy", _REGISTRY_ACTIONS))
    perms.extend(_perms("observability_policy_version", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("monitored_service", _REGISTRY_ACTIONS))
    perms.extend(_perms("monitored_component", _REGISTRY_ACTIONS))
    perms.extend(_perms("metric_definition", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("health_check", _REGISTRY_ACTIONS))
    perms.extend(_perms("service_policy_assignment", _ASSIGNMENT_ACTIONS))
    perms.extend(_perms("log_trace_policy", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("alert_rule", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("alert_routing_policy", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("slo_definition", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("sli_definition", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("dashboard_definition", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("external_platform_binding", _ACTIVATABLE_ACTIONS))
    perms.extend(_perms("service_platform_assignment", _ASSIGNMENT_ACTIONS))
    perms.extend(_perms("signal_correlation", _ACTIVATABLE_ACTIONS))
    perms.extend(_perms("observability_report", _REPORT_ACTIONS))
    return perms


MONITORING_PERMISSIONS: list[tuple[str, str, str, str]] = _build_permissions()

PHASE1_PERMISSION_RESOURCES = (
    "observability_policy",
    "observability_policy_version",
    "monitored_service",
    "monitored_component",
    "metric_definition",
    "health_check",
    "service_policy_assignment",
)
MONITORING_PHASE1_PERMISSIONS = [
    p for p in MONITORING_PERMISSIONS if p[1].split(".")[-1] in PHASE1_PERMISSION_RESOURCES
]

PHASE2_PERMISSION_RESOURCES = (
    "log_trace_policy",
    "alert_rule",
    "alert_routing_policy",
)
MONITORING_PHASE2_PERMISSIONS = [
    p for p in MONITORING_PERMISSIONS if p[1].split(".")[-1] in PHASE2_PERMISSION_RESOURCES
]

PHASE3_PERMISSION_RESOURCES = (
    "slo_definition",
    "sli_definition",
    "dashboard_definition",
    "external_platform_binding",
    "service_platform_assignment",
    "signal_correlation",
)
MONITORING_PHASE3_PERMISSIONS = [
    p for p in MONITORING_PERMISSIONS if p[1].split(".")[-1] in PHASE3_PERMISSION_RESOURCES
]

PHASE4_PERMISSION_RESOURCES = ("observability_report",)
MONITORING_PHASE4_PERMISSIONS = [
    p for p in MONITORING_PERMISSIONS if p[1].split(".")[-1] in PHASE4_PERMISSION_RESOURCES
]
