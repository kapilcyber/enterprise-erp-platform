"""API Developer Portal permissions — Phase 1–4."""

DEVPORTAL_PERMISSION_NAMESPACE = "devportal"
_MODULE = "devportal"

_REGISTRY_ACTIONS = ("read", "create", "update", "archive", "restore", "admin")
_APPROVAL_ACTIONS = (
    "read",
    "create",
    "update",
    "submit",
    "approve",
    "archive",
    "restore",
    "admin",
)
_ACCOUNT_ACTIONS = _APPROVAL_ACTIONS + ("activate", "lock", "suspend", "retire")
_APPLICATION_ACTIONS = _APPROVAL_ACTIONS + ("activate", "suspend", "retire", "bind")
_INVITE_ACTIONS = _APPROVAL_ACTIONS + ("send", "accept", "expire", "revoke")
_SESSION_ACTIONS = ("read", "create", "update", "expire", "revoke", "archive", "restore")
_PUBLISHABLE_ACTIONS = (
    "read",
    "create",
    "update",
    "publish",
    "retire",
    "validate",
    "archive",
    "restore",
)
_SUBSCRIPTION_ACTIONS = _APPROVAL_ACTIONS + ("activate", "suspend", "retire")
_ENTITLEMENT_ACTIONS = (
    "read",
    "create",
    "update",
    "activate",
    "suspend",
    "retire",
    "archive",
    "restore",
)
_SANDBOX_ACTIONS = (
    "read",
    "create",
    "update",
    "activate",
    "retire",
    "archive",
    "restore",
)
_TRYIT_ACTIONS = ("read", "create", "update", "close", "expire", "archive", "restore")
_OPENAPI_REF_ACTIONS = (
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
    "finalize",
    "export",
    "retire",
    "archive",
    "restore",
    "admin",
)


def _perms(resource: str, actions: tuple[str, ...]) -> list[tuple[str, str, str, str]]:
    return [
        (
            f"{DEVPORTAL_PERMISSION_NAMESPACE}.{resource}:{action}",
            f"{DEVPORTAL_PERMISSION_NAMESPACE}.{resource}",
            action,
            _MODULE,
        )
        for action in actions
    ]


def _build_permissions() -> list[tuple[str, str, str, str]]:
    perms: list[tuple[str, str, str, str]] = []
    perms.extend(_perms("developer_organization", _REGISTRY_ACTIONS))
    perms.extend(_perms("developer_team", _REGISTRY_ACTIONS))
    perms.extend(_perms("developer_account", _ACCOUNT_ACTIONS))
    perms.extend(_perms("developer_membership", _REGISTRY_ACTIONS))
    perms.extend(_perms("developer_invite", _INVITE_ACTIONS))
    perms.extend(_perms("portal_session", _SESSION_ACTIONS))
    perms.extend(_perms("application", _APPLICATION_ACTIONS))
    perms.extend(_perms("api_product", _REGISTRY_ACTIONS))
    perms.extend(_perms("api_product_version", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("api_product_environment", _REGISTRY_ACTIONS))
    perms.extend(_perms("plan", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("subscription", _SUBSCRIPTION_ACTIONS))
    perms.extend(_perms("entitlement", _ENTITLEMENT_ACTIONS))
    perms.extend(_perms("documentation_entry", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("openapi_artifact_reference", _OPENAPI_REF_ACTIONS))
    perms.extend(_perms("sandbox_environment", _SANDBOX_ACTIONS))
    perms.extend(_perms("tryit_session", _TRYIT_ACTIONS))
    perms.extend(_perms("report", _REPORT_ACTIONS))
    return perms


DEVPORTAL_PERMISSIONS: list[tuple[str, str, str, str]] = _build_permissions()

PHASE2_PERMISSION_RESOURCES = ("plan", "subscription", "entitlement")
DEVPORTAL_PHASE2_PERMISSIONS = [
    p for p in DEVPORTAL_PERMISSIONS if p[1].split(".")[-1] in PHASE2_PERMISSION_RESOURCES
]

PHASE3_PERMISSION_RESOURCES = (
    "documentation_entry",
    "openapi_artifact_reference",
    "sandbox_environment",
    "tryit_session",
)
DEVPORTAL_PHASE3_PERMISSIONS = [
    p for p in DEVPORTAL_PERMISSIONS if p[1].split(".")[-1] in PHASE3_PERMISSION_RESOURCES
]

PHASE4_PERMISSION_RESOURCES = ("report",)
DEVPORTAL_PHASE4_PERMISSIONS = [
    p for p in DEVPORTAL_PERMISSIONS if p[1].split(".")[-1] in PHASE4_PERMISSION_RESOURCES
]

_ALL = [p[0] for p in DEVPORTAL_PERMISSIONS]

DEVPORTAL_ADMIN_PERMISSIONS = list(_ALL)

API_PRODUCT_MANAGER_PERMISSIONS = [
    p
    for p in _ALL
    if any(
        p.startswith(f"devportal.{r}:")
        for r in (
            "api_product",
            "api_product_version",
            "api_product_environment",
            "application",
            "developer_organization",
            "developer_team",
            "plan",
            "subscription",
            "entitlement",
            "documentation_entry",
            "openapi_artifact_reference",
            "sandbox_environment",
            "tryit_session",
            "report",
        )
    )
]

_DEVELOPER_READ_WRITE = (
    "developer_organization",
    "developer_team",
    "developer_account",
    "developer_membership",
    "developer_invite",
    "portal_session",
    "application",
    "api_product",
    "api_product_version",
    "api_product_environment",
    "plan",
    "subscription",
    "entitlement",
    "documentation_entry",
    "openapi_artifact_reference",
    "sandbox_environment",
    "tryit_session",
    "report",
)

DEVELOPER_PERMISSIONS = [
    p
    for p in _ALL
    if any(p.startswith(f"devportal.{r}:") for r in _DEVELOPER_READ_WRITE)
    and not any(
        p.endswith(f":{a}")
        for a in ("approve", "lock", "admin", "publish", "retire", "bind")
    )
]

PARTNER_DEVELOPER_PERMISSIONS = [
    p
    for p in DEVELOPER_PERMISSIONS
    if not p.startswith("devportal.developer_organization:")
    and not p.startswith("devportal.developer_team:create")
]

API_AUDITOR_PERMISSIONS = [
    p for p in _ALL if p.endswith(":read") or p.endswith(":validate") or p.endswith(":export")
]
