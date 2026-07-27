"""AI Platform Pydantic schemas — Phase 1."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PageMeta(BaseModel):
    total: int
    page: int
    page_size: int
    sort_by: str | None = None
    sort_dir: str = "asc"


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    sort_by: str | None = None
    sort_dir: str = "asc"


def page_of(
    items: list[T],
    *,
    total: int,
    page: int,
    page_size: int,
    sort_by: str | None = None,
    sort_dir: str = "asc",
) -> Page[T]:
    return Page(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


class MessageResponse(BaseModel):
    message: str


class ValidationIssueResponse(BaseModel):
    code: str
    message: str
    severity: str = "error"
    field: str | None = None


class PublishValidationResponse(BaseModel):
    valid: bool
    version_id: UUID
    template_id: UUID
    issues: list[ValidationIssueResponse] = Field(default_factory=list)
    warnings: list[ValidationIssueResponse] = Field(default_factory=list)


class LifecycleReason(BaseModel):
    reason: str | None = None


class PublishBody(BaseModel):
    publish_reason: str | None = None


class RetireBody(BaseModel):
    retire_reason: str | None = None


class CloneBody(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    clone_reason: str | None = None


# --- Provider ---


class ProviderCreate(BaseModel):
    company_id: UUID | None = None
    provider_code: str | None = None
    provider_name: str
    description: str | None = None
    status: str | None = "active"
    sort_order: int | None = 0


class ProviderUpdate(BaseModel):
    provider_name: str | None = None
    description: str | None = None
    status: str | None = None
    sort_order: int | None = None
    version: int | None = None


class ProviderResponse(OrmModel):
    id: UUID
    company_id: UUID
    provider_code: str
    provider_name: str
    description: str | None = None
    status: str
    sort_order: int
    version: int
    is_deleted: bool | None = None


# --- Model ---


class ModelCreate(BaseModel):
    company_id: UUID | None = None
    provider_id: UUID
    model_code: str | None = None
    model_name: str
    description: str | None = None
    status: str | None = "draft"
    capability_json: str | None = None
    residency_region: str | None = None
    cost_class: str | None = None


class ModelUpdate(BaseModel):
    model_name: str | None = None
    description: str | None = None
    status: str | None = None
    capability_json: str | None = None
    residency_region: str | None = None
    cost_class: str | None = None
    version: int | None = None


class ModelResponse(OrmModel):
    id: UUID
    company_id: UUID
    provider_id: UUID
    model_code: str
    model_name: str
    description: str | None = None
    status: str
    capability_json: str | None = None
    residency_region: str | None = None
    cost_class: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Credential ---


class CredentialCreate(BaseModel):
    company_id: UUID | None = None
    provider_id: UUID
    credential_code: str | None = None
    secret_store_ref: str = Field(..., min_length=1, max_length=255)
    status: str | None = "active"
    description: str | None = None


class CredentialUpdate(BaseModel):
    secret_store_ref: str | None = Field(default=None, min_length=1, max_length=255)
    status: str | None = None
    description: str | None = None
    version: int | None = None


class CredentialResponse(OrmModel):
    id: UUID
    company_id: UUID
    provider_id: UUID
    credential_code: str
    secret_store_ref: str
    status: str
    description: str | None = None
    version: int
    is_deleted: bool | None = None


class CredentialRotate(BaseModel):
    secret_store_ref: str = Field(..., min_length=1, max_length=255)
    rotate_reason: str | None = None


# --- Configuration ---


class ConfigurationCreate(BaseModel):
    company_id: UUID | None = None
    config_code: str | None = None
    config_name: str
    scope: str
    scope_ref_id: UUID | None = None
    status: str | None = "draft"
    config_json: str | None = None
    description: str | None = None


class ConfigurationUpdate(BaseModel):
    config_name: str | None = None
    scope: str | None = None
    scope_ref_id: UUID | None = None
    status: str | None = None
    config_json: str | None = None
    description: str | None = None
    version: int | None = None


class ConfigurationResponse(OrmModel):
    id: UUID
    company_id: UUID
    config_code: str
    config_name: str
    scope: str
    scope_ref_id: UUID | None = None
    status: str
    config_json: str | None = None
    description: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Prompt Template ---


class PromptTemplateCreate(BaseModel):
    company_id: UUID | None = None
    template_code: str | None = None
    template_name: str
    description: str | None = None
    status: str | None = "active"


class PromptTemplateUpdate(BaseModel):
    template_name: str | None = None
    description: str | None = None
    status: str | None = None
    version: int | None = None


class PromptTemplateResponse(OrmModel):
    id: UUID
    company_id: UUID
    template_code: str
    template_name: str
    description: str | None = None
    status: str
    version: int
    is_deleted: bool | None = None


# --- Prompt Version ---


class PromptVersionCreate(BaseModel):
    template_id: UUID
    company_id: UUID | None = None
    version_label: str | None = None
    change_notes: str | None = None
    content_text: str | None = None


class PromptVersionUpdate(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    content_text: str | None = None
    version: int | None = None


class PromptVersionResponse(OrmModel):
    id: UUID
    company_id: UUID
    template_id: UUID
    version_code: str
    version_number: int
    version_label: str | None = None
    change_notes: str | None = None
    status: str
    content_text: str
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    cloned_from_version_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Prompt Variable ---


class PromptVariableCreate(BaseModel):
    prompt_version_id: UUID
    company_id: UUID | None = None
    variable_code: str | None = None
    variable_name: str
    data_type: str
    is_required: bool | None = False
    default_value: str | None = None
    description: str | None = None


class PromptVariableUpdate(BaseModel):
    variable_name: str | None = None
    data_type: str | None = None
    is_required: bool | None = None
    default_value: str | None = None
    description: str | None = None
    version: int | None = None


class PromptVariableResponse(OrmModel):
    id: UUID
    company_id: UUID
    prompt_version_id: UUID
    variable_code: str
    variable_name: str
    data_type: str
    is_required: bool
    default_value: str | None = None
    description: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Gateway Policy ---


class GatewayPolicyCreate(BaseModel):
    company_id: UUID | None = None
    policy_code: str | None = None
    policy_name: str
    status: str | None = "draft"
    policy_json: str | None = None
    description: str | None = None


class GatewayPolicyUpdate(BaseModel):
    policy_name: str | None = None
    status: str | None = None
    policy_json: str | None = None
    description: str | None = None
    version: int | None = None


class GatewayPolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    policy_code: str
    policy_name: str
    status: str
    policy_json: str | None = None
    description: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Routing Rule ---


class RoutingRuleCreate(BaseModel):
    company_id: UUID | None = None
    gateway_policy_id: UUID
    provider_id: UUID
    model_id: UUID
    rule_code: str | None = None
    priority: int | None = 0
    status: str | None = "draft"
    rule_json: str | None = None
    description: str | None = None


class RoutingRuleUpdate(BaseModel):
    priority: int | None = None
    status: str | None = None
    rule_json: str | None = None
    description: str | None = None
    version: int | None = None


class RoutingRuleResponse(OrmModel):
    id: UUID
    company_id: UUID
    gateway_policy_id: UUID
    provider_id: UUID
    model_id: UUID
    rule_code: str
    priority: int
    status: str
    rule_json: str | None = None
    description: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Guardrail Policy ---


class GuardrailPolicyCreate(BaseModel):
    company_id: UUID | None = None
    policy_code: str | None = None
    policy_name: str
    status: str | None = "draft"
    policy_json: str | None = None
    description: str | None = None


class GuardrailPolicyUpdate(BaseModel):
    policy_name: str | None = None
    status: str | None = None
    policy_json: str | None = None
    description: str | None = None
    version: int | None = None


class GuardrailPolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    policy_code: str
    policy_name: str
    status: str
    policy_json: str | None = None
    description: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Moderation Policy ---


class ModerationPolicyCreate(BaseModel):
    company_id: UUID | None = None
    policy_code: str | None = None
    policy_name: str
    status: str | None = "draft"
    policy_json: str | None = None
    description: str | None = None


class ModerationPolicyUpdate(BaseModel):
    policy_name: str | None = None
    status: str | None = None
    policy_json: str | None = None
    description: str | None = None
    version: int | None = None


class ModerationPolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    policy_code: str
    policy_name: str
    status: str
    policy_json: str | None = None
    description: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Rate Limit Policy ---


class RateLimitPolicyCreate(BaseModel):
    company_id: UUID | None = None
    policy_code: str | None = None
    policy_name: str
    status: str | None = "draft"
    policy_json: str | None = None
    description: str | None = None


class RateLimitPolicyUpdate(BaseModel):
    policy_name: str | None = None
    status: str | None = None
    policy_json: str | None = None
    description: str | None = None
    version: int | None = None


class RateLimitPolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    policy_code: str
    policy_name: str
    status: str
    policy_json: str | None = None
    description: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Assistant ---


class AssistantCreate(BaseModel):
    company_id: UUID | None = None
    assistant_code: str | None = None
    assistant_name: str
    assistant_kind: str
    prompt_version_id: UUID
    configuration_id: UUID | None = None
    gateway_policy_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    moderation_policy_id: UUID | None = None
    rate_limit_policy_id: UUID | None = None
    lowcode_form_id: UUID | None = None
    lowcode_page_id: UUID | None = None
    status: str | None = "draft"
    description: str | None = None


class AssistantUpdate(BaseModel):
    assistant_name: str | None = None
    assistant_kind: str | None = None
    configuration_id: UUID | None = None
    gateway_policy_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    moderation_policy_id: UUID | None = None
    rate_limit_policy_id: UUID | None = None
    lowcode_form_id: UUID | None = None
    lowcode_page_id: UUID | None = None
    status: str | None = None
    description: str | None = None
    version: int | None = None


class AssistantResponse(OrmModel):
    id: UUID
    company_id: UUID
    assistant_code: str
    assistant_name: str
    assistant_kind: str
    prompt_version_id: UUID
    configuration_id: UUID | None = None
    gateway_policy_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    moderation_policy_id: UUID | None = None
    rate_limit_policy_id: UUID | None = None
    lowcode_form_id: UUID | None = None
    lowcode_page_id: UUID | None = None
    status: str
    description: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Session ---


class SessionCreate(BaseModel):
    company_id: UUID | None = None
    session_code: str | None = None
    assistant_id: UUID | None = None
    agent_version_id: UUID | None = None
    configuration_id: UUID | None = None
    user_id: UUID | None = None
    module_code: str | None = None
    entity_id: UUID | None = None
    bpm_task_id: UUID | None = None
    status: str | None = "open"
    ttl_minutes: int | None = None


class SessionUpdate(BaseModel):
    assistant_id: UUID | None = None
    configuration_id: UUID | None = None
    module_code: str | None = None
    entity_id: UUID | None = None
    bpm_task_id: UUID | None = None
    status: str | None = None
    version: int | None = None


class SessionResponse(OrmModel):
    id: UUID
    company_id: UUID
    session_code: str
    status: str
    assistant_id: UUID | None = None
    agent_version_id: UUID | None = None
    configuration_id: UUID | None = None
    user_id: UUID
    module_code: str | None = None
    entity_id: UUID | None = None
    bpm_task_id: UUID | None = None
    opened_at: datetime
    closed_at: datetime | None = None
    expires_at: datetime | None = None
    version: int
    is_deleted: bool | None = None


# --- Conversation ---


class ConversationCreate(BaseModel):
    company_id: UUID | None = None
    session_id: UUID
    conversation_code: str | None = None
    title: str | None = None
    status: str | None = "active"


class ConversationUpdate(BaseModel):
    title: str | None = None
    status: str | None = None
    version: int | None = None


class ConversationResponse(OrmModel):
    id: UUID
    company_id: UUID
    session_id: UUID
    conversation_code: str
    status: str
    title: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Conversation Message ---


class ConversationMessageCreate(BaseModel):
    company_id: UUID | None = None
    conversation_id: UUID
    message_role: str
    content_text: str
    sequence_no: int | None = None
    token_count: int | None = None
    prompt_version_id: UUID | None = None
    tool_version_id: UUID | None = None


class ConversationMessageUpdate(BaseModel):
    content_text: str | None = None
    token_count: int | None = None
    version: int | None = None


class ConversationMessageResponse(OrmModel):
    id: UUID
    company_id: UUID
    conversation_id: UUID
    message_role: str
    content_text: str
    sequence_no: int
    token_count: int | None = None
    prompt_version_id: UUID | None = None
    tool_version_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Conversation Memory ---


class ConversationMemoryCreate(BaseModel):
    company_id: UUID | None = None
    conversation_id: UUID
    memory_code: str | None = None
    memory_kind: str
    content_text: str
    status: str | None = "active"
    expires_at: datetime | None = None


class ConversationMemoryUpdate(BaseModel):
    content_text: str | None = None
    status: str | None = None
    expires_at: datetime | None = None
    version: int | None = None


class ConversationMemoryResponse(OrmModel):
    id: UUID
    company_id: UUID
    conversation_id: UUID
    memory_code: str
    memory_kind: str
    content_text: str
    status: str
    expires_at: datetime | None = None
    version: int
    is_deleted: bool | None = None


# --- Context Package ---


class ContextPackageCreate(BaseModel):
    company_id: UUID | None = None
    session_id: UUID
    package_code: str | None = None
    status: str | None = "active"
    module_code: str | None = None
    entity_id: UUID | None = None
    context_json: str | None = None
    prompt_version_id: UUID | None = None
    lowcode_form_id: UUID | None = None
    bpm_task_id: UUID | None = None
    document_id: UUID | None = None


class ContextPackageUpdate(BaseModel):
    status: str | None = None
    module_code: str | None = None
    entity_id: UUID | None = None
    context_json: str | None = None
    prompt_version_id: UUID | None = None
    lowcode_form_id: UUID | None = None
    bpm_task_id: UUID | None = None
    document_id: UUID | None = None
    version: int | None = None


class ContextPackageResponse(OrmModel):
    id: UUID
    company_id: UUID
    session_id: UUID
    package_code: str
    status: str
    module_code: str | None = None
    entity_id: UUID | None = None
    context_json: str | None = None
    prompt_version_id: UUID | None = None
    lowcode_form_id: UUID | None = None
    bpm_task_id: UUID | None = None
    document_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Usage Record ---


class UsageRecordCreate(BaseModel):
    company_id: UUID | None = None
    session_id: UUID
    model_id: UUID
    usage_code: str | None = None
    input_tokens: int | None = 0
    output_tokens: int | None = 0
    total_tokens: int | None = 0
    unit_label: str | None = None
    recorded_at: datetime | None = None


class UsageRecordUpdate(BaseModel):
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    unit_label: str | None = None
    version: int | None = None


class UsageRecordResponse(OrmModel):
    id: UUID
    company_id: UUID
    session_id: UUID
    model_id: UUID
    usage_code: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    unit_label: str | None = None
    recorded_at: datetime
    version: int
    is_deleted: bool | None = None


# --- Cost Record ---


class CostRecordCreate(BaseModel):
    company_id: UUID | None = None
    session_id: UUID
    model_id: UUID
    cost_code: str | None = None
    currency_code: str | None = "USD"
    amount: Decimal
    recorded_at: datetime | None = None
    notes: str | None = None


class CostRecordUpdate(BaseModel):
    currency_code: str | None = None
    amount: Decimal | None = None
    notes: str | None = None
    version: int | None = None


class CostRecordResponse(OrmModel):
    id: UUID
    company_id: UUID
    session_id: UUID
    model_id: UUID
    cost_code: str
    currency_code: str
    amount: Decimal
    recorded_at: datetime
    notes: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Cache Entry ---


class CacheEntryCreate(BaseModel):
    company_id: UUID | None = None
    session_id: UUID | None = None
    entry_code: str | None = None
    cache_key: str = Field(..., min_length=1, max_length=255)
    cache_scope: str | None = None
    status: str | None = "created"
    expires_at: datetime | None = None
    payload_json: str | None = None


class CacheEntryUpdate(BaseModel):
    cache_scope: str | None = None
    status: str | None = None
    expires_at: datetime | None = None
    payload_json: str | None = None
    version: int | None = None


class CacheEntryResponse(OrmModel):
    id: UUID
    company_id: UUID
    session_id: UUID | None = None
    entry_code: str
    cache_key: str
    cache_scope: str | None = None
    status: str
    expires_at: datetime | None = None
    payload_json: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Runtime ---


class RuntimeResolveRequest(BaseModel):
    company_id: UUID | None = None
    assistant_id: UUID | None = None
    session_id: UUID | None = None
    prompt_version_id: UUID | None = None
    configuration_id: UUID | None = None
    module_code: str | None = None
    entity_id: UUID | None = None


class RuntimeResolveResponse(BaseModel):
    assistant_id: UUID | None = None
    prompt_version_id: UUID | None = None
    configuration_id: UUID | None = None
    model_id: UUID | None = None
    provider_id: UUID | None = None
    gateway_policy_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    moderation_policy_id: UUID | None = None
    rate_limit_policy_id: UUID | None = None
    resolved_json: str | None = None


class InvokeRequest(BaseModel):
    assistant_id: UUID
    company_id: UUID | None = None
    session_id: UUID | None = None
    conversation_id: UUID | None = None
    user_message: str = Field(..., min_length=1)
    messages: list[dict[str, Any]] | None = None
    prompt_variables: dict[str, Any] | None = None
    use_cache: bool = False
    correlation_id: str | None = None
    context_package_id: UUID | None = None
    metadata_json: str | None = None


class InvokeResponse(BaseModel):
    session_id: UUID
    conversation_id: UUID
    message_id: UUID | None = None
    assistant_message: str | None = None
    model_id: UUID | None = None
    prompt_version_id: UUID | None = None
    usage_record_id: UUID | None = None
    cost_record_id: UUID | None = None
    correlation_id: str | None = None
    metadata_json: str | None = None


# --- Knowledge Base (Phase 2) ---


class KnowledgeBaseCreate(BaseModel):
    company_id: UUID | None = None
    knowledge_base_code: str | None = None
    knowledge_base_name: str
    description: str | None = None
    classification: str | None = None
    retention_policy_json: str | None = None
    access_policy_json: str | None = None
    status: str | None = "draft"


class KnowledgeBaseUpdate(BaseModel):
    knowledge_base_name: str | None = None
    description: str | None = None
    classification: str | None = None
    retention_policy_json: str | None = None
    access_policy_json: str | None = None
    status: str | None = None
    version: int | None = None


class KnowledgeBaseResponse(OrmModel):
    id: UUID
    company_id: UUID
    knowledge_base_code: str
    knowledge_base_name: str
    description: str | None = None
    classification: str | None = None
    retention_policy_json: str | None = None
    access_policy_json: str | None = None
    status: str
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Knowledge Source ---


class KnowledgeSourceCreate(BaseModel):
    company_id: UUID | None = None
    knowledge_base_id: UUID
    source_code: str | None = None
    source_name: str | None = None
    source_kind: str
    document_id: UUID | None = None
    external_ref: str | None = None
    status: str | None = "active"
    description: str | None = None
    metadata_json: str | None = None


class KnowledgeSourceUpdate(BaseModel):
    source_name: str | None = None
    source_kind: str | None = None
    document_id: UUID | None = None
    external_ref: str | None = None
    description: str | None = None
    metadata_json: str | None = None
    status: str | None = None
    version: int | None = None


class KnowledgeSourceResponse(OrmModel):
    id: UUID
    company_id: UUID
    knowledge_base_id: UUID
    source_code: str
    source_name: str | None = None
    source_kind: str
    document_id: UUID | None = None
    external_ref: str | None = None
    status: str
    description: str | None = None
    metadata_json: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Knowledge Chunk ---


class KnowledgeChunkCreate(BaseModel):
    company_id: UUID | None = None
    knowledge_source_id: UUID
    chunk_code: str | None = None
    sequence_no: int
    content_preview: str | None = None
    content_hash: str | None = None
    token_estimate: int | None = None
    status: str | None = "created"
    metadata_json: str | None = None


class KnowledgeChunkUpdate(BaseModel):
    sequence_no: int | None = None
    content_preview: str | None = None
    content_hash: str | None = None
    token_estimate: int | None = None
    metadata_json: str | None = None
    status: str | None = None
    version: int | None = None


class KnowledgeChunkResponse(OrmModel):
    id: UUID
    company_id: UUID
    knowledge_source_id: UUID
    chunk_code: str
    sequence_no: int
    content_preview: str | None = None
    content_hash: str | None = None
    token_estimate: int | None = None
    status: str
    metadata_json: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Embedding ---


class EmbeddingCreate(BaseModel):
    company_id: UUID | None = None
    knowledge_chunk_id: UUID
    model_id: UUID
    embedding_code: str | None = None
    dimensions: int | None = None
    status: str | None = "created"
    vector_ref: str | None = None
    metadata_json: str | None = None


class EmbeddingUpdate(BaseModel):
    model_id: UUID | None = None
    dimensions: int | None = None
    vector_ref: str | None = None
    metadata_json: str | None = None
    status: str | None = None
    version: int | None = None


class EmbeddingResponse(OrmModel):
    id: UUID
    company_id: UUID
    knowledge_chunk_id: UUID
    model_id: UUID
    embedding_code: str
    dimensions: int | None = None
    status: str
    vector_ref: str | None = None
    metadata_json: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Vector Index ---


class VectorIndexCreate(BaseModel):
    company_id: UUID | None = None
    knowledge_base_id: UUID
    model_id: UUID
    index_code: str | None = None
    index_name: str | None = None
    status: str | None = "active"
    provider_index_ref: str | None = None
    description: str | None = None


class VectorIndexUpdate(BaseModel):
    index_name: str | None = None
    model_id: UUID | None = None
    provider_index_ref: str | None = None
    description: str | None = None
    status: str | None = None
    version: int | None = None


class VectorIndexResponse(OrmModel):
    id: UUID
    company_id: UUID
    knowledge_base_id: UUID
    model_id: UUID
    index_code: str
    index_name: str | None = None
    status: str
    provider_index_ref: str | None = None
    description: str | None = None
    version: int
    is_deleted: bool | None = None


class IngestionEnqueueBody(BaseModel):
    model_id: UUID | None = None


# --- Tool (Phase 3) ---


class ToolCreate(BaseModel):
    company_id: UUID | None = None
    tool_code: str | None = None
    tool_name: str
    description: str | None = None
    module_code: str
    side_effect_class: str = "read_only"
    auth_scope_json: str | None = None
    status: str | None = "draft"


class ToolUpdate(BaseModel):
    tool_name: str | None = None
    description: str | None = None
    module_code: str | None = None
    side_effect_class: str | None = None
    auth_scope_json: str | None = None
    status: str | None = None
    version: int | None = None


class ToolResponse(OrmModel):
    id: UUID
    company_id: UUID
    tool_code: str
    tool_name: str
    description: str | None = None
    module_code: str
    side_effect_class: str
    auth_scope_json: str | None = None
    status: str
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Tool Version ---


class ToolVersionCreate(BaseModel):
    company_id: UUID | None = None
    tool_id: UUID
    input_schema_json: str
    output_schema_json: str | None = None
    contract_key: str | None = None
    version_label: str | None = None
    change_notes: str | None = None


class ToolVersionUpdate(BaseModel):
    input_schema_json: str | None = None
    output_schema_json: str | None = None
    contract_key: str | None = None
    version_label: str | None = None
    change_notes: str | None = None
    version: int | None = None


class ToolVersionResponse(OrmModel):
    id: UUID
    company_id: UUID
    tool_id: UUID
    version_code: str
    version_number: int
    version_label: str | None = None
    change_notes: str | None = None
    status: str
    input_schema_json: str
    output_schema_json: str | None = None
    contract_key: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    cloned_from_version_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Skill ---


class SkillCreate(BaseModel):
    company_id: UUID | None = None
    skill_code: str | None = None
    skill_name: str
    description: str | None = None
    tool_version_ids: list[UUID] | None = None
    tool_version_ids_json: str | None = None
    prompt_version_id: UUID | None = None
    status: str | None = "draft"


class SkillUpdate(BaseModel):
    skill_name: str | None = None
    description: str | None = None
    tool_version_ids: list[UUID] | None = None
    tool_version_ids_json: str | None = None
    prompt_version_id: UUID | None = None
    status: str | None = None
    version: int | None = None


class SkillResponse(OrmModel):
    id: UUID
    company_id: UUID
    skill_code: str
    skill_name: str
    description: str | None = None
    status: str
    tool_version_ids_json: str
    prompt_version_id: UUID | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Agent ---


class AgentCreate(BaseModel):
    company_id: UUID | None = None
    agent_code: str | None = None
    agent_name: str
    description: str | None = None
    risk_class: str | None = None
    status: str | None = "active"
    owner_role_ref: UUID | None = None


class AgentUpdate(BaseModel):
    agent_name: str | None = None
    description: str | None = None
    risk_class: str | None = None
    status: str | None = None
    owner_role_ref: UUID | None = None
    version: int | None = None


class AgentResponse(OrmModel):
    id: UUID
    company_id: UUID
    agent_code: str
    agent_name: str
    description: str | None = None
    risk_class: str | None = None
    status: str
    owner_role_ref: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Agent Version ---


class AgentVersionCreate(BaseModel):
    company_id: UUID | None = None
    agent_id: UUID
    prompt_version_id: UUID
    skill_ids: list[UUID] | None = None
    tool_version_ids: list[UUID] | None = None
    knowledge_base_id: UUID | None = None
    gateway_policy_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    moderation_policy_id: UUID | None = None
    rate_limit_policy_id: UUID | None = None
    bpm_definition_id: UUID | None = None
    max_steps: int | None = None
    max_tokens: int | None = None
    hitl_policy_json: str | None = None
    orchestration_limits_json: str | None = None
    version_label: str | None = None


class AgentVersionUpdate(BaseModel):
    prompt_version_id: UUID | None = None
    skill_ids: list[UUID] | None = None
    tool_version_ids: list[UUID] | None = None
    knowledge_base_id: UUID | None = None
    gateway_policy_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    moderation_policy_id: UUID | None = None
    rate_limit_policy_id: UUID | None = None
    bpm_definition_id: UUID | None = None
    max_steps: int | None = None
    max_tokens: int | None = None
    hitl_policy_json: str | None = None
    orchestration_limits_json: str | None = None
    version_label: str | None = None
    version: int | None = None


class AgentVersionResponse(OrmModel):
    id: UUID
    company_id: UUID
    agent_id: UUID
    version_code: str
    version_number: int
    version_label: str | None = None
    status: str
    prompt_version_id: UUID
    skill_ids_json: str
    tool_version_ids_json: str
    knowledge_base_id: UUID | None = None
    gateway_policy_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    moderation_policy_id: UUID | None = None
    rate_limit_policy_id: UUID | None = None
    bpm_definition_id: UUID | None = None
    max_steps: int | None = None
    max_tokens: int | None = None
    hitl_policy_json: str | None = None
    orchestration_limits_json: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    cloned_from_version_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Evaluation (Phase 4) ---


class EvaluationCreate(BaseModel):
    company_id: UUID | None = None
    evaluation_code: str | None = None
    evaluation_name: str | None = None
    evaluation_kind: str | None = None
    prompt_version_id: UUID | None = None
    knowledge_base_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    agent_version_id: UUID | None = None
    dataset_ref_json: str | None = None
    status: str | None = "queued"


class EvaluationUpdate(BaseModel):
    evaluation_name: str | None = None
    evaluation_kind: str | None = None
    prompt_version_id: UUID | None = None
    knowledge_base_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    agent_version_id: UUID | None = None
    dataset_ref_json: str | None = None
    result_summary_json: str | None = None
    metrics_json: str | None = None
    version: int | None = None


class EvaluationCompleteBody(BaseModel):
    result_summary_json: str | None = None
    metrics_json: str | None = None


class EvaluationFailBody(BaseModel):
    failure_reason: str | None = None


class EvaluationResponse(OrmModel):
    id: UUID
    company_id: UUID
    evaluation_code: str
    evaluation_name: str | None = None
    evaluation_kind: str | None = None
    status: str
    prompt_version_id: UUID | None = None
    knowledge_base_id: UUID | None = None
    guardrail_policy_id: UUID | None = None
    agent_version_id: UUID | None = None
    dataset_ref_json: str | None = None
    result_summary_json: str | None = None
    metrics_json: str | None = None
    failure_reason: str | None = None
    queued_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    failed_at: datetime | None = None
    version: int
    is_deleted: bool | None = None


# --- Feedback ---


class FeedbackCreate(BaseModel):
    company_id: UUID | None = None
    feedback_code: str | None = None
    session_id: UUID | None = None
    conversation_id: UUID | None = None
    message_id: UUID | None = None
    rating: int | None = None
    comment_text: str | None = None
    correction_flag: bool | None = False
    feedback_kind: str | None = None
    metadata_json: str | None = None
    bpm_case_id: UUID | None = None
    status: str | None = "captured"


class FeedbackUpdate(BaseModel):
    rating: int | None = None
    comment_text: str | None = None
    correction_flag: bool | None = None
    feedback_kind: str | None = None
    metadata_json: str | None = None
    bpm_case_id: UUID | None = None
    version: int | None = None


class FeedbackResponse(OrmModel):
    id: UUID
    company_id: UUID
    feedback_code: str
    status: str
    session_id: UUID | None = None
    conversation_id: UUID | None = None
    message_id: UUID | None = None
    rating: int | None = None
    comment_text: str | None = None
    correction_flag: bool
    feedback_kind: str | None = None
    metadata_json: str | None = None
    bpm_case_id: UUID | None = None
    reviewed_at: datetime | None = None
    reviewed_by: UUID | None = None
    closed_at: datetime | None = None
    closed_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Multimodal Profile ---


class MultimodalProfileCreate(BaseModel):
    company_id: UUID | None = None
    profile_code: str | None = None
    profile_name: str
    description: str | None = None
    modality_kind: str
    provider_id: UUID
    model_id: UUID | None = None
    document_id: UUID | None = None
    capabilities_json: str | None = None
    ingress_policy_json: str | None = None
    egress_policy_json: str | None = None
    status: str | None = "draft"


class MultimodalProfileUpdate(BaseModel):
    profile_name: str | None = None
    description: str | None = None
    modality_kind: str | None = None
    provider_id: UUID | None = None
    model_id: UUID | None = None
    document_id: UUID | None = None
    capabilities_json: str | None = None
    ingress_policy_json: str | None = None
    egress_policy_json: str | None = None
    status: str | None = None
    version: int | None = None


class MultimodalProfileResponse(OrmModel):
    id: UUID
    company_id: UUID
    profile_code: str
    profile_name: str
    description: str | None = None
    modality_kind: str
    status: str
    provider_id: UUID
    model_id: UUID | None = None
    document_id: UUID | None = None
    capabilities_json: str | None = None
    ingress_policy_json: str | None = None
    egress_policy_json: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    version: int
    is_deleted: bool | None = None
