# Sprint 25 Phase 4 Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.20-beta |
| **Sprint** | Sprint 25 — Workflow & BPM Designer |
| **Phase** | Phase 4 — Runtime Foundation |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-25 / ERD-25 — Preserved |
| **Prior Phases** | Phase 1 · Phase 1.5 · Phase 2A · Phase 2B · Phase 3A · Phase 3B — Complete |
| **Schema / Prefix** | `bpm` / `bpm_` |
| **New Tables** | 4 (`bpm_workflow_instance` · `bpm_workflow_task` · `bpm_workflow_history` · `bpm_task_delegation`) |
| **Total BPM Tables** | 19 of 20 |
| **Alembic Head** | `0489_seed_bpm_phase4_permissions` |
| **BPM Tests** | 116 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `bpm_workflow_instance` | CRUD · start · cancel · suspend · resume · complete · fail · Published version only · `module_code` + `entity_id` UUID |
| 2 | `bpm_workflow_task` | CRUD · assign · claim · release · complete · reject · parallel/sequential metadata · assignee · due · priority |
| 3 | `bpm_workflow_history` | Append-only · state transitions · assignments · approvals · rejects · delegations · audit metadata |
| 4 | `bpm_task_delegation` | CRUD · delegate · accept · reject · expire · original/delegate assignees · effective period · reason |

### Validation Rules Enforced

- Runtime uses **Published Version only** (`assert_executable` — no draft execution)
- History is **append-only** (update / soft-delete forbidden)
- Business entity references remain **UUID-only** (`module_code` + `entity_id`)
- No peer ORM writes · business modules remain Systems of Record
- Foundation Audit used for entity change logging
- No simulation · no trigger execution · no notification delivery

### Explicitly Not Done

- `bpm_simulation_run`
- Trigger firing / schedule / webhook / MQ execution
- Foundation Notification delivery
- Full graph-driven auto task spawning engine

---

## Files Created

### Domain / Models / Repositories

| File |
|------|
| `apps/api/src/modules/bpm/models/workflow_instance.py` |
| `apps/api/src/modules/bpm/models/workflow_task.py` |
| `apps/api/src/modules/bpm/models/workflow_history.py` |
| `apps/api/src/modules/bpm/models/task_delegation.py` |
| `apps/api/src/modules/bpm/repository/workflow_instance_repository.py` |
| `apps/api/src/modules/bpm/repository/workflow_task_repository.py` |
| `apps/api/src/modules/bpm/repository/workflow_history_repository.py` |
| `apps/api/src/modules/bpm/repository/task_delegation_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/bpm/service/workflow_instance_service.py` |
| `apps/api/src/modules/bpm/service/workflow_task_service.py` |
| `apps/api/src/modules/bpm/service/workflow_history_service.py` |
| `apps/api/src/modules/bpm/service/task_delegation_service.py` |
| `apps/api/src/modules/bpm/service/engines/runtime_engines.py` |

### Migrations

| Revision | File |
|----------|------|
| `0486_bpm_workflow_instance` | `apps/api/alembic/versions/0486_bpm_workflow_instance.py` |
| `0487_bpm_workflow_task` | `apps/api/alembic/versions/0487_bpm_workflow_task.py` |
| `0488_bpm_history_delegation` | `apps/api/alembic/versions/0488_bpm_history_delegation.py` |
| `0489_seed_bpm_phase4_permissions` | `apps/api/alembic/versions/0489_seed_bpm_phase4_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/bpm/test_bpm_phase4_runtime.py` |
| `apps/api/src/tests/security/bpm/test_bpm_phase4_permissions.py` |
| `apps/api/src/tests/integration/bpm/test_bpm_phase4_module_import.py` |

### Report

| File |
|------|
| `docs/07_RELEASES/Sprint_25_Phase4_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/bpm/domain/enums.py` | Instance / task / history / delegation enums · code prefixes |
| `apps/api/src/modules/bpm/domain/exceptions.py` | Runtime exceptions · draft-not-executable · history append-only |
| `apps/api/src/modules/bpm/domain/entities.py` | Runtime identities |
| `apps/api/src/modules/bpm/domain/value_objects.py` | Business entity ref · history / delegation VOs |
| `apps/api/src/modules/bpm/models/__init__.py` | Export Phase 4 models (19 total) |
| `apps/api/src/modules/bpm/service/engines/workflow_version_engine.py` | `assert_executable` (Published only) |
| `apps/api/src/modules/bpm/service/engines/__init__.py` | Export runtime engines |
| `apps/api/src/modules/bpm/service/application_service.py` | Wire instances · tasks · history · delegations |
| `apps/api/src/modules/bpm/service/__init__.py` | Export Phase 4 services |
| `apps/api/src/modules/bpm/schemas.py` | Runtime Create / Update / Response · action payloads |
| `apps/api/src/modules/bpm/permissions.py` | Phase 4 permissions · owner runtime actions |
| `apps/api/src/modules/bpm/routers/__init__.py` | Instances · tasks · history · delegations routes |
| `apps/api/src/modules/bpm/router.py` | Include Phase 4 routers |
| Integration import tests (hub · 1.5 · 2A · 2B · 3A · 3B) | Model count → 19 · runtime present |

