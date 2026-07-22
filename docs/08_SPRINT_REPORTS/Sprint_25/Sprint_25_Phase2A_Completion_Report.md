# Sprint 25 Phase 2A Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.20-beta (planned) |
| **Sprint** | Sprint 25 — Workflow & BPM Designer |
| **Phase** | Phase 2A — Visual Designer Foundation |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-25 / ERD-25 — Preserved |
| **Prior Phases** | Phase 1 · Phase 1.5 — Complete |
| **Schema / Prefix** | `bpm` / `bpm_` |
| **New Tables** | 2 (`bpm_designer_node` · `bpm_designer_transition`) |
| **Total BPM Tables** | 6 of 20 |
| **Alembic Head** | `0474_seed_bpm_phase2a_permissions` |
| **BPM Tests** | 51 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `bpm_designer_node` | Node CRUD · all designer node types |
| 2 | `bpm_designer_transition` | Transition CRUD · routing types · condition · decision-table UUID ref · priority |

### Designer Node Types

start · end · user_task · approval_task · gateway · parallel_gateway · exclusive_gateway · inclusive_gateway · timer · api · sub_workflow · validation

### Transition Types

sequential · conditional · parallel · merge · split

### Validation Rules Enforced

- Exactly one Start Node
- At least one End Node
- No orphan / disconnected nodes
- No circular transitions unless `allow_cycles=true`
- No duplicate transition (UK + service check)
- Transition must reference existing nodes in the same version
- Draft versions only editable (published immutable)

### Explicitly Not Done

- Runtime · instances · tasks · history
- Decision tables · business rules · variables
- Form references · assignment · SLA · escalation · triggers
- Execution engine · peer ORM writes · business data ownership

---

## Files Created

### Domain / Models / Repositories

| File |
|------|
| `apps/api/src/modules/bpm/models/designer_node.py` |
| `apps/api/src/modules/bpm/models/designer_transition.py` |
| `apps/api/src/modules/bpm/repository/designer_node_repository.py` |
| `apps/api/src/modules/bpm/repository/designer_transition_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/bpm/service/designer_node_service.py` |
| `apps/api/src/modules/bpm/service/designer_transition_service.py` |
| `apps/api/src/modules/bpm/service/designer_graph_validation_service.py` |
| `apps/api/src/modules/bpm/service/engines/designer_node_engine.py` |
| `apps/api/src/modules/bpm/service/engines/designer_transition_engine.py` |

### Migrations

| Revision | File |
|----------|------|
| `0472_bpm_designer_node` | `apps/api/alembic/versions/0472_bpm_designer_node.py` |
| `0473_bpm_designer_transition` | `apps/api/alembic/versions/0473_bpm_designer_transition.py` |
| `0474_seed_bpm_phase2a_permissions` | `apps/api/alembic/versions/0474_seed_bpm_phase2a_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/bpm/test_bpm_phase2a_designer.py` |
| `apps/api/src/tests/security/bpm/test_bpm_phase2a_permissions.py` |
| `apps/api/src/tests/integration/bpm/test_bpm_phase2a_module_import.py` |

### Report

| File |
|------|
| `docs/07_RELEASES/Sprint_25_Phase2A_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/bpm/domain/enums.py` | Node / transition enums · code prefixes |
| `apps/api/src/modules/bpm/domain/exceptions.py` | Designer / graph exceptions |
| `apps/api/src/modules/bpm/domain/entities.py` | Node / transition identities |
| `apps/api/src/modules/bpm/domain/value_objects.py` | `GraphValidationResult` |
| `apps/api/src/modules/bpm/models/__init__.py` | Export Phase 2A models (6 total) |
| `apps/api/src/modules/bpm/service/engines/__init__.py` | Export designer engines |
| `apps/api/src/modules/bpm/service/application_service.py` | Wire nodes · transitions · graph validation |
| `apps/api/src/modules/bpm/service/__init__.py` | Export Phase 2A services |
| `apps/api/src/modules/bpm/schemas.py` | Node / transition / graph schemas |
| `apps/api/src/modules/bpm/permissions.py` | Designer permissions |
| `apps/api/src/modules/bpm/routers/__init__.py` | Nodes · transitions · graph routes |
| `apps/api/src/modules/bpm/router.py` | Include Phase 2A routers |
| `apps/api/src/tests/integration/bpm/test_bpm_hub_module_import.py` | Model count → 6 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase15_module_import.py` | Model count → 6 |

---

## APIs

**Mount:** `/api/v1/bpm`

### Nodes — `/nodes`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.node:read` |
| GET | `/{id}` | `bpm.node:read` |
| POST | `` | `bpm.node:create` |
| PATCH | `/{id}` | `bpm.node:update` |
| DELETE | `/{id}` | `bpm.node:delete` |

