# ERP Core v1.20-beta — Release Notes

| Field | Value |
|-------|--------|
| **Document Type** | Enterprise Release Notes |
| **Release Name** | ERP Core v1.20-beta |
| **Release Status** | Release Ready |
| **Architecture Lock** | v1.1 — Maintained |
| **Prepared As** | Enterprise Solution Architect · ERP Product Architect · Technical Documentation Lead · Release Manager · Principal Software Engineer |
| **Classification** | Internal — Confidential |
| **Predecessor** | [ERP Core v1.19-beta](./ERP_Core_v1.19-beta.md) |
| **Ready For** | Sprint 26 — Low-Code Platform |

---

## 1. Release Overview

| Field | Value |
|-------|--------|
| **Version** | ERP Core v1.20-beta |
| **Status** | Release Ready |
| **Date** | 2026-07-22 |
| **Previous Release** | ERP Core v1.19-beta |
| **Sprint Delivered** | Sprint 25 — Workflow & BPM Designer |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-25 Locked · ERD-25 Locked |
| **Recommended Git Tag** | `v1.20-beta` |

Sprint 25 delivered the **Workflow & BPM Designer** domain as the enterprise design-time and runtime foundation for process definitions — categories → templates → definitions → versions → visual designer graph → decision tables / business rules / variables / form references → assignment / escalation / SLA → triggers / notification templates → workflow instances / tasks / history / delegations → simulation — while **Foundation `wf_*` remains untouched** (no competing engine redesign). Business modules remain Systems of Record. Peer bindings use **UUID / services only** — **no peer ORM writes**. Simulation never mutates business entities and never creates runtime instances.

---

## 2. Sprint Summary

| Attribute | Value |
|-----------|--------|
| **Sprint** | Sprint 25 |
| **Domain** | Workflow & BPM Designer |
| **Phases** | Phase 1 · Phase 1.5 · Phase 2A · Phase 2B · Phase 3A · Phase 3B · Phase 4 · Phase 5 |
| **Module** | `apps/api/src/modules/bpm/` |
| **Schema / Prefix** | `bpm` / `bpm_` |
| **Business Tables** | **20 of 20** (ERD-25 complete) |
| **API Mount** | `/api/v1/bpm` |
| **Alembic Head** | `0491_seed_bpm_phase5_permissions` |
| **BPM Tests** | **136 passed** |
| **Sprint Validation** | **PASS** |

| Phase | Scope | Outcome |
|-------|--------|---------|
| Phase 1 | Design spine — category · template · definition · version | Complete |
| Phase 1.5 | Publish validation · version compare · template import/export · dashboard polish | Complete |
| Phase 2A | Visual designer — nodes · transitions · graph validation | Complete |
| Phase 2B | Intelligence — decision tables · business rules · variables · form references | Complete |
| Phase 3A | Governance — assignment rules · escalation policies · SLA policies | Complete |
| Phase 3B | Communication — workflow triggers · notification templates (WHAT only) | Complete |
| Phase 4 | Runtime foundation — instances · tasks · history · delegations | Complete |
| Phase 5 | Simulation · graph-driven initial task generation polish | Complete |

---

## 3. Architecture Status

| Principle | Confirmation |
|-----------|--------------|
| **Architecture Lock v1.1** | **Preserved** — no Architecture Lock changes |
| **FRD-25 / ERD-25** | **Locked and implemented** (backend table scope) |
| **Clean Architecture** | Router → Service → Repository → Database maintained |
| **DDD** | BPM domain enums, exceptions, entities, value objects, engines |
| **Modular Monolith** | New `modules/bpm` package; no service-boundary redesign |
| **Foundation Workflow (`wf_*`)** | Unchanged — no competing engine / no redesign |
| **No duplicate masters** | Confirmed (C-01) |
| **No peer ORM writes** | Confirmed — UUID refs only for business SoR |
| **Published-only runtime** | Confirmed — draft versions not executable |
| **Append-only history** | Confirmed |
| **Previous modules** | Unchanged except required BPM wiring (router / Alembic env / permissions) |

Stack unchanged: FastAPI · SQLAlchemy 2.0 · Alembic · PostgreSQL · Redis · Celery · Next.js (frontend not in this sprint’s BPM UI scope).

---

## 4. Major Highlights

