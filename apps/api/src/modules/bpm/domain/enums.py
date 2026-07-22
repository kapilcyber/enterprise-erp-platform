"""BPM domain enums per FRD-25 / ERD-25 Phase 1."""

from enum import Enum


class CategoryStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class TemplateStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


class DefinitionStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


class VersionStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"


class DesignerNodeType(str, Enum):
    START = "start"
    END = "end"
    USER_TASK = "user_task"
    APPROVAL_TASK = "approval_task"
    GATEWAY = "gateway"
    PARALLEL_GATEWAY = "parallel_gateway"
    EXCLUSIVE_GATEWAY = "exclusive_gateway"
    INCLUSIVE_GATEWAY = "inclusive_gateway"
    TIMER = "timer"
    API = "api"
    SUB_WORKFLOW = "sub_workflow"
    VALIDATION = "validation"


class DesignerNodeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class TransitionType(str, Enum):
    SEQUENTIAL = "sequential"
    CONDITIONAL = "conditional"
    PARALLEL = "parallel"
    MERGE = "merge"
    SPLIT = "split"


class TransitionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class DecisionTableStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class BusinessRuleType(str, Enum):
    EXPRESSION = "expression"
    DECISION = "decision"
    VALIDATION = "validation"
    ROUTING = "routing"


class BusinessRuleStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"


class VariableType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"
    JSON = "json"


class VariableStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class FormReferenceMode(str, Enum):
    READ_ONLY = "read_only"
    EDITABLE = "editable"


class FormReferenceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class AssignmentType(str, Enum):
    ROLE = "role"
    USER = "user"
    DEPARTMENT = "department"
    DYNAMIC = "dynamic"


class AssignmentStrategy(str, Enum):
    STATIC = "static"
    ROUND_ROBIN = "round_robin"
    LOAD_BALANCE = "load_balance"


class AssignmentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class EscalationTargetType(str, Enum):
    ROLE = "role"
    USER = "user"
    DEPARTMENT = "department"


class EscalationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class SlaStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class GovernanceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class TriggerType(str, Enum):
    MANUAL = "manual"
    EVENT = "event"
    API = "api"
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"
    MESSAGE_QUEUE = "message_queue"


class TriggerStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class NotificationTemplateType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class NotificationTemplateStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class InstanceStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class TaskStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    CLAIMED = "claimed"
    COMPLETED = "completed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class TaskExecutionMode(str, Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class HistoryEventType(str, Enum):
    STATE_TRANSITION = "state_transition"
    ASSIGNMENT = "assignment"
    APPROVAL = "approval"
    REJECTION = "rejection"
    DELEGATION = "delegation"
    ESCALATION = "escalation"
    COMMENT = "comment"


class DelegationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class SimulationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BpmEntityType(str, Enum):
    WORKFLOW_CATEGORY = "workflow_category"
    WORKFLOW_TEMPLATE = "workflow_template"
    WORKFLOW_DEFINITION = "workflow_definition"
    WORKFLOW_VERSION = "workflow_version"
    DESIGNER_NODE = "designer_node"
    DESIGNER_TRANSITION = "designer_transition"
    DECISION_TABLE = "decision_table"
    BUSINESS_RULE = "business_rule"
    WORKFLOW_VARIABLE = "workflow_variable"
    FORM_REFERENCE = "form_reference"
    ASSIGNMENT_RULE = "assignment_rule"
    ESCALATION_POLICY = "escalation_policy"
    SLA_POLICY = "sla_policy"
    WORKFLOW_TRIGGER = "workflow_trigger"
    NOTIFICATION_TEMPLATE = "notification_template"
    WORKFLOW_INSTANCE = "workflow_instance"
    WORKFLOW_TASK = "workflow_task"
    WORKFLOW_HISTORY = "workflow_history"
    TASK_DELEGATION = "task_delegation"
    SIMULATION_RUN = "simulation_run"


CODE_PREFIXES: dict[BpmEntityType, tuple[str, int, bool]] = {
    BpmEntityType.WORKFLOW_CATEGORY: ("CAT-", 6, True),
    BpmEntityType.WORKFLOW_TEMPLATE: ("TPL-", 6, True),
    BpmEntityType.WORKFLOW_DEFINITION: ("DEF-", 6, True),
    BpmEntityType.WORKFLOW_VERSION: ("VER-", 6, True),
    BpmEntityType.DESIGNER_NODE: ("NOD-", 6, True),
    BpmEntityType.DESIGNER_TRANSITION: ("TRN-", 6, True),
    BpmEntityType.DECISION_TABLE: ("DTB-", 6, True),
    BpmEntityType.BUSINESS_RULE: ("RUL-", 6, True),
    BpmEntityType.WORKFLOW_VARIABLE: ("VAR-", 6, True),
    BpmEntityType.FORM_REFERENCE: ("FRM-", 6, True),
    BpmEntityType.ASSIGNMENT_RULE: ("ASN-", 6, True),
    BpmEntityType.ESCALATION_POLICY: ("ESC-", 6, True),
    BpmEntityType.SLA_POLICY: ("SLA-", 6, True),
    BpmEntityType.WORKFLOW_TRIGGER: ("TRG-", 6, True),
    BpmEntityType.NOTIFICATION_TEMPLATE: ("NTF-", 6, True),
    BpmEntityType.WORKFLOW_INSTANCE: ("INS-", 6, True),
    BpmEntityType.WORKFLOW_TASK: ("TSK-", 6, True),
    BpmEntityType.WORKFLOW_HISTORY: ("HST-", 6, True),
    BpmEntityType.TASK_DELEGATION: ("DLG-", 6, True),
    BpmEntityType.SIMULATION_RUN: ("SIM-", 6, True),
}

NODE_TYPE_VALUES = tuple(t.value for t in DesignerNodeType)
TRANSITION_TYPE_VALUES = tuple(t.value for t in TransitionType)
BUSINESS_RULE_TYPE_VALUES = tuple(t.value for t in BusinessRuleType)
VARIABLE_TYPE_VALUES = tuple(t.value for t in VariableType)
FORM_MODE_VALUES = tuple(t.value for t in FormReferenceMode)
ASSIGNMENT_TYPE_VALUES = tuple(t.value for t in AssignmentType)
ASSIGNMENT_STRATEGY_VALUES = tuple(t.value for t in AssignmentStrategy)
ESCALATION_TARGET_TYPE_VALUES = tuple(t.value for t in EscalationTargetType)
TRIGGER_TYPE_VALUES = tuple(t.value for t in TriggerType)
NOTIFICATION_TEMPLATE_TYPE_VALUES = tuple(t.value for t in NotificationTemplateType)
INSTANCE_STATUS_VALUES = tuple(t.value for t in InstanceStatus)
TASK_STATUS_VALUES = tuple(t.value for t in TaskStatus)
TASK_EXECUTION_MODE_VALUES = tuple(t.value for t in TaskExecutionMode)
HISTORY_EVENT_TYPE_VALUES = tuple(t.value for t in HistoryEventType)
DELEGATION_STATUS_VALUES = tuple(t.value for t in DelegationStatus)
SIMULATION_STATUS_VALUES = tuple(t.value for t in SimulationStatus)
