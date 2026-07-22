# Sprint 25 Phase 3B Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.20-beta |
| **Sprint** | Sprint 25 — Workflow & BPM Designer |
| **Phase** | Phase 3B — Triggers & Communication Layer |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-25 / ERD-25 — Preserved |
| **Prior Phases** | Phase 1 · Phase 1.5 · Phase 2A · Phase 2B · Phase 3A — Complete |
| **Schema / Prefix** | `bpm` / `bpm_` |
| **New Tables** | 2 (`bpm_workflow_trigger` · `bpm_notification_template`) |
| **Total BPM Tables** | 15 of 20 |
| **Alembic Head** | `0485_seed_bpm_phase3b_permissions` |
| **BPM Tests** | 99 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `bpm_workflow_trigger` | CRUD · types (manual/event/api/schedule/webhook/message_queue) · enable/disable · definition binding · optional version binding · event/module/entity · execution metadata |
| 2 | `bpm_notification_template` | CRUD · types (email/sms/push/in_app) · subject/body · variables · localization · enable/disable · version binding |

### Validation Rules Enforced

- Triggers belong to **one** Workflow Definition
- Optional Version binding must belong to the **same** definition
- Mutations blocked when trigger is bound to a non-draft (published) version
- Notification templates belong to **one** Workflow Version
- **Draft** editable; **Published** immutable
- Notification templates define **WHAT** only — Foundation Notification owns delivery
- No delivery engine · no peer ORM writes · no runtime · no simulation · no instances / tasks / history / delegation

### Explicitly Not Done

- Runtime · instances · tasks · history · task delegation
- Simulation runs
- Workflow execution · trigger firing · notification delivery
- Integration Hub transport implementation (consume-only boundary preserved)

---

## Files Created

### Domain / Models / Repositories

| File |
|------|
| `apps/api/src/modules/bpm/models/workflow_trigger.py` |
| `apps/api/src/modules/bpm/models/notification_template.py` |
| `apps/api/src/modules/bpm/repository/workflow_trigger_repository.py` |
| `apps/api/src/modules/bpm/repository/notification_template_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/bpm/service/workflow_trigger_service.py` |
| `apps/api/src/modules/bpm/service/notification_template_service.py` |
| `apps/api/src/modules/bpm/service/engines/comms_engines.py` |

### Migrations

| Revision | File |
|----------|------|
| `0483_bpm_workflow_trigger` | `apps/api/alembic/versions/0483_bpm_workflow_trigger.py` |
| `0484_bpm_notification_template` | `apps/api/alembic/versions/0484_bpm_notification_template.py` |
| `0485_seed_bpm_phase3b_permissions` | `apps/api/alembic/versions/0485_seed_bpm_phase3b_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/bpm/test_bpm_phase3b_comms.py` |
| `apps/api/src/tests/security/bpm/test_bpm_phase3b_permissions.py` |
| `apps/api/src/tests/integration/bpm/test_bpm_phase3b_module_import.py` |

### Report

