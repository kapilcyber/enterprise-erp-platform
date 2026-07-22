"""BPM domain entity markers."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class WorkflowCategoryIdentity:
    category_id: UUID
    category_code: str


@dataclass
class WorkflowTemplateIdentity:
    template_id: UUID
    template_code: str


@dataclass
class WorkflowDefinitionIdentity:
    definition_id: UUID
    definition_code: str
    module_code: str
    entity_type: str


@dataclass
class WorkflowVersionIdentity:
    version_id: UUID
    definition_id: UUID
    version_number: int
    status: str


@dataclass
class DesignerNodeIdentity:
    node_id: UUID
    version_id: UUID
    node_code: str
    node_type: str


@dataclass
class DesignerTransitionIdentity:
    transition_id: UUID
    version_id: UUID
    from_node_id: UUID
    to_node_id: UUID
    transition_type: str


@dataclass
class DecisionTableIdentity:
    decision_table_id: UUID
    version_id: UUID
    table_code: str


@dataclass
class BusinessRuleIdentity:
    business_rule_id: UUID
    version_id: UUID
    rule_code: str
    rule_type: str


@dataclass
class WorkflowVariableIdentity:
    variable_id: UUID
    version_id: UUID
    variable_key: str
    variable_type: str


@dataclass
class FormReferenceIdentity:
    form_reference_id: UUID
    version_id: UUID
    low_code_form_id: UUID


@dataclass
class AssignmentRuleIdentity:
    assignment_rule_id: UUID
    version_id: UUID
    assignment_code: str
    assignment_type: str


@dataclass
class EscalationPolicyIdentity:
    escalation_policy_id: UUID
    version_id: UUID
    policy_code: str
    escalation_level: int


@dataclass
class SlaPolicyIdentity:
    sla_policy_id: UUID
    version_id: UUID
    policy_code: str
    timezone: str


@dataclass
class WorkflowTriggerIdentity:
    trigger_id: UUID
    definition_id: UUID
    version_id: UUID | None
    trigger_code: str
    trigger_type: str


@dataclass
class NotificationTemplateIdentity:
    notification_template_id: UUID
    version_id: UUID
    template_code: str
    template_type: str


@dataclass
class WorkflowInstanceIdentity:
    instance_id: UUID
    version_id: UUID
    module_code: str
    entity_id: UUID
    status: str


@dataclass
class WorkflowTaskIdentity:
    task_id: UUID
    instance_id: UUID
    task_code: str
    status: str
    assignee_id: UUID | None = None


@dataclass
class WorkflowHistoryIdentity:
    history_id: UUID
    instance_id: UUID
    event_type: str
    task_id: UUID | None = None


@dataclass
class TaskDelegationIdentity:
    delegation_id: UUID
    task_id: UUID
    original_assignee_id: UUID
    delegate_assignee_id: UUID
    status: str


@dataclass
class SimulationRunIdentity:
    simulation_run_id: UUID
    version_id: UUID
    simulation_code: str
    status: str

