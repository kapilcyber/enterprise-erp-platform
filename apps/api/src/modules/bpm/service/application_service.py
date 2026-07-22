"""BPM application service facade — Phase 1 through Phase 5."""

from sqlalchemy.orm import Session

from modules.bpm.service.assignment_rule_service import AssignmentRuleService
from modules.bpm.service.bpm_dashboard_service import BpmDashboardService
from modules.bpm.service.bpm_integration_service import BpmIntegrationService
from modules.bpm.service.business_rule_service import BusinessRuleService
from modules.bpm.service.decision_table_service import DecisionTableService
from modules.bpm.service.designer_graph_validation_service import DesignerGraphValidationService
from modules.bpm.service.designer_node_service import DesignerNodeService
from modules.bpm.service.designer_transition_service import DesignerTransitionService
from modules.bpm.service.escalation_policy_service import EscalationPolicyService
from modules.bpm.service.form_reference_service import FormReferenceService
from modules.bpm.service.graph_driven_task_generation_service import (
    GraphDrivenTaskGenerationService,
)
from modules.bpm.service.notification_template_service import NotificationTemplateService
from modules.bpm.service.publish_validation_service import PublishValidationService
from modules.bpm.service.simulation_run_service import SimulationRunService
from modules.bpm.service.sla_policy_service import SlaPolicyService
from modules.bpm.service.task_delegation_service import TaskDelegationService
from modules.bpm.service.template_import_export_service import TemplateImportExportService
from modules.bpm.service.version_comparison_service import VersionComparisonService
from modules.bpm.service.workflow_category_service import WorkflowCategoryService
from modules.bpm.service.workflow_definition_service import WorkflowDefinitionService
from modules.bpm.service.workflow_history_service import WorkflowHistoryService
from modules.bpm.service.workflow_instance_service import WorkflowInstanceService
from modules.bpm.service.workflow_task_service import WorkflowTaskService
from modules.bpm.service.workflow_template_service import WorkflowTemplateService
from modules.bpm.service.workflow_trigger_service import WorkflowTriggerService
from modules.bpm.service.workflow_variable_service import WorkflowVariableService
from modules.bpm.service.workflow_version_service import WorkflowVersionService


class BpmApplicationService:
    def __init__(self, db: Session) -> None:
        self.categories = WorkflowCategoryService(db)
        self.templates = WorkflowTemplateService(db)
        self.definitions = WorkflowDefinitionService(db)
        self.versions = WorkflowVersionService(db)
        self.publish_validation = PublishValidationService(db)
        self.version_comparison = VersionComparisonService(db)
        self.template_io = TemplateImportExportService(db)
        self.dashboard = BpmDashboardService(db)
        self.nodes = DesignerNodeService(db)
        self.transitions = DesignerTransitionService(db)
        self.graph_validation = DesignerGraphValidationService(db)
        self.decision_tables = DecisionTableService(db)
        self.business_rules = BusinessRuleService(db)
        self.variables = WorkflowVariableService(db)
        self.form_references = FormReferenceService(db)
        self.assignment_rules = AssignmentRuleService(db)
        self.escalation_policies = EscalationPolicyService(db)
        self.sla_policies = SlaPolicyService(db)
        self.triggers = WorkflowTriggerService(db)
        self.notification_templates = NotificationTemplateService(db)
        self.instances = WorkflowInstanceService(db)
        self.tasks = WorkflowTaskService(db)
        self.history = WorkflowHistoryService(db)
        self.delegations = TaskDelegationService(db)
        self.simulations = SimulationRunService(db)
        self.graph_task_generation = GraphDrivenTaskGenerationService(db)
        self.integration = BpmIntegrationService(db)