| Capability | Delivery |
|------------|----------|
| **BPM Module** | `apps/api/src/modules/bpm/` — Clean Architecture package (domain, models, repositories, engines, services, routers, adapters) |
| **Design Spine** | Category · Template · Definition · Version (Draft / Publish / Retire / Clone) |
| **Visual Designer** | Nodes · Transitions · Graph validation |
| **Intelligence** | Decision tables · Business rules · Variables · Form references (Low-Code UUID only) |
| **Governance** | Assignment rules · Escalation policies · SLA policies |
| **Communication** | Triggers (capability / bind) · Notification templates (WHAT; Foundation delivers) |
| **Runtime** | Instances · Tasks · History · Delegations — Published version only |
| **Simulation** | Dry-run validation / traversal / intelligence eval — no SoR mutation |
| **Runtime Polish** | Graph-driven initial task seed from published designer graph on instance start |
| **Application Facade** | `BpmApplicationService` wires all phase services |

**Supporting delivered items:** BPM document numbering (`CAT-` / `TPL-` / `DEF-` / `VER-` / `NOD-` / `TRN-` / `DTB-` / `RUL-` / `VAR-` / `FRM-` / `ASN-` / `ESC-` / `SLA-` / `TRG-` / `NTF-` / `INS-` / `TSK-` / `HST-` / `DLG-` / `SIM-`), RBAC roles (`BPM_ADMIN`, `PROCESS_DESIGNER`, `PROCESS_OWNER`, `WORKFLOW_OPERATOR`, `WORKFLOW_AUDITOR`), and Foundation Audit for entity change logging.

---

## 5. Workflow & BPM Designer

| Item | Value |
|------|--------|
| **Schema** | `bpm` |
| **Prefix** | `bpm_` |
| **Business Tables** | **20** |
| **ERD** | ERD-25 Workflow & BPM Designer (locked) |
| **FRD** | FRD-25 Workflow & BPM Designer Domain (locked) |
| **API mount** | `/api/v1/bpm` |

**Tables:** `bpm_workflow_category`, `bpm_workflow_template`, `bpm_workflow_definition`, `bpm_workflow_version`, `bpm_designer_node`, `bpm_designer_transition`, `bpm_decision_table`, `bpm_business_rule`, `bpm_workflow_variable`, `bpm_form_reference`, `bpm_assignment_rule`, `bpm_escalation_policy`, `bpm_sla_policy`, `bpm_workflow_trigger`, `bpm_notification_template`, `bpm_workflow_instance`, `bpm_workflow_task`, `bpm_workflow_history`, `bpm_task_delegation`, `bpm_simulation_run`.

### 5.1 Design Layer

| Table | Capability |
|-------|------------|
| `bpm_workflow_category` | Category CRUD · archive / restore |
| `bpm_workflow_template` | Template CRUD · copy · archive / restore · export / import validate · autocomplete · popular / recent |
| `bpm_workflow_definition` | Definition CRUD · stable identity across versions · archive / restore |
| `bpm_workflow_version` | Draft · Publish · Retire · Clone · Compare · Validate-publish · **one Published version per Definition** |

**Phase 1.5 polish:** publish validation · version comparison · template import/export validation · BPM dashboard summary.

### 5.2 Designer Layer

| Table | Capability |
|-------|------------|
| `bpm_designer_node` | Node CRUD — start / end / user_task / approval_task / gateways / timer / api / sub_workflow / validation |
| `bpm_designer_transition` | Transition CRUD — sequential / conditional / parallel / merge / split · condition expression · decision-table UUID ref |

**Graph validation:** exactly one Start · at least one End · orphan / connectivity / self-loop warnings · cycle detection option.

### 5.3 Intelligence Layer

| Table | Capability |
|-------|------------|
| `bpm_decision_table` | CRUD · rows JSON · enable / disable · priority / evaluation order |
| `bpm_business_rule` | CRUD · expression / decision / validation / routing types |
| `bpm_workflow_variable` | CRUD · typed variables · defaults · required flags |
| `bpm_form_reference` | CRUD · Low-Code form UUID reference only (no form definition ownership) |

Draft editable / Published version immutability enforced for design-time intelligence objects.

### 5.4 Governance Layer

