"""Low-Code domain exceptions."""

from core.exceptions import ConflictException


class InvalidCategoryState(ConflictException):
    def __init__(self, message: str = "Invalid form category state") -> None:
        super().__init__(message)


class InvalidDefinitionState(ConflictException):
    def __init__(self, message: str = "Invalid form definition state") -> None:
        super().__init__(message)


class InvalidVersionState(ConflictException):
    def __init__(self, message: str = "Invalid form version state") -> None:
        super().__init__(message)


class PublishedVersionImmutable(ConflictException):
    def __init__(self, message: str = "Published versions are immutable") -> None:
        super().__init__(message)


class MultiplePublishedVersionsForbidden(ConflictException):
    def __init__(
        self, message: str = "Exactly one Published Version allowed per Form Definition"
    ) -> None:
        super().__init__(message)


class DraftVersionNotExecutable(ConflictException):
    def __init__(
        self, message: str = "Runtime uses Published Version only — draft cannot execute"
    ) -> None:
        super().__init__(message)


class InvalidSectionState(ConflictException):
    def __init__(self, message: str = "Invalid form section state") -> None:
        super().__init__(message)


class InvalidFieldState(ConflictException):
    def __init__(self, message: str = "Invalid form field state") -> None:
        super().__init__(message)


class DuplicateFieldKeyForbidden(ConflictException):
    def __init__(
        self, message: str = "Field key must be unique within a Form Version"
    ) -> None:
        super().__init__(message)


class FormStructureInvalid(ConflictException):
    def __init__(self, message: str = "Form structure validation failed") -> None:
        super().__init__(message)


class InvalidComponentState(ConflictException):
    def __init__(self, message: str = "Invalid component state") -> None:
        super().__init__(message)


class InvalidComponentVersionState(ConflictException):
    def __init__(self, message: str = "Invalid component version state") -> None:
        super().__init__(message)


class PublishedComponentVersionImmutable(ConflictException):
    def __init__(
        self, message: str = "Published component versions are immutable"
    ) -> None:
        super().__init__(message)


class MultiplePublishedComponentVersionsForbidden(ConflictException):
    def __init__(
        self, message: str = "Exactly one Published Version allowed per Component"
    ) -> None:
        super().__init__(message)


class InvalidDataSourceState(ConflictException):
    def __init__(self, message: str = "Invalid data source state") -> None:
        super().__init__(message)


class InvalidExpressionState(ConflictException):
    def __init__(self, message: str = "Invalid expression state") -> None:
        super().__init__(message)


class PublishedExpressionImmutable(ConflictException):
    def __init__(self, message: str = "Published expressions are immutable") -> None:
        super().__init__(message)


class InvalidExpressionBindingState(ConflictException):
    def __init__(self, message: str = "Invalid expression binding state") -> None:
        super().__init__(message)


class InvalidEventHandlerState(ConflictException):
    def __init__(self, message: str = "Invalid event handler state") -> None:
        super().__init__(message)


class InvalidLocalizationEntryState(ConflictException):
    def __init__(self, message: str = "Invalid localization entry state") -> None:
        super().__init__(message)


class PublishedLocalizationImmutable(ConflictException):
    def __init__(
        self, message: str = "Published localization entries are immutable"
    ) -> None:
        super().__init__(message)


class DuplicateLocalizationKeyForbidden(ConflictException):
    def __init__(
        self,
        message: str = "locale + translation_key must be unique within the owner",
    ) -> None:
        super().__init__(message)


class InvalidPageDefinitionState(ConflictException):
    def __init__(self, message: str = "Invalid page definition state") -> None:
        super().__init__(message)


class InvalidPageVersionState(ConflictException):
    def __init__(self, message: str = "Invalid page version state") -> None:
        super().__init__(message)


class PublishedPageVersionImmutable(ConflictException):
    def __init__(self, message: str = "Published page versions are immutable") -> None:
        super().__init__(message)


class MultiplePublishedPageVersionsForbidden(ConflictException):
    def __init__(
        self, message: str = "Exactly one Published Version allowed per Page Definition"
    ) -> None:
        super().__init__(message)


class InvalidPageRegionState(ConflictException):
    def __init__(self, message: str = "Invalid page region state") -> None:
        super().__init__(message)


class InvalidPublishHistoryState(ConflictException):
    def __init__(self, message: str = "Invalid publish history state") -> None:
        super().__init__(message)


class InvalidRuntimeSubmissionState(ConflictException):
    def __init__(self, message: str = "Invalid runtime submission state") -> None:
        super().__init__(message)


class InvalidPreviewSessionState(ConflictException):
    def __init__(self, message: str = "Invalid preview session state") -> None:
        super().__init__(message)
