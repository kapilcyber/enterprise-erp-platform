"""AI Platform permission constants — Phase 1 + Phase 2 + Phase 3."""

AI_PERMISSION_NAMESPACE = "ai"

_MODULE = "ai"

# (code, resource, action, module)
_REGISTRY_ACTIONS = ("read", "create", "update", "archive", "restore", "admin")
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
_AGENT_CATALOG_ACTIONS = ("read", "create", "update", "archive", "restore", "admin")
_KNOWLEDGE_SOURCE_ACTIONS = _REGISTRY_ACTIONS + ("suspend",)
_KNOWLEDGE_CHUNK_ACTIONS = ("read", "create", "update", "archive", "restore", "invalidate")
_EMBEDDING_ACTIONS = (
    "read",
    "create",
    "update",
    "archive",
    "restore",
    "rebuild",
    "invalidate",
)
_VECTOR_INDEX_ACTIONS = (
    "read",
    "create",
    "update",
    "archive",
    "restore",
    "rebuild",
    "retire",
    "admin",
)
_PROMPT_TEMPLATE_ACTIONS = ("read", "create", "update", "archive", "restore", "delete")
_PROMPT_VARIABLE_ACTIONS = ("read", "create", "update", "archive", "restore", "delete")
_RUNTIME_ACTIONS = ("read", "create", "update", "archive", "restore")
_SESSION_ACTIONS = _RUNTIME_ACTIONS + ("invoke",)
_TELEMETRY_ACTIONS = ("read", "create", "audit")
_CACHE_ACTIONS = ("read", "create", "update", "delete", "archive", "restore", "admin")
_EVALUATION_ACTIONS = ("read", "create", "update", "archive", "restore", "start", "complete", "fail")
_FEEDBACK_ACTIONS = ("read", "create", "update", "archive", "restore", "review", "close")
_PLATFORM_ACTIONS = (("invoke", "invoke"), ("platform", "admin"))


def _perms(resource: str, actions: tuple[str, ...]) -> list[tuple[str, str, str, str]]:
    return [
        (f"{AI_PERMISSION_NAMESPACE}.{resource}:{action}", f"{AI_PERMISSION_NAMESPACE}.{resource}", action, _MODULE)
        for action in actions
    ]


