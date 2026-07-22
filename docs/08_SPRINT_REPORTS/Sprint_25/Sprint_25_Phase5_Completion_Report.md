# Sprint 25 Phase 5 Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.20-beta |
| **Sprint** | Sprint 25 — Workflow & BPM Designer |
| **Phase** | Phase 5 — Simulation & Enterprise Completion |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-25 / ERD-25 — Preserved |
| **Prior Phases** | Phase 1 · Phase 1.5 · Phase 2A · Phase 2B · Phase 3A · Phase 3B · Phase 4 — Complete |
| **Schema / Prefix** | `bpm` / `bpm_` |
| **New Tables** | 1 (`bpm_simulation_run`) |
| **Total BPM Tables** | **20 of 20** |
| **Alembic Head** | `0491_seed_bpm_phase5_permissions` |
| **BPM Tests** | **136 passed** |
| **Sprint Completion** | **100%** (ERD-25 backend table scope) |

---

## Scope Delivered

| # | Item | Capability |
|---|------|------------|
| 1 | `bpm_simulation_run` | CRUD · Run Simulation · Validate Workflow · duration · warnings · errors · execution trace · result summary |
| 2 | Runtime polish | Graph-driven initial task generation from published designer graph on instance `start()` |

### Simulation Capabilities

- Node traversal (BFS from Start)
- Transition validation (including conditional simulation)
- Decision table evaluation (**simulation only**)
- Business rule evaluation (**simulation only**)
- Variable resolution (**simulation only**)
- Stores warnings / errors / execution_trace / result_summary on the simulation row

### Validation Rules Enforced

- Simulation allowed only on **Draft or Published** versions
- Simulation **never** mutates business entities
- Simulation **never** creates runtime workflow instances
- Simulation **never** sends notifications
- Simulation **never** executes triggers
- No runtime persistence outside simulation records
- No peer ORM writes · business modules remain Systems of Record
- Foundation Notification / Integration Hub / Foundation Audit ownership unchanged

### Runtime Polish

- On instance `start()`, `GraphDrivenTaskGenerationService` walks the published designer graph
- Seeds `user_task` / `approval_task` / `validation` nodes via existing `WorkflowTaskService`
- Reuses existing runtime services — **no duplicate execution engine**

### Explicitly Out of Scope (post–Sprint 25 backend ERD)

- Trigger firing / schedule / webhook / MQ consumers
- Foundation Notification delivery handoff
- Continuous graph auto-routing after each task completion
- BPM Designer UI / runtime inbox UX

---

## Files Created

### Domain / Models / Repositories

| File |
|------|
| `apps/api/src/modules/bpm/models/simulation_run.py` |
| `apps/api/src/modules/bpm/repository/simulation_run_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/bpm/service/simulation_run_service.py` |
| `apps/api/src/modules/bpm/service/graph_driven_task_generation_service.py` |
| `apps/api/src/modules/bpm/service/engines/simulation_engines.py` |

### Migrations

| Revision | File |
|----------|------|
| `0490_bpm_simulation_run` | `apps/api/alembic/versions/0490_bpm_simulation_run.py` |
| `0491_seed_bpm_phase5_permissions` | `apps/api/alembic/versions/0491_seed_bpm_phase5_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/bpm/test_bpm_phase5_simulation.py` |
| `apps/api/src/tests/security/bpm/test_bpm_phase5_permissions.py` |
| `apps/api/src/tests/integration/bpm/test_bpm_phase5_module_import.py` |

### Report

| File |
|------|
| `docs/07_RELEASES/Sprint_25_Phase5_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/bpm/domain/enums.py` | `SimulationStatus` · `SIMULATION_RUN` entity · code prefix `SIM-` |
| `apps/api/src/modules/bpm/domain/exceptions.py` | `InvalidSimulationRunState` · `SimulationNotAllowed` |
| `apps/api/src/modules/bpm/domain/entities.py` | `SimulationRunIdentity` |
| `apps/api/src/modules/bpm/domain/value_objects.py` | `SimulationResultSummary` |
| `apps/api/src/modules/bpm/models/__init__.py` | Export `BpmSimulationRun` (20/20) |
| `apps/api/src/modules/bpm/service/engines/__init__.py` | Export `SimulationRunEngine` |
| `apps/api/src/modules/bpm/service/workflow_instance_service.py` | Wire graph-driven task generation on `start()` |
| `apps/api/src/modules/bpm/service/application_service.py` | Wire simulations · graph task generation |
| `apps/api/src/modules/bpm/service/__init__.py` | Export Phase 5 services |
| `apps/api/src/modules/bpm/schemas.py` | Simulation Create / Update / Response · Validate payloads |
| `apps/api/src/modules/bpm/permissions.py` | Phase 5 simulation permissions · owner run/validate |
| `apps/api/src/modules/bpm/routers/__init__.py` | Simulations routes |
| `apps/api/src/modules/bpm/router.py` | Include `simulations_router` |
| Integration import tests (hub · 1.5 · 2A · 2B · 3A · 3B · 4) | Model count → 20 · simulation present |

