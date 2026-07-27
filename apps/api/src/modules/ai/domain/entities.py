"""AI Platform domain entity markers — Phase 1."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class ProviderIdentity:
    provider_id: UUID
    provider_code: str


@dataclass
class ModelIdentity:
    model_id: UUID
    provider_id: UUID
    model_code: str
    status: str


@dataclass
class CredentialReferenceIdentity:
    credential_id: UUID
    provider_id: UUID
    credential_code: str


@dataclass
class ConfigurationIdentity:
    configuration_id: UUID
    config_code: str
    scope: str


@dataclass
class PromptTemplateIdentity:
    template_id: UUID
    template_code: str


@dataclass
class PromptVersionIdentity:
    version_id: UUID
    template_id: UUID
    version_number: int
    status: str


@dataclass
class PromptVariableIdentity:
    variable_id: UUID
    prompt_version_id: UUID
    variable_code: str
    data_type: str


@dataclass
class GatewayPolicyIdentity:
    policy_id: UUID
    policy_code: str
    status: str


@dataclass
class RoutingRuleIdentity:
    rule_id: UUID
    gateway_policy_id: UUID
    rule_code: str
    priority: int
    status: str


@dataclass
class GuardrailPolicyIdentity:
    policy_id: UUID
    policy_code: str
    status: str


@dataclass
class ModerationPolicyIdentity:
    policy_id: UUID
    policy_code: str
    status: str


@dataclass
class RateLimitPolicyIdentity:
    policy_id: UUID
    policy_code: str
    status: str


@dataclass
class AssistantIdentity:
    assistant_id: UUID
    assistant_code: str
    assistant_kind: str
    status: str


@dataclass
class SessionIdentity:
    session_id: UUID
    session_code: str
    user_id: UUID
    status: str


@dataclass
class ConversationIdentity:
    conversation_id: UUID
    session_id: UUID
    conversation_code: str


@dataclass
class ConversationMessageIdentity:
    message_id: UUID
    conversation_id: UUID
    message_role: str
    sequence_no: int


@dataclass
class ConversationMemoryIdentity:
    memory_id: UUID
    conversation_id: UUID
    memory_code: str
    memory_kind: str


@dataclass
class ContextPackageIdentity:
    package_id: UUID
    session_id: UUID
    package_code: str


@dataclass
class UsageRecordIdentity:
    usage_id: UUID
    session_id: UUID
    model_id: UUID
    usage_code: str


@dataclass
class CostRecordIdentity:
    cost_id: UUID
    session_id: UUID
    model_id: UUID
    cost_code: str


@dataclass
class CacheEntryIdentity:
    entry_id: UUID
    entry_code: str
    cache_key: str
    status: str


@dataclass
class KnowledgeBaseIdentity:
    knowledge_base_id: UUID
    knowledge_base_code: str
    status: str


@dataclass
class KnowledgeSourceIdentity:
    knowledge_source_id: UUID
    knowledge_base_id: UUID
    source_code: str
    source_kind: str
    status: str


@dataclass
class KnowledgeChunkIdentity:
    knowledge_chunk_id: UUID
    knowledge_source_id: UUID
    chunk_code: str
    sequence_no: int
    status: str


@dataclass
class EmbeddingIdentity:
    embedding_id: UUID
    knowledge_chunk_id: UUID
    model_id: UUID
    embedding_code: str
    status: str


@dataclass
class VectorIndexIdentity:
    vector_index_id: UUID
    knowledge_base_id: UUID
    model_id: UUID
    index_code: str
    status: str


@dataclass
class ToolIdentity:
    tool_id: UUID
    tool_code: str
    module_code: str
    side_effect_class: str
    status: str


@dataclass
class ToolVersionIdentity:
    version_id: UUID
    tool_id: UUID
    version_number: int
    status: str


@dataclass
class SkillIdentity:
    skill_id: UUID
    skill_code: str
    status: str


@dataclass
class AgentIdentity:
    agent_id: UUID
    agent_code: str
    status: str


@dataclass
class AgentVersionIdentity:
    version_id: UUID
    agent_id: UUID
    version_number: int
    status: str
