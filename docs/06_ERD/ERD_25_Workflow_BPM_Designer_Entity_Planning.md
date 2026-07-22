# ERD-25 — Entity Planning  
## Workflow & Business Process Management (BPM) Designer

| Field | Value |
|-------|--------|
| **Document** | ERD-25 Entity Planning |
| **Version** | 1.0 |
| **Status** | Ready for Architect Review |
| **Schema / Prefix (proposed)** | `bpm` / `bpm_` |
| **Business Tables** | Exactly **20** |
| **Aligned To** | FRD-25 (Locked) · Architecture Lock v1.1 (C-04 / DG-03) · Foundation Workflow Engine (ERD_01 `wf_*` — unchanged) |
| **Prior Release** | ERP Core v1.19-beta |

> **Planning only.** No Mermaid, SQL, migrations, APIs, or implementation in this document.

---

## 1. Proposed 20 Business Entities

| # | Table Name | Business Purpose |
|---|------------|------------------|
| 1 | `bpm_workflow_template` | Reusable Template Library entry (cross-module, version-controlled) |
| 2 | `bpm_workflow_definition` | Workflow definition bound to module / document type |
| 3 | `bpm_workflow_version` | Immutable published / draft versions of a definition |
| 4 | `bpm_designer_node` | Visual designer node (start, user task, approval, gateway, end, etc.) |
| 5 | `bpm_designer_transition` | Visual designer edge (sequential / parallel / conditional paths) |
| 6 | `bpm_decision_table` | Configurable decision tables for routing / approvals / decisions |
| 7 | `bpm_business_rule` | Business / decision rules influencing routing and outcomes |
| 8 | `bpm_workflow_variable` | Workflow variables / context keys for a definition version |
| 9 | `bpm_form_reference` | Dynamic Forms Runtime references (Low-Code owns forms) |
| 10 | `bpm_assignment_rule` | Dynamic / role-based assignment policies |
| 11 | `bpm_task_delegation` | Task delegation records |
| 12 | `bpm_escalation_policy` | Escalation policies |
| 13 | `bpm_sla_policy` | SLA policies, timers, and reminder rules |
| 14 | `bpm_workflow_trigger` | Event / manual / scheduled / API triggers |
| 15 | `bpm_workflow_instance` | Runtime workflow instance (orchestrates business entity UUID) |
| 16 | `bpm_workflow_task` | User / approval tasks (sequential & parallel) |
| 17 | `bpm_workflow_history` | Workflow action / history trail (approve, reject, delegate, escalate, recover) |
| 18 | `bpm_simulation_run` | Simulation / dry-run validation before publish |
| 19 | `bpm_notification_template` | Notification content templates (WHAT is delivered) |
| 20 | `bpm_workflow_category` | Reusable categories for organizing workflow templates |

---

## 2. Short Explanation of Each

### Design & Publishing

1. **`bpm_workflow_template`** — Catalog entry in the Workflow Template Library; seed for new definitions across modules (FR-BPM-030). Organized under `bpm_workflow_category`.
2. **`bpm_workflow_definition`** — Logical process identity (code, module, entity type, owner). Acts as the stable business identity across multiple workflow versions.
3. **`bpm_workflow_version`** — Draft / published / retired versions; published versions immutable for audit.
4. **`bpm_designer_node`** — Visual designer step/gateway/task nodes for a version.
5. **`bpm_designer_transition`** — Transitions between nodes; supports sequential, parallel join/split, and conditional branching. Routing and branching may evaluate **Decision Tables** and/or **Condition Expressions**.

### Intelligence & Context

6. **`bpm_decision_table`** — Tabular decision logic for routing / approvals (FR-BPM-028).
7. **`bpm_business_rule`** — Named business / decision rules referenced by nodes or transitions.
8. **`bpm_workflow_variable`** — Variable declarations and default/context mapping for a version.
9. **`bpm_form_reference`** — UUID / key reference to Low-Code dynamic forms; BPM orchestrates only (FR-BPM-027).

