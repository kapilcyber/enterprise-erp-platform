"""Low-Code Pydantic schemas — Phase 1."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- Category ---


class FormCategoryCreate(BaseModel):
    company_id: UUID | None = None
    category_code: str | None = None
    category_name: str
    description: str | None = None
    status: str | None = "active"
    sort_order: int | None = 0


class FormCategoryUpdate(BaseModel):
    category_name: str | None = None
    description: str | None = None
    status: str | None = None
    sort_order: int | None = None
    version: int | None = None


class FormCategoryResponse(OrmModel):
    id: UUID
    company_id: UUID
    category_code: str
    category_name: str
    description: str | None = None
    status: str
    sort_order: int
    version: int
    is_deleted: bool | None = None


# --- Definition ---


class FormDefinitionCreate(BaseModel):
    company_id: UUID | None = None
    form_code: str | None = None
    form_name: str
    description: str | None = None
    status: str | None = "draft"
    category_id: UUID | None = None
    module_affinity: str = Field(default="general", min_length=1, max_length=50)
    entity_type: str | None = None


class FormDefinitionUpdate(BaseModel):
    form_name: str | None = None
    description: str | None = None
    status: str | None = None
    category_id: UUID | None = None
    module_affinity: str | None = None
    entity_type: str | None = None
    version: int | None = None


class FormDefinitionResponse(OrmModel):
    id: UUID
    company_id: UUID
    form_code: str
    form_name: str
    description: str | None = None
    status: str
    category_id: UUID | None = None
    module_affinity: str
    entity_type: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Version ---


class FormVersionCreate(BaseModel):
    definition_id: UUID
    company_id: UUID | None = None
    version_label: str | None = None
    change_notes: str | None = None


class FormVersionUpdate(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    version: int | None = None


class FormVersionClone(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    clone_reason: str | None = None


class FormVersionPublish(BaseModel):
    publish_reason: str | None = None


class FormVersionRetire(BaseModel):
    retire_reason: str | None = None


class FormVersionResponse(OrmModel):
    id: UUID
    company_id: UUID
    definition_id: UUID
    version_code: str
    version_number: int
    version_label: str | None = None
    change_notes: str | None = None
    status: str
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    cloned_from_version_id: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    clone_reason: str | None = None
    version: int


# --- Section (Phase 2A) ---


class FormSectionCreate(BaseModel):
    form_version_id: UUID
    company_id: UUID | None = None
    section_code: str | None = None
    section_name: str
    description: str | None = None
    status: str | None = "active"
    display_order: int | None = 0


class FormSectionUpdate(BaseModel):
    section_name: str | None = None
    description: str | None = None
    status: str | None = None
    display_order: int | None = None
    version: int | None = None


class FormSectionResponse(OrmModel):
    id: UUID
    company_id: UUID
    form_version_id: UUID
    section_code: str
    section_name: str
    description: str | None = None
    status: str
    display_order: int
    version: int
    is_deleted: bool | None = None


# --- Field (Phase 2A) ---


class FormFieldCreate(BaseModel):
    form_version_id: UUID
    company_id: UUID | None = None
    field_code: str | None = None
    field_key: str = Field(..., min_length=1, max_length=100)
    field_label: str
    field_type: str
    description: str | None = None
    help_text: str | None = None
    placeholder: str | None = None
    status: str | None = "active"
    display_order: int | None = 0
    is_required: bool | None = False
    is_readonly: bool | None = False
    is_hidden: bool | None = False
    section_id: UUID | None = None
    component_version_id: UUID | None = None
    data_source_id: UUID | None = None
    validation_rules_json: str | None = None
    binding_json: str | None = None
    options_json: str | None = None
    document_ref_uuid: UUID | None = None


class FormFieldUpdate(BaseModel):
    field_key: str | None = None
    field_label: str | None = None
    field_type: str | None = None
    description: str | None = None
    help_text: str | None = None
    placeholder: str | None = None
    status: str | None = None
    display_order: int | None = None
    is_required: bool | None = None
    is_readonly: bool | None = None
    is_hidden: bool | None = None
    section_id: UUID | None = None
    component_version_id: UUID | None = None
    data_source_id: UUID | None = None
    validation_rules_json: str | None = None
    binding_json: str | None = None
    options_json: str | None = None
    document_ref_uuid: UUID | None = None
    version: int | None = None


class FormFieldResponse(OrmModel):
    id: UUID
    company_id: UUID
    form_version_id: UUID
    section_id: UUID | None = None
    component_version_id: UUID | None = None
    data_source_id: UUID | None = None
    field_code: str
    field_key: str
    field_label: str
    field_type: str
    description: str | None = None
    help_text: str | None = None
    placeholder: str | None = None
    status: str
    display_order: int
    is_required: bool
    is_readonly: bool
    is_hidden: bool
    validation_rules_json: str | None = None
    binding_json: str | None = None
    options_json: str | None = None
    document_ref_uuid: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Component (Phase 2B) ---


class ComponentCreate(BaseModel):
    company_id: UUID | None = None
    component_code: str | None = None
    component_name: str
    component_kind: str
    description: str | None = None
    status: str | None = "draft"


class ComponentUpdate(BaseModel):
    component_name: str | None = None
    component_kind: str | None = None
    description: str | None = None
    status: str | None = None
    version: int | None = None


class ComponentResponse(OrmModel):
    id: UUID
    company_id: UUID
    component_code: str
    component_name: str
    component_kind: str
    description: str | None = None
    status: str
    version: int
    is_deleted: bool | None = None


class ComponentVersionCreate(BaseModel):
    component_id: UUID
    company_id: UUID | None = None
    version_label: str | None = None
    change_notes: str | None = None
    properties_json: str | None = None
    default_props_json: str | None = None


class ComponentVersionUpdate(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    properties_json: str | None = None
    default_props_json: str | None = None
    version: int | None = None


class ComponentVersionClone(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    clone_reason: str | None = None


class ComponentVersionPublish(BaseModel):
    publish_reason: str | None = None


class ComponentVersionRetire(BaseModel):
    retire_reason: str | None = None


class ComponentVersionResponse(OrmModel):
    id: UUID
    company_id: UUID
    component_id: UUID
    version_code: str
    version_number: int
    version_label: str | None = None
    change_notes: str | None = None
    status: str
    properties_json: str | None = None
    default_props_json: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    cloned_from_version_id: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    clone_reason: str | None = None
    version: int


# --- Data Source (Phase 2C) ---


class DataSourceCreate(BaseModel):
    company_id: UUID | None = None
    data_source_code: str | None = None
    data_source_name: str
    description: str | None = None
    status: str | None = "draft"
    module_code: str = Field(..., min_length=1, max_length=50)
    entity_type: str = Field(..., min_length=1, max_length=100)
    allowed_operations: str | None = "read,lookup"
    attribute_catalog_json: str | None = None


class DataSourceUpdate(BaseModel):
    data_source_name: str | None = None
    description: str | None = None
    module_code: str | None = None
    entity_type: str | None = None
    allowed_operations: str | None = None
    attribute_catalog_json: str | None = None
    version: int | None = None


class DataSourceResponse(OrmModel):
    id: UUID
    company_id: UUID
    data_source_code: str
    data_source_name: str
    description: str | None = None
    status: str
    module_code: str
    entity_type: str
    allowed_operations: str
    attribute_catalog_json: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Expression (Phase 2C) ---


class ExpressionCreate(BaseModel):
    company_id: UUID | None = None
    expression_code: str | None = None
    expression_name: str
    expression_kind: str
    description: str | None = None
    expression_body: str
    status: str | None = "draft"


class ExpressionUpdate(BaseModel):
    expression_name: str | None = None
    expression_kind: str | None = None
    description: str | None = None
    expression_body: str | None = None
    version: int | None = None


class ExpressionPublish(BaseModel):
    publish_reason: str | None = None


class ExpressionRetire(BaseModel):
    retire_reason: str | None = None


class ExpressionResponse(OrmModel):
    id: UUID
    company_id: UUID
    expression_code: str
    expression_name: str
    expression_kind: str
    description: str | None = None
    expression_body: str
    status: str
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Expression Binding (Phase 2C) ---


class ExpressionBindingCreate(BaseModel):
    company_id: UUID | None = None
    binding_code: str | None = None
    expression_id: UUID
    target_type: str
    form_version_id: UUID | None = None
    section_id: UUID | None = None
    field_id: UUID | None = None
    page_version_id: UUID | None = None
    status: str | None = "active"
    sort_order: int | None = 0
    notes: str | None = None


class ExpressionBindingUpdate(BaseModel):
    status: str | None = None
    sort_order: int | None = None
    notes: str | None = None
    version: int | None = None


class ExpressionBindingResponse(OrmModel):
    id: UUID
    company_id: UUID
    binding_code: str
    expression_id: UUID
    target_type: str
    form_version_id: UUID | None = None
    section_id: UUID | None = None
    field_id: UUID | None = None
    page_version_id: UUID | None = None
    status: str
    sort_order: int
    notes: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Event Handler (Phase 3A) ---


class EventHandlerCreate(BaseModel):
    company_id: UUID | None = None
    handler_code: str | None = None
    event_type: str
    custom_event_name: str | None = None
    target_type: str
    form_version_id: UUID | None = None
    section_id: UUID | None = None
    field_id: UUID | None = None
    page_version_id: UUID | None = None
    status: str | None = "active"
    execution_order: int | None = 0
    is_enabled: bool | None = True
    metadata_json: str | None = None
    notes: str | None = None


class EventHandlerUpdate(BaseModel):
    event_type: str | None = None
    custom_event_name: str | None = None
    status: str | None = None
    execution_order: int | None = None
    is_enabled: bool | None = None
    metadata_json: str | None = None
    notes: str | None = None
    version: int | None = None


class EventHandlerResponse(OrmModel):
    id: UUID
    company_id: UUID
    handler_code: str
    event_type: str
    custom_event_name: str | None = None
    target_type: str
    form_version_id: UUID | None = None
    section_id: UUID | None = None
    field_id: UUID | None = None
    page_version_id: UUID | None = None
    status: str
    execution_order: int
    is_enabled: bool
    metadata_json: str | None = None
    notes: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Localization Entry (Phase 3A) ---


class LocalizationEntryCreate(BaseModel):
    company_id: UUID | None = None
    entry_code: str | None = None
    owner_type: str
    locale: str = Field(..., min_length=1, max_length=20)
    translation_key: str = Field(..., min_length=1, max_length=255)
    translated_value: str
    form_version_id: UUID | None = None
    section_id: UUID | None = None
    field_id: UUID | None = None
    component_id: UUID | None = None
    page_version_id: UUID | None = None
    status: str | None = "draft"
    notes: str | None = None


class LocalizationEntryUpdate(BaseModel):
    locale: str | None = None
    translation_key: str | None = None
    translated_value: str | None = None
    notes: str | None = None
    version: int | None = None


class LocalizationEntryPublish(BaseModel):
    publish_reason: str | None = None


class LocalizationEntryRetire(BaseModel):
    retire_reason: str | None = None


class LocalizationEntryResponse(OrmModel):
    id: UUID
    company_id: UUID
    entry_code: str
    owner_type: str
    owner_ref_id: UUID
    locale: str
    translation_key: str
    translated_value: str
    form_version_id: UUID | None = None
    section_id: UUID | None = None
    field_id: UUID | None = None
    component_id: UUID | None = None
    page_version_id: UUID | None = None
    status: str
    notes: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Page Definition (Phase 3B) ---


class PageDefinitionCreate(BaseModel):
    company_id: UUID | None = None
    page_code: str | None = None
    page_name: str
    description: str | None = None
    status: str | None = "draft"
    category_id: UUID | None = None


class PageDefinitionUpdate(BaseModel):
    page_name: str | None = None
    description: str | None = None
    status: str | None = None
    category_id: UUID | None = None
    version: int | None = None


class PageDefinitionResponse(OrmModel):
    id: UUID
    company_id: UUID
    page_code: str
    page_name: str
    description: str | None = None
    status: str
    category_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


class PageVersionCreate(BaseModel):
    definition_id: UUID
    company_id: UUID | None = None
    version_label: str | None = None
    change_notes: str | None = None
    layout_json: str | None = None


class PageVersionUpdate(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    layout_json: str | None = None
    version: int | None = None


class PageVersionClone(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    clone_reason: str | None = None


class PageVersionPublish(BaseModel):
    publish_reason: str | None = None


class PageVersionRetire(BaseModel):
    retire_reason: str | None = None


class PageVersionResponse(OrmModel):
    id: UUID
    company_id: UUID
    definition_id: UUID
    version_code: str
    version_number: int
    version_label: str | None = None
    change_notes: str | None = None
    status: str
    layout_json: str | None = None
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    cloned_from_version_id: UUID | None = None
    publish_reason: str | None = None
    retire_reason: str | None = None
    clone_reason: str | None = None
    version: int


class PageRegionCreate(BaseModel):
    page_version_id: UUID
    company_id: UUID | None = None
    region_code: str | None = None
    region_name: str
    region_type: str
    description: str | None = None
    status: str | None = "active"
    display_order: int | None = 0
    layout_json: str | None = None
    embedded_form_version_id: UUID | None = None
    embedded_component_version_id: UUID | None = None


class PageRegionUpdate(BaseModel):
    region_name: str | None = None
    region_type: str | None = None
    description: str | None = None
    status: str | None = None
    display_order: int | None = None
    layout_json: str | None = None
    embedded_form_version_id: UUID | None = None
    embedded_component_version_id: UUID | None = None
    version: int | None = None


class PageRegionResponse(OrmModel):
    id: UUID
    company_id: UUID
    page_version_id: UUID
    region_code: str
    region_name: str
    region_type: str
    description: str | None = None
    status: str
    display_order: int
    layout_json: str | None = None
    embedded_form_version_id: UUID | None = None
    embedded_component_version_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Publish History (Phase 4) ---


class PublishHistoryResponse(OrmModel):
    id: UUID
    company_id: UUID
    history_code: str
    artifact_kind: str
    action: str
    reason: str | None = None
    occurred_at: datetime
    performed_by: UUID
    form_definition_id: UUID | None = None
    page_definition_id: UUID | None = None
    from_version_id: UUID | None = None
    to_version_id: UUID | None = None
    version: int


# --- Runtime Submission (Phase 4) ---


class RuntimeSubmissionCreate(BaseModel):
    company_id: UUID | None = None
    submission_code: str | None = None
    correlation_id: str | None = None
    form_version_id: UUID | None = None
    page_version_id: UUID | None = None
    module_code: str = Field(..., min_length=1, max_length=50)
    entity_id: UUID
    bpm_task_id: UUID | None = None
    submission_status: str | None = "received"
    validation_result_json: str | None = None
    field_values_snapshot_json: str | None = None
    metadata_json: str | None = None


class RuntimeSubmissionStatusUpdate(BaseModel):
    submission_status: str
    validation_result_json: str | None = None
    metadata_json: str | None = None


class RuntimeSubmissionResponse(OrmModel):
    id: UUID
    company_id: UUID
    submission_code: str
    correlation_id: str
    submission_status: str
    form_version_id: UUID | None = None
    page_version_id: UUID | None = None
    module_code: str
    entity_id: UUID
    bpm_task_id: UUID | None = None
    validation_result_json: str | None = None
    field_values_snapshot_json: str | None = None
    metadata_json: str | None = None
    version: int
    is_deleted: bool | None = None


# --- Preview Session (Phase 4) ---


class PreviewSessionCreate(BaseModel):
    company_id: UUID | None = None
    session_code: str | None = None
    preview_mode: str = "draft"
    form_version_id: UUID | None = None
    page_version_id: UUID | None = None
    designer_user_id: UUID | None = None
    ttl_minutes: int | None = 60
    sample_context_json: str | None = None
    notes: str | None = None


class PreviewSessionResponse(OrmModel):
    id: UUID
    company_id: UUID
    session_code: str
    preview_mode: str
    status: str
    designer_user_id: UUID
    expires_at: datetime
    sample_context_json: str | None = None
    notes: str | None = None
    form_version_id: UUID | None = None
    page_version_id: UUID | None = None
    closed_at: datetime | None = None
    version: int
    is_deleted: bool | None = None
