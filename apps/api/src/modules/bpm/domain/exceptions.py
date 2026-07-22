"""BPM domain exceptions."""

from core.exceptions import ConflictException


class InvalidCategoryState(ConflictException):
    def __init__(self, message: str = "Invalid workflow category state") -> None:
        super().__init__(message)


class InvalidTemplateState(ConflictException):
    def __init__(self, message: str = "Invalid workflow template state") -> None:
        super().__init__(message)


class InvalidDefinitionState(ConflictException):
    def __init__(self, message: str = "Invalid workflow definition state") -> None:
        super().__init__(message)


class InvalidVersionState(ConflictException):
    def __init__(self, message: str = "Invalid workflow version state") -> None:
        super().__init__(message)


class PublishedVersionImmutable(ConflictException):
    def __init__(self, message: str = "Published versions are immutable") -> None:
        super().__init__(message)


class MultiplePublishedVersionsForbidden(ConflictException):
    def __init__(
        self, message: str = "Exactly one Published Version allowed per Definition"
    ) -> None:
        super().__init__(message)


class InvalidDesignerNodeState(ConflictException):
    def __init__(self, message: str = "Invalid designer node state") -> None:
        super().__init__(message)


class InvalidDesignerTransitionState(ConflictException):
    def __init__(self, message: str = "Invalid designer transition state") -> None:
        super().__init__(message)


class DesignerGraphInvalid(ConflictException):
    def __init__(self, message: str = "Designer graph validation failed") -> None:
        super().__init__(message)


class DuplicateTransitionForbidden(ConflictException):
    def __init__(self, message: str = "Duplicate transition between nodes is forbidden") -> None:
        super().__init__(message)


class InvalidDecisionTableState(ConflictException):
    def __init__(self, message: str = "Invalid decision table state") -> None:
        super().__init__(message)


class InvalidBusinessRuleState(ConflictException):
    def __init__(self, message: str = "Invalid business rule state") -> None:
        super().__init__(message)


class InvalidWorkflowVariableState(ConflictException):
    def __init__(self, message: str = "Invalid workflow variable state") -> None:
        super().__init__(message)


class InvalidFormReferenceState(ConflictException):
    def __init__(self, message: str = "Invalid form reference state") -> None:
        super().__init__(message)


class InvalidAssignmentRuleState(ConflictException):
    def __init__(self, message: str = "Invalid assignment rule state") -> None:
        super().__init__(message)


class InvalidEscalationPolicyState(ConflictException):
    def __init__(self, message: str = "Invalid escalation policy state") -> None:
        super().__init__(message)


class InvalidSlaPolicyState(ConflictException):
    def __init__(self, message: str = "Invalid SLA policy state") -> None:
        super().__init__(message)


class InvalidWorkflowTriggerState(ConflictException):
    def __init__(self, message: str = "Invalid workflow trigger state") -> None:
        super().__init__(message)


class InvalidNotificationTemplateState(ConflictException):
    def __init__(self, message: str = "Invalid notification template state") -> None:
        super().__init__(message)


class InvalidWorkflowInstanceState(ConflictException):
    def __init__(self, message: str = "Invalid workflow instance state") -> None:
        super().__init__(message)


class InvalidWorkflowTaskState(ConflictException):
    def __init__(self, message: str = "Invalid workflow task state") -> None:
        super().__init__(message)


class InvalidWorkflowHistoryState(ConflictException):
    def __init__(self, message: str = "Invalid workflow history state") -> None:
        super().__init__(message)


class HistoryAppendOnlyViolation(ConflictException):
    def __init__(self, message: str = "Workflow history is append-only") -> None:
        super().__init__(message)


class InvalidTaskDelegationState(ConflictException):
    def __init__(self, message: str = "Invalid task delegation state") -> None:
        super().__init__(message)


class DraftVersionNotExecutable(ConflictException):
    def __init__(
        self, message: str = "Runtime uses Published Version only — draft cannot execute"
    ) -> None:
        super().__init__(message)


class InvalidSimulationRunState(ConflictException):
    def __init__(self, message: str = "Invalid simulation run state") -> None:
        super().__init__(message)


class SimulationNotAllowed(ConflictException):
    def __init__(
        self, message: str = "Simulation allowed only on Draft or Published versions"
    ) -> None:
        super().__init__(message)