def _build_permissions() -> list[tuple[str, str, str, str]]:
    perms: list[tuple[str, str, str, str]] = []
    for resource in ("provider", "model", "credential", "configuration"):
        perms.extend(_perms(resource, _REGISTRY_ACTIONS))
    perms.extend(_perms("prompt_template", _PROMPT_TEMPLATE_ACTIONS))
    perms.extend(_perms("prompt_version", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("prompt_variable", _PROMPT_VARIABLE_ACTIONS))
    for resource in (
        "gateway_policy",
        "routing_rule",
        "guardrail_policy",
        "moderation_policy",
        "rate_limit_policy",
    ):
        perms.extend(_perms(resource, _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("assistant", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("session", _SESSION_ACTIONS))
    perms.extend(_perms("conversation", _RUNTIME_ACTIONS))
    perms.extend(_perms("conversation_message", _RUNTIME_ACTIONS))
    perms.extend(_perms("conversation_memory", _PROMPT_VARIABLE_ACTIONS))
    perms.extend(_perms("context_package", _RUNTIME_ACTIONS))
    perms.extend(_perms("usage", _TELEMETRY_ACTIONS))
    perms.extend(_perms("cost", _TELEMETRY_ACTIONS))
    perms.extend(_perms("cache", _CACHE_ACTIONS))
    perms.extend(_perms("knowledge_base", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("knowledge_source", _KNOWLEDGE_SOURCE_ACTIONS))
    perms.extend(_perms("knowledge_chunk", _KNOWLEDGE_CHUNK_ACTIONS))
    perms.extend(_perms("embedding", _EMBEDDING_ACTIONS))
    perms.extend(_perms("vector_index", _VECTOR_INDEX_ACTIONS))
    perms.extend(_perms("tool", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("tool_version", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("skill", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("agent", _AGENT_CATALOG_ACTIONS))
    perms.extend(_perms("agent_version", _PUBLISHABLE_ACTIONS))
    perms.extend(_perms("evaluation", _EVALUATION_ACTIONS))
    perms.extend(_perms("feedback", _FEEDBACK_ACTIONS))
    perms.extend(_perms("multimodal_profile", _PUBLISHABLE_ACTIONS))
    for resource, action in _PLATFORM_ACTIONS:
        perms.append(
            (
                f"{AI_PERMISSION_NAMESPACE}.{resource}:{action}",
                f"{AI_PERMISSION_NAMESPACE}.{resource}",
                action,
                _MODULE,
            )
        )
    return perms


AI_PERMISSIONS: list[tuple[str, str, str, str]] = _build_permissions()

_ALL = [p[0] for p in AI_PERMISSIONS]

_REGISTRY_RESOURCES = ("provider", "model", "credential", "configuration")
_PROMPT_RESOURCES = ("prompt_template", "prompt_version", "prompt_variable")
_POLICY_RESOURCES = (
    "gateway_policy",
    "routing_rule",
    "guardrail_policy",
    "moderation_policy",
    "rate_limit_policy",
)
_VERSIONED_RESOURCES = _PROMPT_RESOURCES[1:] + _POLICY_RESOURCES + ("assistant",)
_RUNTIME_RESOURCES = (
    "session",
    "conversation",
    "conversation_message",
    "conversation_memory",
    "context_package",
)
_TELEMETRY_RESOURCES = ("usage", "cost")
_KNOWLEDGE_RESOURCES = (
    "knowledge_base",
    "knowledge_source",
    "knowledge_chunk",
    "embedding",
    "vector_index",
)
_PHASE3_RESOURCES = ("tool", "tool_version", "skill", "agent", "agent_version")
_PHASE3_VERSIONED_RESOURCES = ("tool_version", "skill", "agent_version")
_PHASE3_DESIGN_RESOURCES = ("tool", "tool_version", "skill", "agent", "agent_version")
_PHASE4_RESOURCES = ("evaluation", "feedback", "multimodal_profile")
_PHASE4_PUBLISHABLE_RESOURCES = ("multimodal_profile",)

AI_PHASE2_PERMISSIONS: list[tuple[str, str, str, str]] = [
    p for p in AI_PERMISSIONS if any(p[1] == f"ai.{r}" for r in _KNOWLEDGE_RESOURCES)
]

AI_PHASE3_PERMISSIONS: list[tuple[str, str, str, str]] = [
    p for p in AI_PERMISSIONS if any(p[1] == f"ai.{r}" for r in _PHASE3_RESOURCES)
]

AI_PHASE4_PERMISSIONS: list[tuple[str, str, str, str]] = [
    p for p in AI_PERMISSIONS if any(p[1] == f"ai.{r}" for r in _PHASE4_RESOURCES)
]

AI_PLATFORM_ADMIN_PERMISSIONS = list(_ALL)

AI_PROMPT_ENGINEER_PERMISSIONS = [
    p
    for p in _ALL
    if (
        any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _REGISTRY_RESOURCES)
        and not any(x in p for x in (":publish", ":retire", ":delete", ":admin"))
    )
    or (
        any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _PROMPT_RESOURCES)
        and not any(x in p for x in (":publish", ":retire", ":delete", ":admin"))
    )
    or (any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:read") for r in _POLICY_RESOURCES))
]

AI_PUBLISHER_PERMISSIONS = [
    p
    for p in _ALL
    if ":read" in p
    or (
        any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _VERSIONED_RESOURCES)
        and any(x in p for x in (":publish", ":retire", ":validate"))
    )
    or (
        p.startswith(f"{AI_PERMISSION_NAMESPACE}.knowledge_base:")
        and any(x in p for x in (":publish", ":retire", ":validate"))
    )
    or (
        any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _PHASE3_VERSIONED_RESOURCES)
        and any(x in p for x in (":publish", ":retire", ":validate"))
    )
    or (
        p.startswith(f"{AI_PERMISSION_NAMESPACE}.tool:")
        and any(x in p for x in (":publish", ":retire", ":validate"))
    )
    or (
        p.startswith(f"{AI_PERMISSION_NAMESPACE}.skill:")
        and any(x in p for x in (":publish", ":retire", ":validate"))
    )
    or (
        any(
            p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:")
            for r in _PHASE4_PUBLISHABLE_RESOURCES
        )
        and any(x in p for x in (":publish", ":retire", ":validate"))
    )
]

AI_AGENT_DESIGNER_PERMISSIONS = [
    p
    for p in _ALL
    if any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _PHASE3_DESIGN_RESOURCES)
    and not any(x in p for x in (":publish", ":retire", ":validate", ":admin"))
]

AI_KNOWLEDGE_CURATOR_PERMISSIONS = [
    p
    for p in _ALL
    if any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _KNOWLEDGE_RESOURCES)
    or p == f"{AI_PERMISSION_NAMESPACE}.model:read"
]

AI_OPERATOR_PERMISSIONS = [
    p
    for p in _ALL
    if any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _RUNTIME_RESOURCES)
    or p
    in (
        f"{AI_PERMISSION_NAMESPACE}.invoke:invoke",
        f"{AI_PERMISSION_NAMESPACE}.session:invoke",
    )
    or any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _TELEMETRY_RESOURCES)
    or p.startswith(f"{AI_PERMISSION_NAMESPACE}.cache:")
]

AI_AUDITOR_PERMISSIONS = [p for p in _ALL if ":read" in p or ":audit" in p]

AI_CONSUMER_PERMISSIONS = [
    f"{AI_PERMISSION_NAMESPACE}.invoke:invoke",
    f"{AI_PERMISSION_NAMESPACE}.session:invoke",
    f"{AI_PERMISSION_NAMESPACE}.session:read",
    f"{AI_PERMISSION_NAMESPACE}.session:create",
    f"{AI_PERMISSION_NAMESPACE}.conversation:read",
    f"{AI_PERMISSION_NAMESPACE}.conversation:create",
    f"{AI_PERMISSION_NAMESPACE}.conversation_message:read",
    f"{AI_PERMISSION_NAMESPACE}.conversation_message:create",
    f"{AI_PERMISSION_NAMESPACE}.context_package:read",
    f"{AI_PERMISSION_NAMESPACE}.feedback:create",
    f"{AI_PERMISSION_NAMESPACE}.feedback:read",
]

AI_QUALITY_ANALYST_PERMISSIONS = [
    p
    for p in _ALL
    if any(p.startswith(f"{AI_PERMISSION_NAMESPACE}.{r}:") for r in _PHASE4_RESOURCES)
    and not any(x in p for x in (":publish", ":retire", ":validate", ":admin"))
]
