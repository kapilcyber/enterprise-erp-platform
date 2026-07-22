"""BPM module router aggregation — Phase 1 through Phase 5."""

from fastapi import APIRouter

from modules.bpm.routers import (
    assignment_rules_router,
    business_rules_router,
    categories_router,
    dashboard_router,
    decision_tables_router,
    definitions_router,
    delegations_router,
    escalation_policies_router,
    form_references_router,
    graph_router,
    history_router,
    instances_router,
    nodes_router,
    notification_templates_router,
    simulations_router,
    sla_policies_router,
    tasks_router,
    templates_router,
    transitions_router,
    triggers_router,
    variables_router,
    versions_router,
)

bpm_router = APIRouter(prefix="/bpm")
bpm_router.include_router(dashboard_router)
bpm_router.include_router(categories_router)
bpm_router.include_router(templates_router)
bpm_router.include_router(definitions_router)
bpm_router.include_router(versions_router)
bpm_router.include_router(nodes_router)
bpm_router.include_router(transitions_router)
bpm_router.include_router(graph_router)
bpm_router.include_router(decision_tables_router)
bpm_router.include_router(business_rules_router)
bpm_router.include_router(variables_router)
bpm_router.include_router(form_references_router)
bpm_router.include_router(assignment_rules_router)
bpm_router.include_router(escalation_policies_router)
bpm_router.include_router(sla_policies_router)
bpm_router.include_router(triggers_router)
bpm_router.include_router(notification_templates_router)
bpm_router.include_router(instances_router)
bpm_router.include_router(tasks_router)
bpm_router.include_router(history_router)
bpm_router.include_router(delegations_router)
bpm_router.include_router(simulations_router)
