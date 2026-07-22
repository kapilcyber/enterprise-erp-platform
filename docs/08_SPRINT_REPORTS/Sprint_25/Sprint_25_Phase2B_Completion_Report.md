# Sprint 25 Phase 2B Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.20-beta |
| **Sprint** | Sprint 25 — Workflow & BPM Designer |
| **Phase** | Phase 2B — Workflow Intelligence Layer |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-25 / ERD-25 — Preserved |
| **Prior Phases** | Phase 1 · Phase 1.5 · Phase 2A — Complete |
| **Schema / Prefix** | `bpm` / `bpm_` |
| **New Tables** | 4 (`bpm_decision_table` · `bpm_business_rule` · `bpm_workflow_variable` · `bpm_form_reference`) |
| **Total BPM Tables** | 10 of 20 |
| **Alembic Head** | `0478_seed_bpm_phase2b_permissions` |
| **BPM Tests** | 67 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `bpm_decision_table` | CRUD · row management · priority · evaluation order · version binding · enable / disable |
| 2 | `bpm_business_rule` | CRUD · expression · rule type · status · version binding · decision table reference |
| 3 | `bpm_workflow_variable` | CRUD · types (string/number/boolean/date/json) · default · required · encrypted |
| 4 | `bpm_form_reference` | CRUD · Low-Code form UUID · node binding · access mode · validation JSON |

### Validation Rules Enforced

- Decision tables, business rules, variables, and form references belong to **one** workflow version
- **Draft** versions editable; **Published** versions immutable
- Business rule `decision_table_id` must reference a table in the **same** version
- Form reference `node_id` (optional) must reference a node in the **same** version
- Form references store **Low-Code UUID only** — no form definition ownership
- No peer ORM writes · no runtime · no instances · no assignment / SLA / escalation

### Explicitly Not Done

- Runtime · instances · tasks · history · task delegation
- Assignment · SLA · escalation · notification templates · triggers · simulation
- Workflow execution engine · evaluation at runtime
- Low-Code form ownership / peer module writes

---

## Files Created

### Domain / Models / Repositories

| File |
|------|
| `apps/api/src/modules/bpm/models/decision_table.py` |
| `apps/api/src/modules/bpm/models/business_rule.py` |
| `apps/api/src/modules/bpm/models/workflow_variable.py` |
| `apps/api/src/modules/bpm/models/form_reference.py` |
| `apps/api/src/modules/bpm/repository/decision_table_repository.py` |
| `apps/api/src/modules/bpm/repository/business_rule_repository.py` |
| `apps/api/src/modules/bpm/repository/workflow_variable_repository.py` |
| `apps/api/src/modules/bpm/repository/form_reference_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/bpm/service/decision_table_service.py` |
| `apps/api/src/modules/bpm/service/business_rule_service.py` |
| `apps/api/src/modules/bpm/service/workflow_variable_service.py` |
| `apps/api/src/modules/bpm/service/form_reference_service.py` |
| `apps/api/src/modules/bpm/service/engines/intelligence_engines.py` |

### Migrations

| Revision | File |
|----------|------|
| `0475_bpm_decision_table` | `apps/api/alembic/versions/0475_bpm_decision_table.py` |
| `0476_bpm_business_rule` | `apps/api/alembic/versions/0476_bpm_business_rule.py` |
| `0477_bpm_variable_form_reference` | `apps/api/alembic/versions/0477_bpm_variable_form_reference.py` |
| `0478_seed_bpm_phase2b_permissions` | `apps/api/alembic/versions/0478_seed_bpm_phase2b_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/bpm/test_bpm_phase2b_intelligence.py` |
| `apps/api/src/tests/security/bpm/test_bpm_phase2b_permissions.py` |
| `apps/api/src/tests/integration/bpm/test_bpm_phase2b_module_import.py` |

### Report

| File |
|------|
| `docs/07_RELEASES/Sprint_25_Phase2B_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/bpm/domain/enums.py` | Decision / rule / variable / form enums · code prefixes |
| `apps/api/src/modules/bpm/domain/exceptions.py` | Intelligence-layer exceptions |
| `apps/api/src/modules/bpm/domain/entities.py` | Intelligence identities |
| `apps/api/src/modules/bpm/models/__init__.py` | Export Phase 2B models (10 total) |
| `apps/api/src/modules/bpm/service/engines/__init__.py` | Export intelligence engines |
| `apps/api/src/modules/bpm/service/application_service.py` | Wire decision tables · rules · variables · form refs |
| `apps/api/src/modules/bpm/service/__init__.py` | Export Phase 2B services |
| `apps/api/src/modules/bpm/schemas.py` | Intelligence Create / Update / Response · row payloads |
| `apps/api/src/modules/bpm/permissions.py` | Phase 2B permissions · role slices |
| `apps/api/src/modules/bpm/routers/__init__.py` | Decision tables · rules · variables · form refs routes |
| `apps/api/src/modules/bpm/router.py` | Include Phase 2B routers |
| `apps/api/src/tests/integration/bpm/test_bpm_hub_module_import.py` | Model count → 10 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase15_module_import.py` | Model count → 10 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase2a_module_import.py` | Model count → 10 · intelligence present |