---

## APIs

**Mount:** `/api/v1/bpm`

### Instances — `/instances`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` or `?module_code=&entity_id=` | `bpm.instance:read` |
| GET | `/{id}` | `bpm.instance:read` |
| POST | `` | `bpm.instance:create` |
| PATCH | `/{id}` | `bpm.instance:update` |
| DELETE | `/{id}` | `bpm.instance:delete` |
| POST | `/{id}/start` | `bpm.instance:start` |
| POST | `/{id}/cancel` | `bpm.instance:cancel` |
| POST | `/{id}/suspend` | `bpm.instance:suspend` |
| POST | `/{id}/resume` | `bpm.instance:resume` |
| POST | `/{id}/complete` | `bpm.instance:complete` |
| POST | `/{id}/fail` | `bpm.instance:fail` |

### Tasks — `/tasks`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?instance_id=` | `bpm.task:read` |
| GET | `/{id}` | `bpm.task:read` |
| POST | `` | `bpm.task:create` |
| PATCH | `/{id}` | `bpm.task:update` |
| DELETE | `/{id}` | `bpm.task:delete` |
| POST | `/{id}/assign` | `bpm.task:assign` |
| POST | `/{id}/claim` | `bpm.task:claim` |
| POST | `/{id}/release` | `bpm.task:release` |
| POST | `/{id}/complete` | `bpm.task:complete` |
| POST | `/{id}/reject` | `bpm.task:reject` |

### History — `/history`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?instance_id=` or `?task_id=` | `bpm.history:read` |
| GET | `/{id}` | `bpm.history:read` |
| POST | `` | `bpm.history:append` |

### Delegations — `/delegations`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?task_id=` | `bpm.delegation:read` |
| GET | `/{id}` | `bpm.delegation:read` |
| POST | `` | `bpm.delegation:create` |
| POST | `/{id}/accept` | `bpm.delegation:accept` |
| POST | `/{id}/reject` | `bpm.delegation:reject` |
| POST | `/{id}/expire` | `bpm.delegation:expire` |
| DELETE | `/{id}` | `bpm.delegation:delete` |

**New Phase 4 routes:** 31

---

## Repositories

| Repository | Role |
|------------|------|
| `WorkflowInstanceRepository` | CRUD · list by version · list by business entity · soft delete |
| `WorkflowTaskRepository` | CRUD · list by instance · soft delete |
| `WorkflowHistoryRepository` | Append · get · list by instance/task (no update/delete) |
| `TaskDelegationRepository` | CRUD · list by task · soft delete |

---

## Services

| Service | Role |
|---------|------|
| `WorkflowInstanceService` | Create on Published version · lifecycle transitions · history recording · UUID business ref |
| `WorkflowTaskService` | Task CRUD · assign/claim/release/complete/reject · history events |
| `WorkflowHistoryService` | Append-only events · forbids update/delete |
| `TaskDelegationService` | Delegate · accept (reassigns task) · reject · expire · history |
| `WorkflowInstanceEngine` | Start/cancel/suspend/resume/complete/fail transitions |
| `WorkflowTaskEngine` | Assign/claim/release/complete/reject |
| `WorkflowHistoryEngine` | Event type validation · append-only guard |
| `TaskDelegationEngine` | Period validation · accept/reject/expire |
| `WorkflowVersionEngine` | `assert_executable` (Published only) |
| `BpmApplicationService` | Facade wiring for Phase 4 |

**Tasks:** None required for Phase 4 foundation (no Celery trigger/delivery workers).

---

## Permissions

| Permission |
|------------|
| `bpm.instance:read` · `create` · `update` · `delete` · `start` · `cancel` · `suspend` · `resume` · `complete` · `fail` |
| `bpm.task:read` · `create` · `update` · `delete` · `assign` · `claim` · `release` · `complete` · `reject` |
| `bpm.history:read` · `append` |
| `bpm.delegation:read` · `create` · `accept` · `reject` · `expire` · `delete` |

Roles re-synced: `BPM_ADMIN` · `PROCESS_DESIGNER` · `PROCESS_OWNER` · `WORKFLOW_OPERATOR` · `WORKFLOW_AUDITOR`

---

## Tests

| Suite | Coverage | Result |
|-------|----------|--------|
| Unit | Instance lifecycle · Published-only · task actions · history append-only · delegation | PASS |
| Security | Phase 4 permission presence · owner runtime · auditor read | PASS |
| Integration | Models (19) · services · routes · no simulation | PASS |
| Prior phases | Engines · polish · designer · intelligence · governance · comms · imports | PASS |
| **Total BPM** | | **116 passed** |

---

## Remaining Work for Phase 5

| Area | Remaining |
|------|-----------|
| Simulation | `bpm_simulation_run` (status · duration · warnings · errors · no business mutation) |
| Engine polish | Graph-driven auto task creation from Published designer nodes |
| Execution | Trigger firing · schedule/webhook/MQ consumers |
| Delivery | Foundation Notification handoff from templates |
| UI | Runtime inbox · instance monitor · delegation UX |

**Tables remaining after Phase 4:** 1 of 20 ERD-25 business tables (`bpm_simulation_run`).

---

**Sprint 25 Phase 4 — Complete.**