| File |
|------|
| `docs/07_RELEASES/Sprint_25_Phase3B_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/bpm/domain/enums.py` | Trigger / notification enums · code prefixes |
| `apps/api/src/modules/bpm/domain/exceptions.py` | Trigger / notification exceptions |
| `apps/api/src/modules/bpm/domain/entities.py` | Trigger / notification identities |
| `apps/api/src/modules/bpm/domain/value_objects.py` | Trigger binding · notification content VOs |
| `apps/api/src/modules/bpm/models/__init__.py` | Export Phase 3B models (15 total) |
| `apps/api/src/modules/bpm/service/engines/__init__.py` | Export comms engines |
| `apps/api/src/modules/bpm/service/application_service.py` | Wire triggers · notification templates |
| `apps/api/src/modules/bpm/service/__init__.py` | Export Phase 3B services |
| `apps/api/src/modules/bpm/schemas.py` | Trigger / notification Create · Update · Response |
| `apps/api/src/modules/bpm/permissions.py` | Phase 3B permissions · role slices |
| `apps/api/src/modules/bpm/routers/__init__.py` | Triggers · notification template routes |
| `apps/api/src/modules/bpm/router.py` | Include Phase 3B routers |
| `apps/api/src/tests/integration/bpm/test_bpm_hub_module_import.py` | Model count → 15 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase15_module_import.py` | Model count → 15 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase2a_module_import.py` | Model count → 15 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase2b_module_import.py` | Model count → 15 · comms present |
| `apps/api/src/tests/integration/bpm/test_bpm_phase3a_module_import.py` | Model count → 15 · comms present |

---

## APIs

**Mount:** `/api/v1/bpm`

### Triggers — `/triggers`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?definition_id=` or `?version_id=` | `bpm.trigger:read` |
| GET | `/{id}` | `bpm.trigger:read` |
| POST | `` | `bpm.trigger:create` |
| PATCH | `/{id}` | `bpm.trigger:update` |
| DELETE | `/{id}` | `bpm.trigger:delete` |
| POST | `/{id}/enable` | `bpm.trigger:enable` |
| POST | `/{id}/disable` | `bpm.trigger:disable` |

### Notification Templates — `/notification-templates`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.notification_template:read` |
| GET | `/{id}` | `bpm.notification_template:read` |
| POST | `` | `bpm.notification_template:create` |
| PATCH | `/{id}` | `bpm.notification_template:update` |
| DELETE | `/{id}` | `bpm.notification_template:delete` |
| POST | `/{id}/enable` | `bpm.notification_template:enable` |
| POST | `/{id}/disable` | `bpm.notification_template:disable` |

**New Phase 3B routes:** 14

---

## Repositories

| Repository | Role |
|------------|------|
| `WorkflowTriggerRepository` | CRUD · list by definition · list by version · soft delete |
| `NotificationTemplateRepository` | CRUD · list by version · soft delete |

---

## Services

| Service | Role |
|---------|------|
| `WorkflowTriggerService` | CRUD · enable/disable · definition ownership · optional same-definition version bind · type payload rules |
| `NotificationTemplateService` | CRUD · enable/disable · version draft-only · content / JSON validation · Foundation delivery boundary |
| `WorkflowTriggerEngine` | Type · enable/disable · event/metadata payload rules |
| `NotificationTemplateEngine` | Type · enable/disable · subject/body · variables/localization JSON |
| `BpmApplicationService` | Facade wiring for Phase 3B |

**Tasks:** None required for Phase 3B (design-time triggers / templates only).

---

## Permissions

| Permission |
|------------|
| `bpm.trigger:read` · `create` · `update` · `delete` · `enable` · `disable` |
| `bpm.notification_template:read` · `create` · `update` · `delete` · `enable` · `disable` |

Roles re-synced: `BPM_ADMIN` · `PROCESS_DESIGNER` · `PROCESS_OWNER` · `WORKFLOW_OPERATOR` · `WORKFLOW_AUDITOR`

---

## Tests

| Suite | Coverage | Result |
|-------|----------|--------|
| Unit | Trigger types/payload · enable/disable · notification types/content · VOs | PASS |
| Security | Phase 3B permission presence · designer / owner / auditor slices | PASS |
| Integration | Models (15) · services · routes · no runtime / simulation | PASS |
| Prior Phase 1 / 1.5 / 2A / 2B / 3A | Engines · polish · designer · intelligence · governance · imports | PASS |
| **Total BPM** | | **99 passed** |

---

## Remaining Work for Phase 4

| Area | Remaining |
|------|-----------|
| Simulation | `bpm_simulation_run` |
| Runtime | `bpm_workflow_instance` · `bpm_workflow_task` · `bpm_workflow_history` · `bpm_task_delegation` |
| Engine | Trigger firing · Foundation Notification delivery handoff · instance execution on Published version only |
| UI | Trigger designer · notification template editor |

**Tables remaining after Phase 3B:** 5 of 20 ERD-25 business tables.

---

**Sprint 25 Phase 3B — Complete.**