| Table | Capability |
|-------|------------|
| `bpm_assignment_rule` | Role / user / department / dynamic targets · strategy metadata (UUID refs only) |
| `bpm_escalation_policy` | Escalation target / timing policies bound to version (optional node) |
| `bpm_sla_policy` | SLA timing · calendar UUID refs · optional node binding |

### 5.5 Communication Layer

| Table | Capability |
|-------|------------|
| `bpm_workflow_trigger` | Manual / event / api / schedule / webhook / message_queue · definition capability · optional version bind · enable / disable |
| `bpm_notification_template` | Email / SMS / push / in-app · **WHAT only** — Foundation Notification delivers |

Trigger **firing** and Foundation Notification **delivery** are deferred (templates / trigger definitions only in this release).

### 5.6 Runtime Foundation

| Table | Capability |
|-------|------------|
| `bpm_workflow_instance` | Create on **Published** version · start / cancel / suspend / resume / complete / fail · `module_code` + `entity_id` UUID |
| `bpm_workflow_task` | Assign / claim / release / complete / reject · sequential / parallel metadata · node binding |
| `bpm_workflow_history` | **Append-only** state / assignment / approval events |
| `bpm_task_delegation` | Delegate / accept / reject / expire · effective period |

**Runtime polish (Phase 5):** on instance `start()`, graph-driven initial task generation from published designer nodes via existing `WorkflowTaskService` — **no duplicate execution engine**.

### 5.7 Simulation

| Table | Capability |
|-------|------------|
| `bpm_simulation_run` | CRUD · Run · Validate · Cancel · duration · warnings · errors · execution trace · result summary |

**Guarantees:** Draft or Published versions only · never mutates business entities · never creates runtime instances · never sends notifications · never executes triggers · stores warnings/errors on the simulation row only.

---

## 6. API Summary

| Metric | Value |
|-------:|
| **Total FastAPI Routes** | **1871** |
| **Total OpenAPI Paths** | **1165** |
| **Total OpenAPI Operations** | **1867** |
| **BPM Route Count** | **140** |
| **BPM OpenAPI Paths** | **85** |
| **BPM OpenAPI Operations** | **140** |

**Mount:** `/api/v1/bpm`

Covered resource groups: dashboard · categories · templates · definitions · versions · nodes · transitions · graph validate · decision-tables · business-rules · variables · form-references · assignment-rules · escalation-policies · sla-policies · triggers · notification-templates · instances · tasks · history · delegations · simulations.

Swagger (`/docs`) and OpenAPI (`/openapi.json`) register BPM APIs under `/api/v1/bpm/*`.

---

## 7. Database Summary

| Item | Value |
|------|--------|
| **New Schema** | `bpm` |
| **BPM Business Tables** | **20** |
| **Alembic Head** | `0491_seed_bpm_phase5_permissions` |
| **Migration range (this release delta)** | `0465_create_bpm_schema` → `0491_seed_bpm_phase5_permissions` |
| **Prior head (v1.19-beta)** | `0464_seed_vp_workflows` |

```text
0464_seed_vp_workflows
        ↓
0465_create_bpm_schema
        ↓
… Sprint 25 Phase 1–5 migrations …
        ↓
0491_seed_bpm_phase5_permissions
```

---

## 8. Alembic

| Check | Result |
|-------|--------|
| **Current Head** | `0491_seed_bpm_phase5_permissions` |
| **Head Count** | 1 (single head) |
| **Chain** | Continuous `0465` → `0491` |
| **Status** | **PASS** |

---

## 9. OpenAPI

| Check | Result |
|-------|--------|
| OpenAPI generation | **PASS** |
| Swagger `/docs` | **PASS** |
| BPM paths registered | **85** |
| Platform OpenAPI paths | **1165** |

---

## 10. Route Count

| Scope | Count |
|-------|------:|
| Platform FastAPI routes | **1871** |
| BPM routes | **140** |
| BPM OpenAPI paths | **85** |

---

## 11. Quality Gates

| Gate | Status |
|------|--------|
| Alembic Head | **PASS** — `0491_seed_bpm_phase5_permissions` |
| FastAPI Startup | **PASS** |
| Swagger `/docs` | **PASS** |
| OpenAPI | **PASS** |
| BPM Router Registration | **PASS** |
| Ruff | **PASS** |
| MyPy | **PASS** |
| Pytest | **PASS** — **136** (BPM unit · security · integration) |
| Architecture Validation | **PASS** |
| Sprint 25 Final Validation | **PASS** |

