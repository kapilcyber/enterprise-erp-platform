# Sprint 25 Phase 3A Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.20-beta |
| **Sprint** | Sprint 25 — Workflow & BPM Designer |
| **Phase** | Phase 3A — Governance Layer |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-25 / ERD-25 — Preserved |
| **Prior Phases** | Phase 1 · Phase 1.5 · Phase 2A · Phase 2B — Complete |
| **Schema / Prefix** | `bpm` / `bpm_` |
| **New Tables** | 3 (`bpm_assignment_rule` · `bpm_escalation_policy` · `bpm_sla_policy`) |
| **Total BPM Tables** | 13 of 20 |
| **Alembic Head** | `0482_seed_bpm_phase3a_permissions` |
| **BPM Tests** | 83 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `bpm_assignment_rule` | CRUD · role / user / department / dynamic · priority · fallback · round-robin / load-balance metadata |
| 2 | `bpm_escalation_policy` | CRUD · levels · delay · target · reason · retry · multi-level JSON |
| 3 | `bpm_sla_policy` | CRUD · business hours · calendar / holiday calendar UUID · reminders · warning / breach · timezone |

### Validation Rules Enforced

- All governance objects belong to **one** workflow version
- Optional node binding must be same-version
- **Draft** editable; **Published** immutable
- Assignment targets are **UUID-only** (Security role / user · Organization department · Master Employee)
- Escalation targets are **UUID-only** (role / user / department)
- SLA calendars are **UUID references only** — no ownership
- No peer ORM writes · no runtime · no triggers · no notification templates · no instances / tasks / history

### Explicitly Not Done

- Runtime · instances · tasks · history · task delegation
- Triggers · notification templates · simulation
- Workflow execution · SLA clock evaluation at runtime
- Assignment resolution engine at runtime

---

## Files Created

### Domain / Models / Repositories

| File |
|------|
| `apps/api/src/modules/bpm/models/assignment_rule.py` |
| `apps/api/src/modules/bpm/models/escalation_policy.py` |
| `apps/api/src/modules/bpm/models/sla_policy.py` |
| `apps/api/src/modules/bpm/repository/assignment_rule_repository.py` |
| `apps/api/src/modules/bpm/repository/escalation_policy_repository.py` |
| `apps/api/src/modules/bpm/repository/sla_policy_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/bpm/service/assignment_rule_service.py` |
| `apps/api/src/modules/bpm/service/escalation_policy_service.py` |
| `apps/api/src/modules/bpm/service/sla_policy_service.py` |
| `apps/api/src/modules/bpm/service/engines/governance_engines.py` |

### Migrations

| Revision | File |
|----------|------|
| `0479_bpm_assignment_rule` | `apps/api/alembic/versions/0479_bpm_assignment_rule.py` |
| `0480_bpm_escalation_policy` | `apps/api/alembic/versions/0480_bpm_escalation_policy.py` |
| `0481_bpm_sla_policy` | `apps/api/alembic/versions/0481_bpm_sla_policy.py` |
| `0482_seed_bpm_phase3a_permissions` | `apps/api/alembic/versions/0482_seed_bpm_phase3a_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/bpm/test_bpm_phase3a_governance.py` |
| `apps/api/src/tests/security/bpm/test_bpm_phase3a_permissions.py` |
| `apps/api/src/tests/integration/bpm/test_bpm_phase3a_module_import.py` |

### Report

| File |
|------|
| `docs/07_RELEASES/Sprint_25_Phase3A_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/bpm/domain/enums.py` | Assignment / escalation / SLA enums · code prefixes |
| `apps/api/src/modules/bpm/domain/exceptions.py` | Governance exceptions |
| `apps/api/src/modules/bpm/domain/entities.py` | Governance identities |
| `apps/api/src/modules/bpm/domain/value_objects.py` | Assignment / escalation / SLA value objects |
| `apps/api/src/modules/bpm/models/__init__.py` | Export Phase 3A models (13 total) |
| `apps/api/src/modules/bpm/service/engines/__init__.py` | Export governance engines |
| `apps/api/src/modules/bpm/service/application_service.py` | Wire assignment · escalation · SLA |
| `apps/api/src/modules/bpm/service/__init__.py` | Export Phase 3A services |
| `apps/api/src/modules/bpm/schemas.py` | Governance Create / Update / Response schemas |
| `apps/api/src/modules/bpm/permissions.py` | Phase 3A permissions · role slices |
| `apps/api/src/modules/bpm/routers/__init__.py` | Assignment · escalation · SLA routes |
| `apps/api/src/modules/bpm/router.py` | Include Phase 3A routers |
| `apps/api/src/tests/integration/bpm/test_bpm_hub_module_import.py` | Model count → 13 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase15_module_import.py` | Model count → 13 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase2a_module_import.py` | Model count → 13 |
| `apps/api/src/tests/integration/bpm/test_bpm_phase2b_module_import.py` | Model count → 13 · governance present |

