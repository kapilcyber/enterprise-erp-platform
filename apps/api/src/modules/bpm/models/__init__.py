"""BPM ORM models — Phase 1 through Phase 5 (20/20 ERD tables)."""

from modules.bpm.models.assignment_rule import BpmAssignmentRule
from modules.bpm.models.business_rule import BpmBusinessRule
from modules.bpm.models.decision_table import BpmDecisionTable
from modules.bpm.models.designer_node import BpmDesignerNode
from modules.bpm.models.designer_transition import BpmDesignerTransition
from modules.bpm.models.escalation_policy import BpmEscalationPolicy
from modules.bpm.models.form_reference import BpmFormReference
from modules.bpm.models.notification_template import BpmNotificationTemplate
from modules.bpm.models.simulation_run import BpmSimulationRun
from modules.bpm.models.sla_policy import BpmSlaPolicy
from modules.bpm.models.task_delegation import BpmTaskDelegation
from modules.bpm.models.workflow_category import BpmWorkflowCategory
from modules.bpm.models.workflow_definition import BpmWorkflowDefinition
from modules.bpm.models.workflow_history import BpmWorkflowHistory
from modules.bpm.models.workflow_instance import BpmWorkflowInstance
from modules.bpm.models.workflow_task import BpmWorkflowTask
from modules.bpm.models.workflow_template import BpmWorkflowTemplate
from modules.bpm.models.workflow_trigger import BpmWorkflowTrigger
from modules.bpm.models.workflow_variable import BpmWorkflowVariable
from modules.bpm.models.workflow_version import BpmWorkflowVersion

__all__ = [
    "BpmWorkflowCategory",
    "BpmWorkflowTemplate",
    "BpmWorkflowDefinition",
    "BpmWorkflowVersion",
    "BpmDesignerNode",
    "BpmDesignerTransition",
    "BpmDecisionTable",
    "BpmBusinessRule",
    "BpmWorkflowVariable",
    "BpmFormReference",
    "BpmAssignmentRule",
    "BpmEscalationPolicy",
    "BpmSlaPolicy",
    "BpmWorkflowTrigger",
    "BpmNotificationTemplate",
    "BpmWorkflowInstance",
    "BpmWorkflowTask",
    "BpmWorkflowHistory",
    "BpmTaskDelegation",
    "BpmSimulationRun",
]
