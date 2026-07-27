"""AI Platform domain enums per FRD-27 / ERD-27 Phase 1."""

from enum import Enum


class ProviderStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"


PROVIDER_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in ProviderStatus)


class ModelStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


MODEL_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in ModelStatus)


class CredentialReferenceStatus(str, Enum):
    ACTIVE = "active"
    ROTATED = "rotated"
    RETIRED = "retired"


CREDENTIAL_REFERENCE_STATUS_VALUES: frozenset[str] = frozenset(
    t.value for t in CredentialReferenceStatus
)


class ConfigurationScope(str, Enum):
    TENANT = "tenant"
    COMPANY = "company"
    MODULE = "module"
    WORKLOAD = "workload"


CONFIGURATION_SCOPE_VALUES: frozenset[str] = frozenset(t.value for t in ConfigurationScope)


class ConfigurationStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


CONFIGURATION_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in ConfigurationStatus)


class PromptTemplateStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


PROMPT_TEMPLATE_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in PromptTemplateStatus)


class PromptVersionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


PROMPT_VERSION_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in PromptVersionStatus)


class PromptVariableDataType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    JSON = "json"


PROMPT_VARIABLE_DATA_TYPE_VALUES: frozenset[str] = frozenset(
    t.value for t in PromptVariableDataType
)


class PolicyStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


POLICY_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in PolicyStatus)


class AssistantKind(str, Enum):
    ASSISTANT = "assistant"
    COPILOT = "copilot"


ASSISTANT_KIND_VALUES: frozenset[str] = frozenset(t.value for t in AssistantKind)


class AssistantStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


ASSISTANT_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in AssistantStatus)


class SessionStatus(str, Enum):
    OPEN = "open"
    ACTIVE = "active"
    CLOSED = "closed"
    EXPIRED = "expired"


SESSION_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in SessionStatus)


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PURGED = "purged"


CONVERSATION_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in ConversationStatus)


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


MESSAGE_ROLE_VALUES: frozenset[str] = frozenset(t.value for t in MessageRole)


class MemoryKind(str, Enum):
    SUMMARY = "summary"
    PREFERENCE = "preference"
    FACT = "fact"
    OTHER = "other"


MEMORY_KIND_VALUES: frozenset[str] = frozenset(t.value for t in MemoryKind)


class MemoryStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    PURGED = "purged"


MEMORY_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in MemoryStatus)


class ContextPackageStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    PURGED = "purged"


CONTEXT_PACKAGE_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in ContextPackageStatus)


class CacheEntryStatus(str, Enum):
    CREATED = "created"
    EXPIRED = "expired"
    INVALIDATED = "invalidated"


CACHE_ENTRY_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in CacheEntryStatus)


class KnowledgeBaseStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


KNOWLEDGE_BASE_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in KnowledgeBaseStatus)


class KnowledgeSourceStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"


KNOWLEDGE_SOURCE_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in KnowledgeSourceStatus)


class KnowledgeSourceKind(str, Enum):
    DOCUMENT = "document"
    CURATED_PACK = "curated_pack"
    MODULE_EXTRACT = "module_extract"
    OTHER = "other"


KNOWLEDGE_SOURCE_KIND_VALUES: frozenset[str] = frozenset(t.value for t in KnowledgeSourceKind)


class KnowledgeChunkStatus(str, Enum):
    CREATED = "created"
    INVALIDATED = "invalidated"


KNOWLEDGE_CHUNK_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in KnowledgeChunkStatus)


class EmbeddingStatus(str, Enum):
    CREATED = "created"
    REBUILT = "rebuilt"
    INVALIDATED = "invalidated"


EMBEDDING_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in EmbeddingStatus)


class VectorIndexStatus(str, Enum):
    ACTIVE = "active"
    REBUILDING = "rebuilding"
    RETIRED = "retired"


VECTOR_INDEX_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in VectorIndexStatus)


class ToolStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


TOOL_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in ToolStatus)


class ToolVersionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


TOOL_VERSION_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in ToolVersionStatus)


class SkillStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


SKILL_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in SkillStatus)


class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


AGENT_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in AgentStatus)


class AgentVersionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


AGENT_VERSION_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in AgentVersionStatus)


class ToolSideEffectClass(str, Enum):
    READ_ONLY = "read_only"
    WRITE = "write"
    HIGH_RISK = "high_risk"


TOOL_SIDE_EFFECT_CLASS_VALUES: frozenset[str] = frozenset(t.value for t in ToolSideEffectClass)


