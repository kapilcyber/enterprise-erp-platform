"""AI Platform API route handlers — Phase 1 + Phase 2."""

from modules.ai.routers.agents import (
    agent_versions_router,
    agents_router,
    skills_router,
    tool_versions_router,
    tools_router,
)
from modules.ai.routers.assistants import assistants_router
from modules.ai.routers.governance import (
    gateway_policies_router,
    guardrail_policies_router,
    moderation_policies_router,
    rate_limit_policies_router,
    routing_rules_router,
)
from modules.ai.routers.hardening import (
    evaluations_router,
    feedbacks_router,
    multimodal_profiles_router,
)
from modules.ai.routers.knowledge import (
    embeddings_router,
    knowledge_bases_router,
    knowledge_chunks_router,
    knowledge_sources_router,
    vector_indexes_router,
)
from modules.ai.routers.ops import (
    cache_entries_router,
    cost_records_router,
    usage_records_router,
)
from modules.ai.routers.prompts import (
    prompt_templates_router,
    prompt_variables_router,
    prompt_versions_router,
)
from modules.ai.routers.providers import (
    configurations_router,
    credentials_router,
    models_router,
    providers_router,
)
from modules.ai.routers.runtime import (
    context_packages_router,
    conversation_memories_router,
    conversation_messages_router,
    conversations_router,
    invoke_router,
    runtime_router,
    sessions_router,
)

__all__ = [
    "providers_router",
    "models_router",
    "credentials_router",
    "configurations_router",
    "prompt_templates_router",
    "prompt_versions_router",
    "prompt_variables_router",
    "gateway_policies_router",
    "routing_rules_router",
    "guardrail_policies_router",
    "moderation_policies_router",
    "rate_limit_policies_router",
    "assistants_router",
    "sessions_router",
    "conversations_router",
    "conversation_messages_router",
    "conversation_memories_router",
    "context_packages_router",
    "runtime_router",
    "invoke_router",
    "usage_records_router",
    "cost_records_router",
    "cache_entries_router",
    "knowledge_bases_router",
    "knowledge_sources_router",
    "knowledge_chunks_router",
    "embeddings_router",
    "vector_indexes_router",
    "tools_router",
    "tool_versions_router",
    "skills_router",
    "agents_router",
    "agent_versions_router",
    "evaluations_router",
    "feedbacks_router",
    "multimodal_profiles_router",
]