### Assignment & Governance

10. **`bpm_assignment_rule`** — Role / dynamic assignee resolution for tasks.
11. **`bpm_task_delegation`** — Runtime delegation from assignee to delegatee.
12. **`bpm_escalation_policy`** — Who/when/how to escalate overdue tasks.
13. **`bpm_sla_policy`** — SLA clocks, timers, reminder intervals.
14. **`bpm_workflow_trigger`** — How instances start (event, manual, schedule, API).

### Runtime & Observability

15. **`bpm_workflow_instance`** — Running/completed/failed/cancelled instance linked to `module + entity_id` (business SoR untouched).
16. **`bpm_workflow_task`** — User and approval tasks; parallel/sequential completion semantics.
17. **`bpm_workflow_history`** — Append-style history of actions for audit / recovery.
18. **`bpm_simulation_run`** — Pre-publish simulation / dry-run results (FR-BPM-029). Stores **status**, **duration**, **warnings**, and **errors** for the run. No separate simulation detail table.
19. **`bpm_notification_template`** — Defines **WHAT** notification content is delivered (subject/body/channel template refs). **Notification Rules** (when to send) are expressed via trigger / SLA / escalation / history events on the definition version — not a separate SoR table. **Foundation Notification** remains responsible for delivery.
20. **`bpm_workflow_category`** — Reusable categories for organizing workflow templates across ERP modules. Operational reporting remains with the **Analytics** module and existing reporting framework (no `bpm_report` table).

---

## 3. Cross-Module Ownership

| Concern | System of Record | BPM Role |
|---------|------------------|----------|
| Workflow categories / templates / definitions / versions / designer graph | **BPM (this module)** | Owns |
| Decision tables / business rules / variables | **BPM** | Owns |
| Assignment, delegation, escalation, SLA | **BPM** | Owns |
| Triggers | **BPM** | Owns |
| Workflow instances / tasks / history | **BPM** (C-04-aligned enterprise engine surface) | Owns |
| Simulation / dry-run | **BPM** | Owns |
| Notification templates (WHAT content) | **BPM** | Owns templates; **when** to notify is rule/event-driven; **Foundation Notification** delivers |
| Operational / enterprise reporting | **Analytics** + existing reporting framework | BPM does not own operational report tables |
| Business documents (PO, invoice, leave, ticket, etc.) | **Owning business module** | Orchestrates only (`entity_id` UUID) |
| Party / org masters | **Master Data / Organization (C-01)** | Consumes (`master_employee`, roles, dept) |
| Dynamic form definitions | **Low-Code Platform (Sprint 26)** | References only (`bpm_form_reference`) |
| Platform Notification / Audit / RBAC / Security | **Foundation** | Consumes |
| External connectors | **Integration Hub** | Transport for API/event triggers |
| Customer / Vendor Portal envelopes | **Portal modules** | Portals remain SoR for envelopes; BPM orchestrates `PT_*` / `VP_*` approvals |
| Foundation `wf_*` (ERD_01) | **Foundation (locked)** | Not redesigned; BPM extends product surface under C-04 / DG-03 |

### Primary Relationships (planning level)