### Transitions — `/transitions`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.transition:read` |
| GET | `/{id}` | `bpm.transition:read` |
| POST | `` | `bpm.transition:create` |
| PATCH | `/{id}` | `bpm.transition:update` |
| DELETE | `/{id}` | `bpm.transition:delete` |

### Graph — `/graph`

| Method | Path | Permission |
|--------|------|------------|
| POST | `/versions/{version_id}/validate` | `bpm.graph:validate` |

Body: `{ "allow_cycles": false }` — returns structured validation result.

**New Phase 2A routes:** 11

---

## Repositories

| Repository | Role |
|------------|------|
| `DesignerNodeRepository` | CRUD · list by version · list by type · soft delete |
| `DesignerTransitionRepository` | CRUD · list by version · find edge · list involving node · soft delete |

---

## Services

| Service | Role |
|---------|------|
| `DesignerNodeService` | Node CRUD · single-start enforcement · draft-only edits · cascade soft-delete transitions |
| `DesignerTransitionService` | Transition CRUD · node existence · duplicate edge · conditional payload |
| `DesignerGraphValidationService` | Start/end · orphans · reachability · cycles · structured result |
| `DesignerNodeEngine` | Type validation · activate / deactivate |
| `DesignerTransitionEngine` | Type validation · conditional rules |
| `BpmApplicationService` | Facade wiring for Phase 2A |

**Tasks:** None required for Phase 2A (designer-only).

---

## Permissions

| Permission |
|------------|
| `bpm.node:read` · `create` · `update` · `delete` |
| `bpm.transition:read` · `create` · `update` · `delete` |
| `bpm.graph:validate` |

Roles re-synced: `BPM_ADMIN` · `PROCESS_DESIGNER` · `PROCESS_OWNER` · `WORKFLOW_OPERATOR` · `WORKFLOW_AUDITOR`

---

## Tests

| Suite | Coverage | Result |
|-------|----------|--------|
| Unit | Node/transition types · conditional rules · cycle helper · graph VO | PASS |
| Security | Phase 2A permission presence · role slices | PASS |
| Integration | Models · services · routes · no runtime models | PASS |
| Prior Phase 1 / 1.5 | Engines · polish · imports | PASS |
| **Total BPM** | | **51 passed** |

---

## Remaining Work for Phase 2B

| Area | Remaining |
|------|-----------|
| Intelligence | `bpm_decision_table` · `bpm_business_rule` · `bpm_workflow_variable` · `bpm_form_reference` |
| Governance | `bpm_assignment_rule` · `bpm_escalation_policy` · `bpm_sla_policy` |
| Triggers / Comms | `bpm_workflow_trigger` · `bpm_notification_template` |
| Simulation | `bpm_simulation_run` |
| Runtime (later) | `bpm_workflow_instance` · `bpm_workflow_task` · `bpm_workflow_history` · `bpm_task_delegation` |
| UI | Visual designer canvas · decision table editor |
| Engine | Runtime execution on Published version only |

**Tables remaining after Phase 2A:** 14 of 20 ERD-25 business tables.

---

**Sprint 25 Phase 2A — Complete.**
