"""AI Platform application facade — Phase 1 + Phase 3."""

from sqlalchemy.orm import Session

from modules.ai.service.agent_design_service import AgentDesignService
from modules.ai.service.agent_service import AgentService
from modules.ai.service.agent_version_service import AgentVersionService
from modules.ai.service.ai_integration_service import AiIntegrationService
from modules.ai.service.assistant_service import AssistantService
from modules.ai.service.cache_entry_service import CacheEntryService
from modules.ai.service.configuration_service import ConfigurationService
from modules.ai.service.context_assembly_service import ContextAssemblyService
from modules.ai.service.context_package_service import ContextPackageService
from modules.ai.service.conversation_memory_service import ConversationMemoryService
from modules.ai.service.conversation_message_service import ConversationMessageService
from modules.ai.service.conversation_service import ConversationService
from modules.ai.service.cost_record_service import CostRecordService
from modules.ai.service.embedding_service import EmbeddingService
from modules.ai.service.evaluation_service import EvaluationService
from modules.ai.service.feedback_service import FeedbackService
from modules.ai.service.gateway_policy_service import GatewayPolicyService
from modules.ai.service.guardrail_policy_service import GuardrailPolicyService
from modules.ai.service.invoke_service import InvokeService
from modules.ai.service.knowledge_base_service import KnowledgeBaseService
from modules.ai.service.knowledge_chunk_service import KnowledgeChunkService
from modules.ai.service.knowledge_ingestion_service import KnowledgeIngestionService
from modules.ai.service.knowledge_source_service import KnowledgeSourceService
from modules.ai.service.model_service import ModelService
from modules.ai.service.moderation_policy_service import ModerationPolicyService
from modules.ai.service.multimodal_profile_service import MultimodalProfileService
from modules.ai.service.prompt_template_service import PromptTemplateService
from modules.ai.service.prompt_variable_service import PromptVariableService
from modules.ai.service.prompt_version_service import PromptVersionService
from modules.ai.service.provider_credential_reference_service import (
    ProviderCredentialReferenceService,
)
from modules.ai.service.provider_service import ProviderService
from modules.ai.service.publish_validation_service import PublishValidationService
from modules.ai.service.rate_limit_policy_service import RateLimitPolicyService
from modules.ai.service.routing_rule_service import RoutingRuleService
from modules.ai.service.runtime_resolve_service import RuntimeResolveService
from modules.ai.service.session_service import SessionService
from modules.ai.service.skill_service import SkillService
from modules.ai.service.tool_registry_service import ToolRegistryService
from modules.ai.service.tool_service import ToolService
from modules.ai.service.tool_version_service import ToolVersionService
from modules.ai.service.usage_record_service import UsageRecordService
from modules.ai.service.vector_index_service import VectorIndexService


class AiApplicationService:
    def __init__(self, db: Session) -> None:
        self.providers = ProviderService(db)
        self.models = ModelService(db)
        self.credential_references = ProviderCredentialReferenceService(db)
        self.configurations = ConfigurationService(db)
        self.prompt_templates = PromptTemplateService(db)
        self.prompt_versions = PromptVersionService(db)
        self.prompt_variables = PromptVariableService(db)
        self.gateway_policies = GatewayPolicyService(db)
        self.routing_rules = RoutingRuleService(db)
        self.guardrail_policies = GuardrailPolicyService(db)
        self.moderation_policies = ModerationPolicyService(db)
        self.rate_limit_policies = RateLimitPolicyService(db)
        self.assistants = AssistantService(db)
        self.sessions = SessionService(db)
        self.conversations = ConversationService(db)
        self.conversation_messages = ConversationMessageService(db)
        self.conversation_memories = ConversationMemoryService(db)
        self.context_packages = ContextPackageService(db)
        self.usage_records = UsageRecordService(db)
        self.cost_records = CostRecordService(db)
        self.cache_entries = CacheEntryService(db)
        self.knowledge_bases = KnowledgeBaseService(db)
        self.knowledge_sources = KnowledgeSourceService(db)
        self.knowledge_chunks = KnowledgeChunkService(db)
        self.embeddings = EmbeddingService(db)
        self.vector_indexes = VectorIndexService(db)
        self.knowledge_ingestion = KnowledgeIngestionService(db)
        self.tools = ToolService(db)
        self.tool_versions = ToolVersionService(db)
        self.skills = SkillService(db)
        self.agents = AgentService(db)
        self.agent_versions = AgentVersionService(db)
        self.tool_registry = ToolRegistryService(db)
        self.agent_design = AgentDesignService(db)
        self.evaluations = EvaluationService(db)
        self.feedbacks = FeedbackService(db)
        self.multimodal_profiles = MultimodalProfileService(db)
        self.publish_validation = PublishValidationService(db)
        self.runtime_resolve = RuntimeResolveService(db)
        self.context_assembly = ContextAssemblyService(db)
        self.integration = AiIntegrationService(db)
        self.invoke = InvokeService(db)