---

## APIs

**Mount:** `/api/v1/bpm`

### Simulations — `/simulations`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.simulation:read` |
| GET | `/{id}` | `bpm.simulation:read` |
| POST | `` | `bpm.simulation:create` |
| PATCH | `/{id}` | `bpm.simulation:update` |
| DELETE | `/{id}` | `bpm.simulation:delete` |
| POST | `/validate` | `bpm.simulation:validate` |
| POST | `/{id}/run` | `bpm.simulation:run` |
| POST | `/{id}/cancel` | `bpm.simulation:cancel` |

**New Phase 5 routes:** 8

**Runtime polish (existing API):** `POST /instances/{id}/start` now seeds graph-driven tasks.

---

## Repositories

| Repository | Role |
|------------|------|
| `SimulationRunRepository` | CRUD · list by version · soft delete · persist warnings/errors/trace/summary |

---

## Services

| Service | Role |
|---------|------|
| `SimulationRunService` | CRUD · validate workflow · run simulation (graph + intelligence dry-eval) · cancel |
| `SimulationRunEngine` | Draft/Published gate · begin/complete/fail/cancel lifecycle |
| `GraphDrivenTaskGenerationService` | Initial task seed from designer graph via `WorkflowTaskService` |
| `WorkflowInstanceService` | `start()` invokes graph task generation (Phase 5 polish) |
| `BpmApplicationService` | Facade wiring for Phase 5 |

**Tasks:** None required for Phase 5 (simulation is synchronous; no Celery workers).

---

## Permissions

| Permission |
|------------|
| `bpm.simulation:read` · `create` · `update` · `delete` · `run` · `validate` · `cancel` |

Roles re-synced: `BPM_ADMIN` · `PROCESS_DESIGNER` · `PROCESS_OWNER` · `WORKFLOW_OPERATOR` · `WORKFLOW_AUDITOR`

- Owner: read · run · validate
- Auditor / Operator: read only
- Admin / Designer: full set per role matrix

---

## Tests

| Suite | Coverage | Result |
|-------|----------|--------|
| Unit | Simulation lifecycle · Draft/Published gate · result summary · transition condition · graph node sets | PASS |
| Security | Phase 5 permission presence · owner run/validate · auditor read-only | PASS |
| Integration | Models (20/20) · services · routes · instance start wiring · e2e simulation contract (no instance/task/notification/trigger calls) | PASS |
| Prior phases | Engines · polish · designer · intelligence · governance · comms · runtime · imports | PASS |
| **Total BPM** | | **136 passed** |

---

## Sprint Completion %

| Scope | Completion |
|-------|------------|
| ERD-25 business tables (20) | **100%** |
| Sprint 25 Phase 1–5 backend design + runtime foundation + simulation | **100%** |
| Optional post-ERD enterprise extensions (trigger execution, notification delivery, continuous routing, UI) | Deferred (not ERD table scope) |

**Sprint 25 ERD backend table delivery: 100%**

---

## Remaining Work (if any)

| Area | Remaining |
|------|-----------|
| Execution | Trigger firing · schedule / webhook / MQ consumers |
| Delivery | Foundation Notification handoff from `bpm_notification_template` |
| Runtime depth | Continuous graph auto-routing after each task complete (beyond initial seed) |
| UI | Designer canvas · simulation console · runtime inbox · instance monitor |

**Tables remaining after Phase 5:** **0 of 20** ERD-25 business tables.

---

**Sprint 25 Phase 5 — Complete.**
**Sprint 25 Workflow & BPM Designer (ERD-25 backend) — Complete.**