| Entity | Primary Relationships | Cross-module integrations |
|--------|----------------------|---------------------------|
| `bpm_workflow_category` | → many templates | Cross-module template organization |
| `bpm_workflow_template` | → category; → many definitions | Used by all ERP modules as catalog |
| `bpm_workflow_definition` | → versions; optional ← template | Bound to module code (Finance…Portals) |
| `bpm_workflow_version` | → nodes, transitions, variables, rules, tables, form refs, policies, triggers | Immutable publish target for instances |
| `bpm_designer_node` | → version; ← transitions | May reference assignment / SLA / form / decision table |
| `bpm_designer_transition` | node → node | **Decision Tables** and/or **Condition Expressions** for routing |
| `bpm_decision_table` | → version | Routing decisions across modules |
| `bpm_business_rule` | → version | Shared rule evaluation |
| `bpm_workflow_variable` | → version | Context from business entity (read via service) |
| `bpm_form_reference` | → version / node | **Low-Code form UUID** only |
| `bpm_assignment_rule` | → version / node | **sec_role** / **master_employee** / org context |
| `bpm_task_delegation` | → task; users | Foundation Security users |
| `bpm_escalation_policy` | → version / node | Role / user escalation targets |
| `bpm_sla_policy` | → version / node | Timers / reminders |
| `bpm_workflow_trigger` | → definition / version | Events from modules · Hub · schedule · API |
| `bpm_workflow_instance` | → version; **module + entity_id** | Business module SoR unchanged |
| `bpm_workflow_task` | → instance; assignee | Approvers via RBAC / assignment |
| `bpm_workflow_history` | → instance / task | Foundation Audit continuity |
| `bpm_simulation_run` | → version | Pre-publish only; stores status · duration · warnings · errors; no business mutation |
| `bpm_notification_template` | → version / events | Foundation `ntf_*` delivery of **WHAT** content |

---

## 4. Entity Dependency Notes

```text
bpm_workflow_category
        ↓
bpm_workflow_template
        ↓ (optional seed)
bpm_workflow_definition
        ↓
bpm_workflow_version  ←── bpm_simulation_run (status · duration · warnings · errors)
        ├── bpm_designer_node
        │         └── bpm_designer_transition
        │                   (Decision Tables and/or Condition Expressions)
        ├── bpm_decision_table
        ├── bpm_business_rule
        ├── bpm_workflow_variable
        ├── bpm_form_reference          → Low-Code (Sprint 26) UUID only
        ├── bpm_assignment_rule
        ├── bpm_escalation_policy
        ├── bpm_sla_policy
        ├── bpm_workflow_trigger
        └── bpm_notification_template   → Foundation Notification (WHAT content)
                ↓ (after publish)
        bpm_workflow_instance  ←── business module entity UUID (SoR stays in module)
                ├── bpm_workflow_task
                │         └── bpm_task_delegation
                └── bpm_workflow_history

Operational reporting → Analytics + existing reporting framework (no bpm_report)
```

**Dependency rules (planning):**

1. **Version is the design unit** — nodes, transitions, rules, tables, variables, form refs, policies, and triggers hang off `bpm_workflow_version`.
2. **Transitions support Decision Tables and Condition Expressions** for routing and branching.
3. **Runtime hangs off published version** — instances never mutate design rows; history is append-oriented.
4. **Business entity is UUID-only** — no FK into peer business tables; no peer ORM writes.
5. **Forms are references only** — no form definition tables in BPM.
6. **Notification Templates define WHAT**; notification timing (WHEN) is event/rule-driven; Foundation delivers.
7. **Simulation stores status, duration, warnings, errors** on `bpm_simulation_run` — no extra table.
8. **Categories organize templates** — operational reports are not BPM SoR.
9. **C-01** — assignee/employee/org resolve via Master Data / Organization / Security only.
10. **C-04 / DG-03** — one enterprise approval path; ERD_01 not redesigned.
11. **Exactly 20 tables.**
12. **Only one Published Version may exist for a Workflow Definition at any point in time.** Draft and Retired versions may coexist, but only a single Published Version is eligible for runtime execution.

---

## Architect Review Notes (applied)

| Change | Result |
|--------|--------|
| `bpm_report` → `bpm_workflow_category` | Templates organized by category; reporting stays with Analytics |
| `bpm_notification_rule` → `bpm_notification_template` | Templates = WHAT; rules/events = WHEN; Foundation delivers |
| Designer transitions | Decision Tables **and** Condition Expressions |
| `bpm_simulation_run` | Stores status · duration · warnings · errors (same table) |

---

**Status:** Ready for Architect Review  

Entity Planning remains Ready for Architect Review.