class RiskClass(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


RISK_CLASS_VALUES: frozenset[str] = frozenset(t.value for t in RiskClass)


class AiEntityType(str, Enum):
    PROVIDER = "provider"
    MODEL = "model"
    PROVIDER_CREDENTIAL_REFERENCE = "provider_credential_reference"
    CONFIGURATION = "configuration"
    PROMPT_TEMPLATE = "prompt_template"
    PROMPT_VERSION = "prompt_version"
    PROMPT_VARIABLE = "prompt_variable"
    GATEWAY_POLICY = "gateway_policy"
    ROUTING_RULE = "routing_rule"
    GUARDRAIL_POLICY = "guardrail_policy"
    MODERATION_POLICY = "moderation_policy"
    RATE_LIMIT_POLICY = "rate_limit_policy"
    ASSISTANT = "assistant"
    SESSION = "session"
    CONVERSATION = "conversation"
    CONVERSATION_MESSAGE = "conversation_message"
    CONVERSATION_MEMORY = "conversation_memory"
    CONTEXT_PACKAGE = "context_package"
    USAGE_RECORD = "usage_record"
    COST_RECORD = "cost_record"
    CACHE_ENTRY = "cache_entry"
    KNOWLEDGE_BASE = "knowledge_base"
    KNOWLEDGE_SOURCE = "knowledge_source"
    KNOWLEDGE_CHUNK = "knowledge_chunk"
    EMBEDDING = "embedding"
    VECTOR_INDEX = "vector_index"
    TOOL = "tool"
    TOOL_VERSION = "tool_version"
    SKILL = "skill"
    AGENT = "agent"
    AGENT_VERSION = "agent_version"
    EVALUATION = "evaluation"
    FEEDBACK = "feedback"
    MULTIMODAL_PROFILE = "multimodal_profile"


# prefix, width, include_year
CODE_PREFIXES: dict[AiEntityType, tuple[str, int, bool]] = {
    AiEntityType.PROVIDER: ("AIPR-", 6, True),
    AiEntityType.MODEL: ("AIMD-", 6, True),
    AiEntityType.PROVIDER_CREDENTIAL_REFERENCE: ("AICR-", 6, True),
    AiEntityType.CONFIGURATION: ("AICF-", 6, True),
    AiEntityType.PROMPT_TEMPLATE: ("AIPT-", 6, True),
    AiEntityType.PROMPT_VERSION: ("AIPV-", 6, True),
    AiEntityType.PROMPT_VARIABLE: ("AIPVAR-", 6, True),
    AiEntityType.GATEWAY_POLICY: ("AIGP-", 6, True),
    AiEntityType.ROUTING_RULE: ("AIRR-", 6, True),
    AiEntityType.GUARDRAIL_POLICY: ("AIGR-", 6, True),
    AiEntityType.MODERATION_POLICY: ("AIMP-", 6, True),
    AiEntityType.RATE_LIMIT_POLICY: ("AIRL-", 6, True),
    AiEntityType.ASSISTANT: ("AIAS-", 6, True),
    AiEntityType.SESSION: ("AISS-", 6, True),
    AiEntityType.CONVERSATION: ("AICN-", 6, True),
    AiEntityType.CONVERSATION_MESSAGE: ("AICM-", 6, True),
    AiEntityType.CONVERSATION_MEMORY: ("AIMEM-", 6, True),
    AiEntityType.CONTEXT_PACKAGE: ("AICP-", 6, True),
    AiEntityType.USAGE_RECORD: ("AIUR-", 6, True),
    AiEntityType.COST_RECORD: ("AICT-", 6, True),
    AiEntityType.CACHE_ENTRY: ("AICE-", 6, True),
    AiEntityType.KNOWLEDGE_BASE: ("AIKB-", 6, True),
    AiEntityType.KNOWLEDGE_SOURCE: ("AIKS-", 6, True),
    AiEntityType.KNOWLEDGE_CHUNK: ("AIKC-", 6, True),
    AiEntityType.EMBEDDING: ("AIEM-", 6, True),
    AiEntityType.VECTOR_INDEX: ("AIVI-", 6, True),
    AiEntityType.TOOL: ("AITL-", 6, True),
    AiEntityType.TOOL_VERSION: ("AITV-", 6, True),
    AiEntityType.SKILL: ("AISK-", 6, True),
    AiEntityType.AGENT: ("AIAG-", 6, True),
    AiEntityType.AGENT_VERSION: ("AIAV-", 6, True),
    AiEntityType.EVALUATION: ("AIEV-", 6, True),
    AiEntityType.FEEDBACK: ("AIFB-", 6, True),
    AiEntityType.MULTIMODAL_PROFILE: ("AIMMP-", 6, True),
}


class EvaluationStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


EVALUATION_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in EvaluationStatus)


class FeedbackStatus(str, Enum):
    CAPTURED = "captured"
    REVIEWED = "reviewed"
    CLOSED = "closed"


FEEDBACK_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in FeedbackStatus)


class MultimodalProfileStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


MULTIMODAL_PROFILE_STATUS_VALUES: frozenset[str] = frozenset(
    t.value for t in MultimodalProfileStatus
)


class MultimodalModalityKind(str, Enum):
    OCR = "ocr"
    STT = "stt"
    TTS = "tts"
    VISION = "vision"
    MULTIMODAL = "multimodal"


MULTIMODAL_MODALITY_VALUES: frozenset[str] = frozenset(t.value for t in MultimodalModalityKind)
