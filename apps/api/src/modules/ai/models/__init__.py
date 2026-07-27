"""AI Platform ORM models — Phase 1–4 (34/34 ERD tables)."""

from modules.ai.models.agent import AiAgent
from modules.ai.models.agent_version import AiAgentVersion
from modules.ai.models.ai_model import AiModel
from modules.ai.models.assistant import AiAssistant
from modules.ai.models.cache_entry import AiCacheEntry
from modules.ai.models.configuration import AiConfiguration
from modules.ai.models.context_package import AiContextPackage
from modules.ai.models.conversation import AiConversation
from modules.ai.models.conversation_memory import AiConversationMemory
from modules.ai.models.conversation_message import AiConversationMessage
from modules.ai.models.cost_record import AiCostRecord
from modules.ai.models.embedding import AiEmbedding
from modules.ai.models.evaluation import AiEvaluation
from modules.ai.models.feedback import AiFeedback
from modules.ai.models.gateway_policy import AiGatewayPolicy
from modules.ai.models.guardrail_policy import AiGuardrailPolicy
from modules.ai.models.knowledge_base import AiKnowledgeBase
from modules.ai.models.knowledge_chunk import AiKnowledgeChunk
from modules.ai.models.knowledge_source import AiKnowledgeSource
from modules.ai.models.moderation_policy import AiModerationPolicy
from modules.ai.models.multimodal_profile import AiMultimodalProfile
from modules.ai.models.prompt_template import AiPromptTemplate
from modules.ai.models.prompt_variable import AiPromptVariable
from modules.ai.models.prompt_version import AiPromptVersion
from modules.ai.models.provider import AiProvider
from modules.ai.models.provider_credential_reference import AiProviderCredentialReference
from modules.ai.models.rate_limit_policy import AiRateLimitPolicy
from modules.ai.models.routing_rule import AiRoutingRule
from modules.ai.models.session import AiSession
from modules.ai.models.skill import AiSkill
from modules.ai.models.tool import AiTool
from modules.ai.models.tool_version import AiToolVersion
from modules.ai.models.usage_record import AiUsageRecord
from modules.ai.models.vector_index import AiVectorIndex

__all__ = [
    "AiProvider",
    "AiModel",
    "AiProviderCredentialReference",
    "AiConfiguration",
    "AiPromptTemplate",
    "AiPromptVersion",
    "AiPromptVariable",
    "AiGatewayPolicy",
    "AiRoutingRule",
    "AiGuardrailPolicy",
    "AiModerationPolicy",
    "AiRateLimitPolicy",
    "AiAssistant",
    "AiSession",
    "AiConversation",
    "AiConversationMessage",
    "AiConversationMemory",
    "AiContextPackage",
    "AiUsageRecord",
    "AiCostRecord",
    "AiCacheEntry",
    "AiKnowledgeBase",
    "AiKnowledgeSource",
    "AiKnowledgeChunk",
    "AiEmbedding",
    "AiVectorIndex",
    "AiTool",
    "AiToolVersion",
    "AiSkill",
    "AiAgent",
    "AiAgentVersion",
    "AiEvaluation",
    "AiFeedback",
    "AiMultimodalProfile",
]
