"""Low-Code domain enums per FRD-26 / ERD-26 Phase 1–4."""

from enum import Enum


class CategoryStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class DefinitionStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


class VersionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


class SectionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class FieldStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class FieldType(str, Enum):
    TEXT = "text"
    TEXTAREA = "textarea"
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    INTEGER = "integer"
    DECIMAL = "decimal"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    LOOKUP = "lookup"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"
    ATTACHMENT = "attachment"
    DISPLAY = "display"
    HIDDEN = "hidden"


FIELD_TYPE_VALUES: frozenset[str] = frozenset(t.value for t in FieldType)


class ComponentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


class ComponentKind(str, Enum):
    TEXT = "text"
    TEXTAREA = "textarea"
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    DATE = "date"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    LOOKUP = "lookup"
    GRID = "grid"
    SECTION = "section"
    DIVIDER = "divider"
    ATTACHMENT = "attachment"
    DISPLAY = "display"
    CUSTOM = "custom"


COMPONENT_KIND_VALUES: frozenset[str] = frozenset(t.value for t in ComponentKind)


class LowcodeEntityType(str, Enum):
    FORM_CATEGORY = "form_category"
    FORM_DEFINITION = "form_definition"
    FORM_VERSION = "form_version"
    FORM_SECTION = "form_section"
    FORM_FIELD = "form_field"
    COMPONENT = "component"
    COMPONENT_VERSION = "component_version"
    DATA_SOURCE = "data_source"
    EXPRESSION = "expression"
    EXPRESSION_BINDING = "expression_binding"
    EVENT_HANDLER = "event_handler"
    LOCALIZATION_ENTRY = "localization_entry"
    PAGE_DEFINITION = "page_definition"
    PAGE_VERSION = "page_version"
    PAGE_REGION = "page_region"
    PUBLISH_HISTORY = "publish_history"
    RUNTIME_SUBMISSION = "runtime_submission"
    PREVIEW_SESSION = "preview_session"


class DataSourceStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


class ExpressionKind(str, Enum):
    VISIBILITY = "visibility"
    REQUIRED = "required"
    ENABLE = "enable"
    DISABLE = "disable"
    DEFAULT = "default"
    CALCULATE = "calculate"


EXPRESSION_KIND_VALUES: frozenset[str] = frozenset(t.value for t in ExpressionKind)


class BindingTargetType(str, Enum):
    FORM_VERSION = "form_version"
    SECTION = "section"
    FIELD = "field"
    PAGE_VERSION = "page_version"  # future — UUID metadata only in Phase 2C


BINDING_TARGET_TYPE_VALUES: frozenset[str] = frozenset(t.value for t in BindingTargetType)


class BindingStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# Data-source contract ops — registry metadata only (no execution)
DATA_SOURCE_OPERATION_VALUES: frozenset[str] = frozenset({"read", "write", "lookup"})


class EventType(str, Enum):
    ON_LOAD = "onLoad"
    ON_CHANGE = "onChange"
    ON_FOCUS = "onFocus"
    ON_BLUR = "onBlur"
    ON_VALIDATE = "onValidate"
    ON_SUBMIT = "onSubmit"
    ON_CANCEL = "onCancel"
    CUSTOM = "custom"


EVENT_TYPE_VALUES: frozenset[str] = frozenset(t.value for t in EventType)


class EventHandlerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class LocalizationOwnerType(str, Enum):
    FORM = "form"
    FIELD = "field"
    SECTION = "section"
    COMPONENT = "component"
    PAGE = "page"  # future — page_version UUID metadata only


LOCALIZATION_OWNER_TYPE_VALUES: frozenset[str] = frozenset(
    t.value for t in LocalizationOwnerType
)


class LocalizationEntryStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


class PageDefinitionStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


class RegionType(str, Enum):
    HEADER = "header"
    CONTENT = "content"
    SIDEBAR = "sidebar"
    FOOTER = "footer"
    MODAL = "modal"
    TAB = "tab"
    WIZARD_STEP = "wizard_step"
    CUSTOM = "custom"


REGION_TYPE_VALUES: frozenset[str] = frozenset(t.value for t in RegionType)


class RegionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class PublishHistoryAction(str, Enum):
    PUBLISH = "publish"
    RETIRE = "retire"


PUBLISH_HISTORY_ACTION_VALUES: frozenset[str] = frozenset(
    t.value for t in PublishHistoryAction
)


class ArtifactKind(str, Enum):
    FORM = "form"
    PAGE = "page"


ARTIFACT_KIND_VALUES: frozenset[str] = frozenset(t.value for t in ArtifactKind)


class SubmissionStatus(str, Enum):
    RECEIVED = "received"
    VALIDATED = "validated"
    FAILED = "failed"
    HANDOFF = "handoff"
    CANCELLED = "cancelled"


SUBMISSION_STATUS_VALUES: frozenset[str] = frozenset(t.value for t in SubmissionStatus)


class PreviewMode(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


PREVIEW_MODE_VALUES: frozenset[str] = frozenset(t.value for t in PreviewMode)


class PreviewSessionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CLOSED = "closed"


PREVIEW_SESSION_STATUS_VALUES: frozenset[str] = frozenset(
    t.value for t in PreviewSessionStatus
)


# prefix, width, include_year
CODE_PREFIXES: dict[LowcodeEntityType, tuple[str, int, bool]] = {
    LowcodeEntityType.FORM_CATEGORY: ("FC-", 6, True),
    LowcodeEntityType.FORM_DEFINITION: ("FRM-", 6, True),
    LowcodeEntityType.FORM_VERSION: ("FVER-", 6, True),
    LowcodeEntityType.FORM_SECTION: ("SEC-", 6, True),
    LowcodeEntityType.FORM_FIELD: ("FLD-", 6, True),
    LowcodeEntityType.COMPONENT: ("CMP-", 6, True),
    LowcodeEntityType.COMPONENT_VERSION: ("CVER-", 6, True),
    LowcodeEntityType.DATA_SOURCE: ("DS-", 6, True),
    LowcodeEntityType.EXPRESSION: ("EXP-", 6, True),
    LowcodeEntityType.EXPRESSION_BINDING: ("EXB-", 6, True),
    LowcodeEntityType.EVENT_HANDLER: ("EVT-", 6, True),
    LowcodeEntityType.LOCALIZATION_ENTRY: ("LOC-", 6, True),
    LowcodeEntityType.PAGE_DEFINITION: ("PG-", 6, True),
    LowcodeEntityType.PAGE_VERSION: ("PVER-", 6, True),
    LowcodeEntityType.PAGE_REGION: ("PREG-", 6, True),
    LowcodeEntityType.PUBLISH_HISTORY: ("PH-", 6, True),
    LowcodeEntityType.RUNTIME_SUBMISSION: ("RSUB-", 6, True),
    LowcodeEntityType.PREVIEW_SESSION: ("PREV-", 6, True),
}