---

## APIs

**Mount:** `/api/v1/bpm`

### Decision Tables — `/decision-tables`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.decision_table:read` |
| GET | `/{id}` | `bpm.decision_table:read` |
| POST | `` | `bpm.decision_table:create` |
| PATCH | `/{id}` | `bpm.decision_table:update` |
| DELETE | `/{id}` | `bpm.decision_table:delete` |
| POST | `/{id}/enable` | `bpm.decision_table:enable` |
| POST | `/{id}/disable` | `bpm.decision_table:disable` |
| PUT | `/{id}/rows` | `bpm.decision_table:update` |
| POST | `/{id}/rows` | `bpm.decision_table:update` |
| PATCH | `/{id}/rows/{decision_row_id}` | `bpm.decision_table:update` |
| DELETE | `/{id}/rows/{decision_row_id}` | `bpm.decision_table:update` |

### Business Rules — `/business-rules`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.business_rule:read` |
| GET | `/{id}` | `bpm.business_rule:read` |
| POST | `` | `bpm.business_rule:create` |
| PATCH | `/{id}` | `bpm.business_rule:update` |
| DELETE | `/{id}` | `bpm.business_rule:delete` |

### Variables — `/variables`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.variable:read` |
| GET | `/{id}` | `bpm.variable:read` |
| POST | `` | `bpm.variable:create` |
| PATCH | `/{id}` | `bpm.variable:update` |
| DELETE | `/{id}` | `bpm.variable:delete` |

### Form References — `/form-references`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.form_reference:read` |
| GET | `/{id}` | `bpm.form_reference:read` |
| POST | `` | `bpm.form_reference:create` |
| PATCH | `/{id}` | `bpm.form_reference:update` |
| DELETE | `/{id}` | `bpm.form_reference:delete` |

**New Phase 2B routes:** 26

---

## Repositories

| Repository | Role |
|------------|------|
| `DecisionTableRepository` | CRUD · list by version · soft delete |
| `BusinessRuleRepository` | CRUD · list by version · soft delete |
| `WorkflowVariableRepository` | CRUD · list by version · soft delete |
| `FormReferenceRepository` | CRUD · list by version · soft delete |

---

## Services

| Service | Role |
|---------|------|
| `DecisionTableService` | CRUD · enable/disable · row replace/add/update/remove · draft-only · audit |
| `BusinessRuleService` | CRUD · type/expression validation · same-version decision table ref |
| `WorkflowVariableService` | CRUD · type/key validation · required/encrypted flags |
| `FormReferenceService` | CRUD · Low-Code UUID only · optional same-version node bind · access mode |
| `DecisionTableEngine` | Enable/disable · rows_json validation |
| `BusinessRuleEngine` | Rule type · expression required |
| `WorkflowVariableEngine` | Variable type · key required |
| `FormReferenceEngine` | Access mode · form UUID required |
| `BpmApplicationService` | Facade wiring for Phase 2B |

**Tasks:** None required for Phase 2B (design-time intelligence only).

---

## Permissions

| Permission |
|------------|
| `bpm.decision_table:read` · `create` · `update` · `delete` · `enable` · `disable` |
| `bpm.business_rule:read` · `create` · `update` · `delete` |
| `bpm.variable:read` · `create` · `update` · `delete` |
| `bpm.form_reference:read` · `create` · `update` · `delete` |

Roles re-synced: `BPM_ADMIN` · `PROCESS_DESIGNER` · `PROCESS_OWNER` · `WORKFLOW_OPERATOR` · `WORKFLOW_AUDITOR`

---

## Tests

| Suite | Coverage | Result |
|-------|----------|--------|
| Unit | Decision enable/disable · rows_json · rule types · variable types · form modes | PASS |
| Security | Phase 2B permission presence · designer / owner / auditor slices | PASS |
| Integration | Models (10) · services · routes · no runtime models | PASS |
| Prior Phase 1 / 1.5 / 2A | Engines · polish · designer · imports | PASS |
| **Total BPM** | | **67 passed** |

---

## Remaining Work for Phase 3

| Area | Remaining |
|------|-----------|
| Governance | `bpm_assignment_rule` · `bpm_escalation_policy` · `bpm_sla_policy` |
| Triggers / Comms | `bpm_workflow_trigger` · `bpm_notification_template` |
| Simulation | `bpm_simulation_run` |
| Runtime (later) | `bpm_workflow_instance` · `bpm_workflow_task` · `bpm_workflow_history` · `bpm_task_delegation` |
| UI | Decision table editor · variable/form binding UX |
| Engine | Runtime evaluation of rules / tables on Published version only |

**Tables remaining after Phase 2B:** 10 of 20 ERD-25 business tables.

---

**Sprint 25 Phase 2B — Complete.**
