"""BPM Pydantic schemas — Phase 1 + 1.5."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PageMeta(BaseModel):
    total: int
    page: int
    page_size: int
    sort_by: str | None = None
    sort_dir: str = "asc"


# --- Category ---


class WorkflowCategoryCreate(BaseModel):
    company_id: UUID | None = None
    category_code: str | None = None
    category_name: str
    description: str | None = None
    status: str | None = "active"
    sort_order: int | None = 0
    owner_employee_id: UUID | None = None


class WorkflowCategoryUpdate(BaseModel):
    category_name: str | None = None
    description: str | None = None
    status: str | None = None
    sort_order: int | None = None
    owner_employee_id: UUID | None = None
    version: int | None = None


class WorkflowCategoryResponse(OrmModel):
    id: UUID
    company_id: UUID
    category_code: str
    category_name: str
    description: str | None = None
    status: str
    sort_order: int
    owner_employee_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Template ---


class WorkflowTemplateCreate(BaseModel):
    company_id: UUID | None = None
    template_code: str | None = None
    template_name: str
    description: str | None = None
    status: str | None = "draft"
    category_id: UUID | None = None
    module_code: str | None = None
    entity_type: str | None = None
    owner_employee_id: UUID | None = None


class WorkflowTemplateUpdate(BaseModel):
    template_name: str | None = None
    description: str | None = None
    status: str | None = None
    category_id: UUID | None = None
    module_code: str | None = None
    entity_type: str | None = None
    owner_employee_id: UUID | None = None
    version: int | None = None


class WorkflowTemplateCopy(BaseModel):
    template_name: str | None = None


class WorkflowTemplateImportPayload(BaseModel):
    company_id: UUID | None = None
    payload: dict[str, Any]


class WorkflowTemplateResponse(OrmModel):
    id: UUID
    company_id: UUID
    template_code: str
    template_name: str
    description: str | None = None
    status: str
    category_id: UUID | None = None
    module_code: str | None = None
    entity_type: str | None = None
    owner_employee_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


class TemplatePopularItem(BaseModel):
    template: WorkflowTemplateResponse
    usage_count: int


# --- Definition ---


class WorkflowDefinitionCreate(BaseModel):
    company_id: UUID | None = None
    definition_code: str | None = None
    definition_name: str
    description: str | None = None
    status: str | None = "draft"
    template_id: UUID | None = None
    module_code: str = Field(..., min_length=1, max_length=50)
    entity_type: str = Field(..., min_length=1, max_length=100)
    owner_employee_id: UUID | None = None
    department_id: UUID | None = None


class WorkflowDefinitionUpdate(BaseModel):
    definition_name: str | None = None
    description: str | None = None
    status: str | None = None
    template_id: UUID | None = None
    module_code: str | None = None
    entity_type: str | None = None
    owner_employee_id: UUID | None = None
    department_id: UUID | None = None
    version: int | None = None


class WorkflowDefinitionResponse(OrmModel):
    id: UUID
    company_id: UUID
    definition_code: str
    definition_name: str
    description: str | None = None
    status: str
    template_id: UUID | None = None
    module_code: str
    entity_type: str
    owner_employee_id: UUID | None = None
    department_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Version ---


class WorkflowVersionCreate(BaseModel):
    definition_id: UUID
    company_id: UUID | None = None
    version_label: str | None = None
    change_notes: str | None = None


class WorkflowVersionUpdate(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    version: int | None = None


class WorkflowVersionClone(BaseModel):
    version_label: str | None = None
    change_notes: str | None = None
    clone_reason: str | None = None


class WorkflowVersionPublish(BaseModel):
    publish_reason: str | None = None


class WorkflowVersionRetire(BaseModel):
    retire_reason: str | None = None


class WorkflowVersionResponse(OrmModel):
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


class BpmDashboardSummaryResponse(BaseModel):
    categories: int
    templates: int
    definitions: int
    draft: int
    published: int
    retired: int


# --- Designer Node (Phase 2A) ---


class DesignerNodeCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    node_code: str | None = None
    node_name: str
    node_type: str
    description: str | None = None
    status: str | None = "active"
    sort_order: int | None = 0
    position_x: float | None = 0.0
    position_y: float | None = 0.0
    config_json: str | None = None


class DesignerNodeUpdate(BaseModel):
    node_name: str | None = None
    node_type: str | None = None
    description: str | None = None
    status: str | None = None
    sort_order: int | None = None
    position_x: float | None = None
    position_y: float | None = None
    config_json: str | None = None
    version: int | None = None


class DesignerNodeResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    node_code: str
    node_name: str
    node_type: str
    description: str | None = None
    status: str
    sort_order: int
    position_x: float
    position_y: float
    config_json: str | None = None
    version: int


# --- Designer Transition (Phase 2A) ---


class DesignerTransitionCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    from_node_id: UUID
    to_node_id: UUID
    transition_code: str | None = None
    transition_name: str
    transition_type: str = "sequential"
    description: str | None = None
    status: str | None = "active"
    priority: int | None = 0
    condition_expression: str | None = None
    decision_table_id: UUID | None = None


class DesignerTransitionUpdate(BaseModel):
    from_node_id: UUID | None = None
    to_node_id: UUID | None = None
    transition_name: str | None = None
    transition_type: str | None = None
    description: str | None = None
    status: str | None = None
    priority: int | None = None
    condition_expression: str | None = None
    decision_table_id: UUID | None = None
    version: int | None = None


class DesignerTransitionResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    from_node_id: UUID
    to_node_id: UUID
    transition_code: str
    transition_name: str
    transition_type: str
    description: str | None = None
    status: str
    priority: int
    condition_expression: str | None = None
    decision_table_id: UUID | None = None
    version: int


class GraphValidateRequest(BaseModel):
    allow_cycles: bool = False


# --- Decision Table (Phase 2B) ---


class DecisionTableCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    table_code: str | None = None
    table_name: str
    description: str | None = None
    status: str | None = "enabled"
    priority: int | None = 0
    evaluation_order: int | None = 0
    rows_json: str | None = None


class DecisionTableUpdate(BaseModel):
    table_name: str | None = None
    description: str | None = None
    status: str | None = None
    priority: int | None = None
    evaluation_order: int | None = None
    rows_json: str | None = None
    version: int | None = None


class DecisionTableResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    table_code: str
    table_name: str
    description: str | None = None
    status: str
    priority: int
    evaluation_order: int
    rows_json: str | None = None
    version: int


class DecisionTableRowsReplace(BaseModel):
    rows: list[dict]


class DecisionTableRowPayload(BaseModel):
    row: dict


# --- Business Rule (Phase 2B) ---


class BusinessRuleCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    rule_code: str | None = None
    rule_name: str
    rule_type: str
    expression: str
    description: str | None = None
    status: str | None = "draft"
    priority: int | None = 0
    decision_table_id: UUID | None = None


class BusinessRuleUpdate(BaseModel):
    rule_name: str | None = None
    rule_type: str | None = None
    expression: str | None = None
    description: str | None = None
    status: str | None = None
    priority: int | None = None
    decision_table_id: UUID | None = None
    version: int | None = None


class BusinessRuleResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    rule_code: str
    rule_name: str
    rule_type: str
    expression: str
    description: str | None = None
    status: str
    priority: int
    decision_table_id: UUID | None = None
    version: int


# --- Workflow Variable (Phase 2B) ---


class WorkflowVariableCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    variable_key: str
    variable_name: str
    variable_type: str
    description: str | None = None
    default_value: str | None = None
    is_required: bool | None = False
    is_encrypted: bool | None = False
    status: str | None = "active"


class WorkflowVariableUpdate(BaseModel):
    variable_key: str | None = None
    variable_name: str | None = None
    variable_type: str | None = None
    description: str | None = None
    default_value: str | None = None
    is_required: bool | None = None
    is_encrypted: bool | None = None
    status: str | None = None
    version: int | None = None


class WorkflowVariableResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    variable_key: str
    variable_name: str
    variable_type: str
    description: str | None = None
    default_value: str | None = None
    is_required: bool
    is_encrypted: bool
    status: str
    version: int


# --- Form Reference (Phase 2B) ---


class FormReferenceCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    reference_code: str | None = None
    reference_name: str
    low_code_form_id: UUID
    node_id: UUID | None = None
    description: str | None = None
    status: str | None = "active"
    access_mode: str | None = "editable"
    is_required: bool | None = False
    validation_json: str | None = None


class FormReferenceUpdate(BaseModel):
    reference_name: str | None = None
    low_code_form_id: UUID | None = None
    node_id: UUID | None = None
    description: str | None = None
    status: str | None = None
    access_mode: str | None = None
    is_required: bool | None = None
    validation_json: str | None = None
    version: int | None = None


class FormReferenceResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    reference_code: str
    reference_name: str
    low_code_form_id: UUID
    node_id: UUID | None = None
    description: str | None = None
    status: str
    access_mode: str
    is_required: bool
    validation_json: str | None = None
    version: int


# --- Assignment Rule (Phase 3A) ---


class AssignmentRuleCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    assignment_code: str | None = None
    assignment_name: str
    assignment_type: str
    strategy: str | None = "static"
    description: str | None = None
    status: str | None = "active"
    priority: int | None = 0
    role_id: UUID | None = None
    user_id: UUID | None = None
    department_id: UUID | None = None
    employee_id: UUID | None = None
    fallback_assignee_id: UUID | None = None
    expression: str | None = None
    strategy_metadata_json: str | None = None
    node_id: UUID | None = None


class AssignmentRuleUpdate(BaseModel):
    assignment_name: str | None = None
    assignment_type: str | None = None
    strategy: str | None = None
    description: str | None = None
    status: str | None = None
    priority: int | None = None
    role_id: UUID | None = None
    user_id: UUID | None = None
    department_id: UUID | None = None
    employee_id: UUID | None = None
    fallback_assignee_id: UUID | None = None
    expression: str | None = None
    strategy_metadata_json: str | None = None
    node_id: UUID | None = None
    version: int | None = None


class AssignmentRuleResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    assignment_code: str
    assignment_name: str
    assignment_type: str
    strategy: str
    description: str | None = None
    status: str
    priority: int
    role_id: UUID | None = None
    user_id: UUID | None = None
    department_id: UUID | None = None
    employee_id: UUID | None = None
    fallback_assignee_id: UUID | None = None
    expression: str | None = None
    strategy_metadata_json: str | None = None
    node_id: UUID | None = None
    version: int


# --- Escalation Policy (Phase 3A) ---


class EscalationPolicyCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    policy_code: str | None = None
    policy_name: str
    escalation_target_type: str
    escalation_target_id: UUID
    description: str | None = None
    status: str | None = "active"
    escalation_level: int | None = 1
    escalation_delay_minutes: int | None = 0
    escalation_reason: str | None = None
    retry_count: int | None = 0
    levels_json: str | None = None
    node_id: UUID | None = None


class EscalationPolicyUpdate(BaseModel):
    policy_name: str | None = None
    escalation_target_type: str | None = None
    escalation_target_id: UUID | None = None
    description: str | None = None
    status: str | None = None
    escalation_level: int | None = None
    escalation_delay_minutes: int | None = None
    escalation_reason: str | None = None
    retry_count: int | None = None
    levels_json: str | None = None
    node_id: UUID | None = None
    version: int | None = None


class EscalationPolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    policy_code: str
    policy_name: str
    escalation_target_type: str
    escalation_target_id: UUID | None = None
    description: str | None = None
    status: str
    escalation_level: int
    escalation_delay_minutes: int
    escalation_reason: str | None = None
    retry_count: int
    levels_json: str | None = None
    node_id: UUID | None = None
    version: int


# --- SLA Policy (Phase 3A) ---


class SlaPolicyCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    policy_code: str | None = None
    policy_name: str
    description: str | None = None
    status: str | None = "active"
    timezone: str | None = "UTC"
    business_hours_json: str | None = None
    reminder_intervals_json: str | None = None
    warning_threshold_minutes: int | None = 60
    breach_threshold_minutes: int | None = 120
    calendar_id: UUID | None = None
    holiday_calendar_id: UUID | None = None
    node_id: UUID | None = None


class SlaPolicyUpdate(BaseModel):
    policy_name: str | None = None
    description: str | None = None
    status: str | None = None
    timezone: str | None = None
    business_hours_json: str | None = None
    reminder_intervals_json: str | None = None
    warning_threshold_minutes: int | None = None
    breach_threshold_minutes: int | None = None
    calendar_id: UUID | None = None
    holiday_calendar_id: UUID | None = None
    node_id: UUID | None = None
    version: int | None = None


class SlaPolicyResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    policy_code: str
    policy_name: str
    description: str | None = None
    status: str
    timezone: str
    business_hours_json: str | None = None
    reminder_intervals_json: str | None = None
    warning_threshold_minutes: int
    breach_threshold_minutes: int
    calendar_id: UUID | None = None
    holiday_calendar_id: UUID | None = None
    node_id: UUID | None = None
    version: int


# --- Workflow Trigger (Phase 3B) ---


class WorkflowTriggerCreate(BaseModel):
    definition_id: UUID
    version_id: UUID | None = None
    company_id: UUID | None = None
    trigger_code: str | None = None
    trigger_name: str
    trigger_type: str
    description: str | None = None
    status: str | None = "enabled"
    event_name: str | None = None
    module_code: str | None = None
    entity_type: str | None = None
    execution_mode_metadata_json: str | None = None


class WorkflowTriggerUpdate(BaseModel):
    version_id: UUID | None = None
    trigger_name: str | None = None
    trigger_type: str | None = None
    description: str | None = None
    status: str | None = None
    event_name: str | None = None
    module_code: str | None = None
    entity_type: str | None = None
    execution_mode_metadata_json: str | None = None
    version: int | None = None


class WorkflowTriggerResponse(OrmModel):
    id: UUID
    company_id: UUID
    definition_id: UUID
    version_id: UUID | None = None
    trigger_code: str
    trigger_name: str
    trigger_type: str
    description: str | None = None
    status: str
    event_name: str | None = None
    module_code: str | None = None
    entity_type: str | None = None
    execution_mode_metadata_json: str | None = None
    version: int


# --- Notification Template (Phase 3B) ---


class NotificationTemplateCreate(BaseModel):
    version_id: UUID
    company_id: UUID | None = None
    template_code: str | None = None
    template_name: str
    template_type: str
    description: str | None = None
    status: str | None = "enabled"
    subject: str | None = None
    body: str
    variables_json: str | None = None
    localization_json: str | None = None
    foundation_template_id: UUID | None = None


class NotificationTemplateUpdate(BaseModel):
    template_name: str | None = None
    template_type: str | None = None
    description: str | None = None
    status: str | None = None
    subject: str | None = None
    body: str | None = None
    variables_json: str | None = None
    localization_json: str | None = None
    foundation_template_id: UUID | None = None
    version: int | None = None


class NotificationTemplateResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    template_code: str
    template_name: str
    template_type: str
    description: str | None = None
    status: str
    subject: str | None = None
    body: str | None = None
    variables_json: str | None = None
    localization_json: str | None = None
    foundation_template_id: UUID | None = None
    version: int


# --- Workflow Instance (Phase 4) ---


class WorkflowInstanceCreate(BaseModel):
    version_id: UUID
    module_code: str
    entity_id: UUID
    company_id: UUID | None = None
    entity_type: str | None = None
    description: str | None = None
    context_json: str | None = None
    auto_start: bool = False


class WorkflowInstanceUpdate(BaseModel):
    description: str | None = None
    context_json: str | None = None
    version: int | None = None


class WorkflowInstanceResponse(OrmModel):
    id: UUID
    company_id: UUID
    definition_id: UUID
    version_id: UUID
    instance_code: str
    status: str
    module_code: str
    entity_type: str | None = None
    entity_id: UUID
    description: str | None = None
    context_json: str | None = None
    failure_reason: str | None = None
    cancel_reason: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    suspended_at: datetime | None = None
    started_by: UUID | None = None
    version: int


class WorkflowInstanceCancel(BaseModel):
    reason: str | None = None


class WorkflowInstanceFail(BaseModel):
    reason: str | None = None


# --- Workflow Task (Phase 4) ---


class WorkflowTaskCreate(BaseModel):
    instance_id: UUID
    company_id: UUID | None = None
    task_code: str | None = None
    task_name: str
    description: str | None = None
    status: str | None = "open"
    priority: int | None = 0
    execution_mode: str | None = "sequential"
    parallel_group_key: str | None = None
    sequence_order: int | None = 0
    assignee_id: UUID | None = None
    due_at: datetime | None = None
    metadata_json: str | None = None
    node_id: UUID | None = None


class WorkflowTaskUpdate(BaseModel):
    task_name: str | None = None
    description: str | None = None
    priority: int | None = None
    execution_mode: str | None = None
    parallel_group_key: str | None = None
    sequence_order: int | None = None
    due_at: datetime | None = None
    metadata_json: str | None = None
    node_id: UUID | None = None
    version: int | None = None


class WorkflowTaskResponse(OrmModel):
    id: UUID
    company_id: UUID
    instance_id: UUID
    task_code: str
    task_name: str
    description: str | None = None
    status: str
    priority: int
    execution_mode: str
    parallel_group_key: str | None = None
    sequence_order: int
    assignee_id: UUID | None = None
    claimed_by: UUID | None = None
    due_at: datetime | None = None
    completed_at: datetime | None = None
    rejection_reason: str | None = None
    metadata_json: str | None = None
    node_id: UUID | None = None
    version: int


class WorkflowTaskAssign(BaseModel):
    assignee_id: UUID


class WorkflowTaskReject(BaseModel):
    reason: str | None = None


# --- Workflow History (Phase 4) ---


class WorkflowHistoryAppend(BaseModel):
    instance_id: UUID
    event_type: str
    task_id: UUID | None = None
    delegation_id: UUID | None = None
    from_status: str | None = None
    to_status: str | None = None
    message: str | None = None
    payload_json: str | None = None


class WorkflowHistoryResponse(OrmModel):
    id: UUID
    company_id: UUID
    instance_id: UUID
    task_id: UUID | None = None
    delegation_id: UUID | None = None
    event_code: str
    event_type: str
    from_status: str | None = None
    to_status: str | None = None
    message: str | None = None
    payload_json: str | None = None
    actor_id: UUID | None = None
    occurred_at: datetime
    version: int


# --- Task Delegation (Phase 4) ---


class TaskDelegationCreate(BaseModel):
    task_id: UUID
    original_assignee_id: UUID
    delegate_assignee_id: UUID
    company_id: UUID | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    reason: str | None = None


class TaskDelegationResponse(OrmModel):
    id: UUID
    company_id: UUID
    task_id: UUID
    delegation_code: str
    status: str
    original_assignee_id: UUID
    delegate_assignee_id: UUID
    effective_from: datetime
    effective_to: datetime | None = None
    accepted_at: datetime | None = None
    rejected_at: datetime | None = None
    expired_at: datetime | None = None
    reason: str | None = None
    version: int


# --- Simulation Run (Phase 5) ---


class SimulationRunCreate(BaseModel):
    version_id: UUID
    simulation_name: str
    company_id: UUID | None = None
    simulation_code: str | None = None
    description: str | None = None
    input_context_json: str | None = None


class SimulationRunUpdate(BaseModel):
    simulation_name: str | None = None
    description: str | None = None
    input_context_json: str | None = None
    version: int | None = None


class SimulationRunResponse(OrmModel):
    id: UUID
    company_id: UUID
    version_id: UUID
    simulation_code: str
    simulation_name: str
    description: str | None = None
    status: str
    duration_ms: int
    input_context_json: str | None = None
    warnings_json: str | None = None
    errors_json: str | None = None
    execution_trace_json: str | None = None
    result_summary_json: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    started_by: UUID | None = None
    version: int


class SimulationValidateRequest(BaseModel):
    version_id: UUID


class SimulationValidateResponse(BaseModel):
    version_id: str
    valid: bool
    warnings: list[dict]
    errors: list[dict]
    decision_tables_evaluated: int = 0
    business_rules_evaluated: int = 0
    variables_resolved: int = 0
