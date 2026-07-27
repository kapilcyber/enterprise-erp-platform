"""AI Platform domain exceptions."""

from core.exceptions import ConflictException


class InvalidProviderState(ConflictException):
    def __init__(self, message: str = "Invalid AI provider state") -> None:
        super().__init__(message)


class InvalidModelState(ConflictException):
    def __init__(self, message: str = "Invalid AI model state") -> None:
        super().__init__(message)


class InvalidCredentialReferenceState(ConflictException):
    def __init__(
        self, message: str = "Invalid provider credential reference state"
    ) -> None:
        super().__init__(message)


class InvalidConfigurationState(ConflictException):
    def __init__(self, message: str = "Invalid AI configuration state") -> None:
        super().__init__(message)


class InvalidPromptTemplateState(ConflictException):
    def __init__(self, message: str = "Invalid prompt template state") -> None:
        super().__init__(message)


class InvalidPromptVersionState(ConflictException):
    def __init__(self, message: str = "Invalid prompt version state") -> None:
        super().__init__(message)


class PublishedPromptVersionImmutable(ConflictException):
    def __init__(self, message: str = "Published prompt versions are immutable") -> None:
        super().__init__(message)


class MultiplePublishedPromptVersionsForbidden(ConflictException):
    def __init__(
        self,
        message: str = "Exactly one Published Version allowed per Prompt Template",
    ) -> None:
        super().__init__(message)


class InvalidPromptVariableState(ConflictException):
    def __init__(self, message: str = "Invalid prompt variable state") -> None:
        super().__init__(message)


class InvalidGatewayPolicyState(ConflictException):
    def __init__(self, message: str = "Invalid gateway policy state") -> None:
        super().__init__(message)


class PublishedGatewayPolicyImmutable(ConflictException):
    def __init__(self, message: str = "Published gateway policies are immutable") -> None:
        super().__init__(message)


class InvalidRoutingRuleState(ConflictException):
    def __init__(self, message: str = "Invalid routing rule state") -> None:
        super().__init__(message)


class PublishedRoutingRuleImmutable(ConflictException):
    def __init__(self, message: str = "Published routing rules are immutable") -> None:
        super().__init__(message)


class InvalidGuardrailPolicyState(ConflictException):
    def __init__(self, message: str = "Invalid guardrail policy state") -> None:
        super().__init__(message)


class PublishedGuardrailPolicyImmutable(ConflictException):
    def __init__(self, message: str = "Published guardrail policies are immutable") -> None:
        super().__init__(message)


class InvalidModerationPolicyState(ConflictException):
    def __init__(self, message: str = "Invalid moderation policy state") -> None:
        super().__init__(message)


class PublishedModerationPolicyImmutable(ConflictException):
    def __init__(self, message: str = "Published moderation policies are immutable") -> None:
        super().__init__(message)


class InvalidRateLimitPolicyState(ConflictException):
    def __init__(self, message: str = "Invalid rate limit policy state") -> None:
        super().__init__(message)


class PublishedRateLimitPolicyImmutable(ConflictException):
    def __init__(self, message: str = "Published rate limit policies are immutable") -> None:
        super().__init__(message)


class InvalidAssistantState(ConflictException):
    def __init__(self, message: str = "Invalid assistant state") -> None:
        super().__init__(message)


class PublishedAssistantImmutable(ConflictException):
    def __init__(self, message: str = "Published assistants are immutable") -> None:
        super().__init__(message)


class InvalidSessionState(ConflictException):
    def __init__(self, message: str = "Invalid AI session state") -> None:
        super().__init__(message)


class InvalidConversationState(ConflictException):
    def __init__(self, message: str = "Invalid conversation state") -> None:
        super().__init__(message)


class InvalidConversationMessageState(ConflictException):
    def __init__(self, message: str = "Invalid conversation message state") -> None:
        super().__init__(message)


class InvalidConversationMemoryState(ConflictException):
    def __init__(self, message: str = "Invalid conversation memory state") -> None:
        super().__init__(message)


class InvalidContextPackageState(ConflictException):
    def __init__(self, message: str = "Invalid context package state") -> None:
        super().__init__(message)


class InvalidUsageRecordState(ConflictException):
    def __init__(self, message: str = "Invalid usage record state") -> None:
        super().__init__(message)


class InvalidCostRecordState(ConflictException):
    def __init__(self, message: str = "Invalid cost record state") -> None:
        super().__init__(message)


class InvalidCacheEntryState(ConflictException):
    def __init__(self, message: str = "Invalid cache entry state") -> None:
        super().__init__(message)


class InvalidKnowledgeBaseState(ConflictException):
    def __init__(self, message: str = "Invalid knowledge base state") -> None:
        super().__init__(message)


class PublishedKnowledgeBaseImmutable(ConflictException):
    def __init__(self, message: str = "Published knowledge bases are immutable") -> None:
        super().__init__(message)


class InvalidKnowledgeSourceState(ConflictException):
    def __init__(self, message: str = "Invalid knowledge source state") -> None:
        super().__init__(message)


class InvalidKnowledgeChunkState(ConflictException):
    def __init__(self, message: str = "Invalid knowledge chunk state") -> None:
        super().__init__(message)


class InvalidEmbeddingState(ConflictException):
    def __init__(self, message: str = "Invalid embedding state") -> None:
        super().__init__(message)


class InvalidVectorIndexState(ConflictException):
    def __init__(self, message: str = "Invalid vector index state") -> None:
        super().__init__(message)


class InvalidToolState(ConflictException):
    def __init__(self, message: str = "Invalid AI tool state") -> None:
        super().__init__(message)


class PublishedToolImmutable(ConflictException):
    def __init__(self, message: str = "Published tools are immutable") -> None:
        super().__init__(message)


class InvalidToolVersionState(ConflictException):
    def __init__(self, message: str = "Invalid AI tool version state") -> None:
        super().__init__(message)


class PublishedToolVersionImmutable(ConflictException):
    def __init__(self, message: str = "Published tool versions are immutable") -> None:
        super().__init__(message)


class InvalidSkillState(ConflictException):
    def __init__(self, message: str = "Invalid AI skill state") -> None:
        super().__init__(message)


class PublishedSkillImmutable(ConflictException):
    def __init__(self, message: str = "Published skills are immutable") -> None:
        super().__init__(message)


class InvalidAgentState(ConflictException):
    def __init__(self, message: str = "Invalid AI agent state") -> None:
        super().__init__(message)


class InvalidAgentVersionState(ConflictException):
    def __init__(self, message: str = "Invalid AI agent version state") -> None:
        super().__init__(message)


class PublishedAgentVersionImmutable(ConflictException):
    def __init__(self, message: str = "Published agent versions are immutable") -> None:
        super().__init__(message)


class ToolAllowListViolation(ConflictException):
    def __init__(self, message: str = "Tool allow-list validation failed") -> None:
        super().__init__(message)


class InvalidEvaluationState(ConflictException):
    def __init__(self, message: str = "Invalid AI evaluation state") -> None:
        super().__init__(message)


class CompletedEvaluationImmutable(ConflictException):
    def __init__(self, message: str = "Completed evaluations are immutable") -> None:
        super().__init__(message)


class InvalidFeedbackState(ConflictException):
    def __init__(self, message: str = "Invalid AI feedback state") -> None:
        super().__init__(message)


class InvalidMultimodalProfileState(ConflictException):
    def __init__(self, message: str = "Invalid multimodal profile state") -> None:
        super().__init__(message)


class PublishedMultimodalProfileImmutable(ConflictException):
    def __init__(self, message: str = "Published multimodal profiles are immutable") -> None:
        super().__init__(message)