---

## 12. Known Limitations

| Limitation | Notes |
|------------|--------|
| **UI not yet implemented** | BPM Designer canvas · simulation console · runtime inbox / instance monitor UX deferred |
| **Trigger execution deferred** | Trigger definitions / enablement exist; schedule / webhook / MQ / event consumers not executed in this release |
| **Foundation Notification delivery deferred** | `bpm_notification_template` defines WHAT; Foundation `ntf_*` delivery handoff not wired for BPM runtime in this release |
| **Continuous graph auto-routing** | Initial task seed on start is delivered; full post-completion graph routing depth remains future polish |
| **Foundation `wf_*`** | Intentionally unchanged — BPM Designer is complementary design/runtime store, not a redesign of Foundation Workflow |

---

## 13. Future Roadmap

| Attribute | Value |
|-----------|--------|
| **Next Release** | ERP Core **v1.21-beta** (planned) |
| **Next Sprint** | **Sprint 26 — Low-Code Platform** |
| **Primary domain** | Low-Code Platform (dynamic forms / builders per ERP roadmap) |

**Planned continuity (planning only — no implementation in this release):**

- Low-Code Platform form definitions consumed by `bpm_form_reference` UUID refs
- Optional BPM UI surfaces against existing `/api/v1/bpm` APIs
- Optional trigger execution / Foundation Notification delivery wiring without redesigning BPM tables
- No redesign of BPM · Foundation Workflow · Vendor Portal · prior business modules

---

## 14. Release Summary

| Item | Confirmation |
|------|----------------|
| Release document | `docs/07_RELEASES/ERP_Core_v1.20-beta.md` |
| Prior releases unmodified | `ERP_Core_v1.0-alpha.md` · `v1.1-beta` … · `v1.19-beta` unchanged |
| **Version** | **ERP Core v1.20-beta** |
| **Status** | **Release Ready** |
| **Modules** | Foundation · Organization · Master Data · Finance · Sales · Procurement · Inventory · Manufacturing · Quality · CRM · HR · Payroll · Recruitment · Project · Asset · Service · Helpdesk · Document · GRC · Analytics · Integration · E-Commerce · Customer Portal · Vendor Portal · **Workflow & BPM Designer** |
| **Alembic head** | **`0491_seed_bpm_phase5_permissions`** |
| **BPM tables** | **20 / 20** |
| **BPM tests** | **136 passed** |
| **Routes** | **1871** FastAPI · **1165** OpenAPI · **140** BPM |
| **Quality gates** | Ruff · MyPy · Pytest · Architecture · Alembic · OpenAPI — **PASS** |
| **Next** | **Sprint 26 — Low-Code Platform** |
| **Ready for Git Tag** | **`v1.20-beta`** |

---

## 15. Version Timeline

| Version | Date | Scope | Alembic Head | Tests |
|---------|------|--------|--------------|-------|
| **v1.18-beta** | 2026-07-16 | Sprints 0–23 (+ Customer Portal) | `0442_seed_portal_workflows` | 297 passed |
| **v1.19-beta** | 2026-07-20 | Sprints 0–24 (+ Supplier / Vendor Portal) | `0464_seed_vp_workflows` | Vendor Portal hub + suite |
| **v1.20-beta** | 2026-07-22 | Sprints 0–25 (+ Workflow & BPM Designer) | `0491_seed_bpm_phase5_permissions` | **136 BPM passed** |

```text
v1.19-beta ──(+ Sprint 25 Workflow & BPM Designer)──► v1.20-beta ──► Sprint 26 Low-Code Platform (planned)
```

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial ERP Core v1.20-beta release notes after Sprint 25 BPM Designer implementation and validation PASS |

---

**Confirmations**

- `ERP_Core_v1.20-beta.md` created successfully
- Previous release notes remain unchanged
- Sprint 25 Validation completed successfully (**PASS**)
- Ready for Git tag: **`v1.20-beta`**
- Ready to begin Sprint 26 — Low-Code Platform planning

**ERP Core v1.20-beta release documentation completed and ready for release approval.**

---

Engineering implementation reports for Sprint 25 are archived under

`docs/08_SPRINT_REPORTS/Sprint_25/`

`ERP_Core_v1.20-beta.md` remains the official release document.