---

## APIs

**Mount:** `/api/v1/bpm`

### Assignment Rules — `/assignment-rules`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.assignment_rule:read` |
| GET | `/{id}` | `bpm.assignment_rule:read` |
| POST | `` | `bpm.assignment_rule:create` |
| PATCH | `/{id}` | `bpm.assignment_rule:update` |
| DELETE | `/{id}` | `bpm.assignment_rule:delete` |

### Escalation Policies — `/escalation-policies`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.escalation_policy:read` |
| GET | `/{id}` | `bpm.escalation_policy:read` |
| POST | `` | `bpm.escalation_policy:create` |
| PATCH | `/{id}` | `bpm.escalation_policy:update` |
| DELETE | `/{id}` | `bpm.escalation_policy:delete` |

### SLA Policies — `/sla-policies`

| Method | Path | Permission |
|--------|------|------------|
| GET | `?version_id=` | `bpm.sla_policy:read` |
| GET | `/{id}` | `bpm.sla_policy:read` |
| POST | `` | `bpm.sla_policy:create` |
| PATCH | `/{id}` | `bpm.sla_policy:update` |
| DELETE | `/{id}` | `bpm.sla_policy:delete` |

**New Phase 3A routes:** 15

---

## Repositories

| Repository | Role |
|------------|------|
| `AssignmentRuleRepository` | CRUD · list by version · soft delete |
| `EscalationPolicyRepository` | CRUD · list by version · soft delete |
| `SlaPolicyRepository` | CRUD · list by version · soft delete |

---

## Services

| Service | Role |
|---------|------|
| `AssignmentRuleService` | CRUD · type/strategy validation · UUID targets · draft-only · audit |
| `EscalationPolicyService` | CRUD · level / delay / retry / levels_json · UUID target |
| `SlaPolicyService` | CRUD · thresholds · timezone · business hours / reminders JSON · calendar UUID refs |
| `AssignmentRuleEngine` | Type · strategy · target · metadata validation |
| `EscalationPolicyEngine` | Target type · level · delay · retry · levels_json |
| `SlaPolicyEngine` | Timezone · thresholds · JSON payload validation |
| `BpmApplicationService` | Facade wiring for Phase 3A |

**Tasks:** None required for Phase 3A (design-time governance only).

---

## Permissions

| Permission |
|------------|
| `bpm.assignment_rule:read` · `create` · `update` · `delete` |
| `bpm.escalation_policy:read` · `create` · `update` · `delete` |
| `bpm.sla_policy:read` · `create` · `update` · `delete` |

Roles re-synced: `BPM_ADMIN` · `PROCESS_DESIGNER` · `PROCESS_OWNER` · `WORKFLOW_OPERATOR` · `WORKFLOW_AUDITOR`

---

## Tests

| Suite | Coverage | Result |
|-------|----------|--------|
| Unit | Assignment types/strategies · escalation rules · SLA thresholds · VOs | PASS |
| Security | Phase 3A permission presence · designer / owner / auditor slices | PASS |
| Integration | Models (13) · services · routes · no runtime models | PASS |
| Prior Phase 1 / 1.5 / 2A / 2B | Engines · polish · designer · intelligence · imports | PASS |
| **Total BPM** | | **83 passed** |

---

## Remaining Work for Phase 3B

| Area | Remaining |
|------|-----------|
| Triggers / Comms | `bpm_workflow_trigger` · `bpm_notification_template` |
| Simulation | `bpm_simulation_run` |
| Runtime (later) | `bpm_workflow_instance` · `bpm_workflow_task` · `bpm_workflow_history` · `bpm_task_delegation` |
| UI | Governance policy editors · assignment strategy UX |
| Engine | Runtime assignment resolution · SLA clock · escalation execution on Published version only |

**Tables remaining after Phase 3A:** 7 of 20 ERD-25 business tables.

---

**Sprint 25 Phase 3A — Complete.**
