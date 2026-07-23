"""Low-Code domain entity markers — Phase 1 · 2A."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class FormCategoryIdentity:
    category_id: UUID
    category_code: str


@dataclass
class FormDefinitionIdentity:
    definition_id: UUID
    form_code: str
    module_affinity: str


@dataclass
class FormVersionIdentity:
    version_id: UUID
    definition_id: UUID
    version_number: int
    status: str


@dataclass
class FormSectionIdentity:
    section_id: UUID
    form_version_id: UUID
    section_code: str


@dataclass
class FormFieldIdentity:
    field_id: UUID
    form_version_id: UUID
    field_key: str
    field_type: str


@dataclass
class ComponentIdentity:
    component_id: UUID
    component_code: str
    component_kind: str


@dataclass
class ComponentVersionIdentity:
    version_id: UUID
    component_id: UUID
    version_number: int
    status: str


@dataclass
class DataSourceIdentity:
    data_source_id: UUID
    data_source_code: str
    module_code: str
    entity_type: str


@dataclass
class ExpressionIdentity:
    expression_id: UUID
    expression_code: str
    expression_kind: str
    status: str


@dataclass
class ExpressionBindingIdentity:
    binding_id: UUID
    expression_id: UUID
    target_type: str


@dataclass
class EventHandlerIdentity:
    handler_id: UUID
    event_type: str
    form_version_id: UUID | None


@dataclass
class LocalizationEntryIdentity:
    entry_id: UUID
    owner_type: str
    locale: str
    translation_key: str


@dataclass
class PageDefinitionIdentity:
    definition_id: UUID
    page_code: str


@dataclass
class PageVersionIdentity:
    version_id: UUID
    definition_id: UUID
    version_number: int
    status: str


@dataclass
class PageRegionIdentity:
    region_id: UUID
    page_version_id: UUID
    region_type: str


@dataclass
class PublishHistoryIdentity:
    history_id: UUID
    action: str
    artifact_kind: str


@dataclass
class RuntimeSubmissionIdentity:
    submission_id: UUID
    correlation_id: str
    module_code: str


@dataclass
class PreviewSessionIdentity:
    session_id: UUID
    designer_user_id: UUID
    preview_mode: str
