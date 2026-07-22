# FRD-25 — Workflow & Business Process Management (BPM) Designer

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document ID** | FRD-25 |
| **Document Title** | Workflow & Business Process Management (BPM) Designer Domain |
| **Domain** | Workflow & BPM Designer |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Classification** | Internal — Confidential |
| **Aligned To** | BRD v1.0 (FR-005) · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · FRD-01 Foundation Workflow Engine (C-04 / DG-03) · ERP Core v1.19-beta |
| **Sprint** | Sprint 25 (planning) |
| **Predecessor Release** | ERP Core v1.19-beta |
| **Planned Delivery** | ERP Core v1.20-beta (planned) |

### Cross References

- Upstream / platform: [FRD-01 Foundation Domain](./FRD-01-Foundation-Domain.md) (Workflow Engine · Notification Engine · Audit Engine · RBAC) · [FRD-02 Organization Domain](./FRD-02-Organization-Domain.md) · [FRD-03 Master Data Domain](./FRD-03-Master-Data-Domain.md)
- Consuming business domains: FRD-04 Finance · FRD-05 CRM · FRD-06 Sales · FRD-07 Procurement · FRD-08 Inventory · FRD-09 HR · FRD-10 Payroll · FRD-11 Project · FRD-12 Asset · FRD-13 Manufacturing · FRD-14 Quality · FRD-15 Supply Chain · FRD-16 Service · FRD-17 Helpdesk · FRD-18 Analytics · FRD-19 Document · FRD-20 GRC · FRD-21 Integration Hub · FRD-22 E-Commerce · [FRD-23 Customer Portal](./FRD-23-Customer-Portal-Domain.md) · [FRD-24 Vendor Portal](./FRD-24-Supplier-Vendor-Portal-Domain.md)
- Architecture: [Architecture Lock v1.1](../05_ARCHITECTURE_LOCK/ERP_Architecture_Lock_Report_v1.1.md)
- Prior release: [ERP Core v1.19-beta](../07_RELEASES/ERP_Core_v1.19-beta.md)

---

## 2. Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | Initial FRD-25 Workflow & BPM Designer for Sprint 25 architect review. Extends Foundation Workflow Engine (C-04 / DG-03). No redesign of prior modules. Architect review improvements: Dynamic Forms Runtime Integration, Decision Tables, Workflow Simulation / Dry Run Validation. |
| 1.1 | 2026-07-20 | Editorial lock after architect review. Cross references synchronized for Sprint 25 planning. No functional changes. |

---

## 3. Purpose

Provide a **centralized Workflow & BPM Designer platform** for designing, publishing, executing, monitoring, and governing business workflows across the ERP — enabling business users and administrators to create reusable workflow templates, approval processes, routing rules, SLAs, escalation policies, and workflow analytics **without changing application code**.

This domain **productizes and extends** the Foundation Workflow Engine already mandated by Architecture Lock v1.1 (C-04 / DG-03). It becomes the **enterprise workflow design and governance experience** consumed by every ERP module. It **does not** become the system of record for business documents or master data.

---

## 4. Business Overview

Workflow & BPM Designer is an **orchestration and governance** domain:

- **Design:** workflow templates, definitions, visual designer, versioning, publishing
- **Execution:** workflow execution engine, instances, tasks (user / approval), parallel and sequential approvals
- **Intelligence:** conditional branching, decision rules, decision tables, business rules, workflow variables, forms mapping
- **Assignment:** dynamic assignment, role assignment, delegation
- **Governance:** escalation, SLA policies, timers, reminder rules
- **Triggers:** event, manual, scheduled, API triggers
- **Communications:** email and in-app notifications (via Foundation Notification Engine)
- **Observability:** history, audit trail, process monitoring, KPI dashboard, process analytics, failed workflow recovery, simulation, dry-run validation, reports
- **Forms orchestration:** Dynamic Forms Runtime Integration — workflow definitions may reference reusable dynamic forms; forms remain owned by the future Low-Code Platform (Sprint 26)

| Concern | Authority |
|---------|-----------|
| Workflow design / definition / publish | Workflow & BPM Designer (this FRD) |
| Workflow execution / instances / tasks / history | Workflow & BPM Designer **on Foundation Workflow Engine (C-04)** — single enterprise engine; no parallel approval bypass |
| Dynamic form definitions | Future Low-Code Platform (Sprint 26) — Workflow references only |
| Business documents (PO, invoice, leave, ticket, etc.) | Owning business module (SoR) |
| Party / item masters | Master Data / Organization (C-01) |
| Notifications transport | Foundation Notification Engine |
| Security / RBAC / sessions | Foundation Security |
| Cross-system transport | Integration Hub |
| Analytics consumption | Analytics (read-only metrics) |

**Architectural stance:** There is **one** enterprise Workflow Engine (Architecture Lock). FRD-25 is the **BPM Designer + governance + monitoring product surface** that matures Foundation workflow capabilities for all modules. It **must not** introduce a second competing approval engine or bypass C-04 / DG-03.

---

## 5. Objectives

1. Enable no-code / low-code design of reusable workflow templates and definitions.
2. Provide a visual workflow designer for sequential, parallel, and conditional processes.
3. Support process versioning and controlled publishing.
4. Execute and monitor workflow instances and tasks consistently across all ERP modules.
5. Enforce SLA, escalation, delegation, and reminder policies.
6. Support event, manual, scheduled, and API triggers.
7. Deliver workflow history, auditability, KPI monitoring, analytics, recovery, simulation, and dry-run validation.
8. Orchestrate Dynamic Forms Runtime references without owning form definitions (Low-Code Platform remains forms SoR).
9. Preserve Architecture Lock v1.1: Clean Architecture, DDD, Modular Monolith, C-01, C-04, DG-03.
10. Ensure business modules remain systems of record; workflow only orchestrates.

---

## 6. Business Scope

Scope covers **Sprint 25 Workflow & BPM Designer** functional requirements for enterprise workflow design, execution governance, task management, SLA/escalation, triggers, notifications, monitoring, analytics, recovery, simulation, dry-run validation, decision tables, dynamic forms runtime integration, and reporting — integrated with Foundation Workflow / Notification / Audit / RBAC and consumed by all locked ERP domains (FRD-01 through FRD-24) and future modules.

---

## 7. In Scope

### Expected Capabilities

- Workflow templates and workflow definitions
- Workflow Template Library (version-controlled reusable templates across ERP modules)
- Visual workflow designer
- Process versioning and workflow publishing
- Workflow execution engine (enterprise, C-04-aligned)
- Workflow instances and workflow tasks
- User tasks and approval tasks
- Parallel approvals and sequential approvals
- Conditional branching, decision rules, decision tables, business rules
- Workflow variables and forms mapping
- Dynamic Forms Runtime Integration
- Dynamic assignment, role assignment, delegation
- Escalation, SLA policies, timers, reminder rules
- Event triggers, manual triggers, scheduled triggers, API triggers
- Email notifications and in-app notifications (via Foundation Notification)
- Workflow history and audit trail
- Process monitoring, KPI dashboard, process analytics
- Failed workflow recovery
- Workflow Simulation
- Dry Run Validation
- Workflow reports
- Integration contracts for all existing ERP modules and future modules

**Dynamic Forms Runtime Integration — Purpose:** Workflow definitions may reference reusable dynamic forms provided by the future Low-Code Platform. The Workflow module orchestrates forms. The Workflow module does **NOT** own forms. Forms remain owned by the future Low-Code Platform (Sprint 26).

---

## 8. Out of Scope

- Redesign or replacement of FRD-01 Foundation as a separate product
- Owning business transactional data (orders, invoices, leave, tickets, etc.)
- Owning dynamic form definitions (Low-Code Platform / Sprint 26 remains forms SoR)
- Duplicate masters (C-01 forbidden)
- Bypassing Workflow Engine for business approvals (forbidden — C-04 / DG-03)
- Replacing Foundation Notification Engine or Audit Engine
- Replacing Analytics as enterprise BI SoR (BPM consumes / contributes metrics only)
- Full external BPMN-suite product replacement of Architecture Lock stack
- Redesign of Customer Portal, Vendor Portal, or any prior business module
- Implementation artifacts in this FRD (ERD, schema, APIs, code, migrations)

---

## 9. Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| Business process owners | Accurate, maintainable approval and routing processes |
| Process designers / BPM admins | Visual design, versioning, publish control |
| Module owners (Finance, HR, Procurement, etc.) | Compliant orchestration without losing SoR |
| End users / approvers | Clear tasks, SLA, delegation, reminders |
| Security / Compliance | Audit trail, RBAC, segregation of duties |
| Operations / Support | Monitoring, failed recovery, KPIs |
| Enterprise Architect | Architecture Lock v1.1 · C-04 · DG-03 compliance |

---

## 10. User Roles

| Role | Intent |
|------|--------|
| `BPM_ADMIN` | Full BPM design, publish, recover, and governance control |
| `PROCESS_DESIGNER` | Create / version templates and definitions; submit for publish |
| `PROCESS_OWNER` | Own process outcomes; approve publish; monitor KPIs for owned processes |
| `WORKFLOW_OPERATOR` | Operate runtime instances; reassign; recover failed instances within policy |
| `WORKFLOW_AUDITOR` | Read-only history, audit, and compliance reporting |
| `APPROVER` / business roles | Execute user and approval tasks via module + workflow task inbox (existing domain roles) |

Namespace (planned): **`bpm.*`** / **`workflow.*`** (final seed naming aligned to Foundation RBAC conventions at ERD/implementation time — this FRD does not prescribe schema).

---

## 11. Business Processes

### 11.1 Template design
Create reusable workflow template → configure steps / rules / variables → save draft.

### 11.2 Definition & visual design
Author workflow definition in visual designer → sequential / parallel / conditional paths → map forms and variables → configure decision tables.

### 11.3 Simulate & validate
Run workflow simulation / dry-run validation → correct design issues → prepare for publish.

### 11.4 Version & publish
Create new version → validate → publish → prior version retired or kept for in-flight instances.

### 11.5 Trigger & start
Event / manual / schedule / API trigger starts instance bound to a business entity UUID in owning module.

### 11.6 Task execution
Create user / approval tasks → assign by role or dynamic rule → approve / reject / delegate → advance (forms rendered via Dynamic Forms Runtime references when mapped).

### 11.7 SLA & escalation
Timer / SLA clock → reminder → escalate per policy → notify.

### 11.8 Complete / cancel / recover
Instance completes or cancels; failed instances recoverable under operator policy without corrupting business SoR.

### 11.9 Monitor & analyze
History + KPI dashboard + analytics + reports for compliance and continuous improvement.

---

## 12. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-BPM-001 | System shall support reusable workflow templates configurable without application code changes. |
| FR-BPM-002 | System shall support workflow definitions bound to module and document/entity type. |
| FR-BPM-003 | System shall provide a visual workflow designer for steps, transitions, and gateways. |
| FR-BPM-004 | System shall support process versioning with immutable published versions for auditability. |
| FR-BPM-005 | System shall support controlled workflow publishing (draft → published → retired). |
| FR-BPM-006 | System shall execute workflows through the enterprise Workflow Engine aligned to C-04 / DG-03. |
| FR-BPM-007 | System shall manage workflow instances linked to business entity references (module + entity UUID) without owning business data. |
| FR-BPM-008 | System shall manage workflow tasks including user tasks and approval tasks. |
| FR-BPM-009 | System shall support sequential approvals. |
| FR-BPM-010 | System shall support parallel approvals (including join / completion rules). |
| FR-BPM-011 | System shall support conditional branching based on decision rules and workflow variables. |
| FR-BPM-012 | System shall support configurable business rules influencing routing and outcomes. |
| FR-BPM-013 | System shall support workflow variables and forms mapping to business context fields (by reference). |
| FR-BPM-014 | System shall support dynamic assignment and role-based assignment. |
| FR-BPM-015 | System shall support delegation of tasks. |
| FR-BPM-016 | System shall support escalation policies. |
| FR-BPM-017 | System shall support SLA policies, timers, and reminder rules. |
| FR-BPM-018 | System shall support event, manual, scheduled, and API triggers. |
| FR-BPM-019 | System shall send email and in-app notifications via Foundation Notification Engine. |
| FR-BPM-020 | System shall retain workflow history and an audit trail of actions (approve, reject, delegate, escalate, recover). |
| FR-BPM-021 | System shall provide process monitoring and a KPI dashboard. |
| FR-BPM-022 | System shall provide process analytics (consumed by / exported to Analytics read patterns). |
| FR-BPM-023 | System shall support failed workflow recovery without mutating peer business SoR data directly. |
| FR-BPM-024 | System shall provide workflow operational reports. |
| FR-BPM-025 | System shall be consumable by all existing ERP modules and future modules via service contracts only. |
| FR-BPM-026 | System shall never replace C-01 masters or peer business ledgers. |
| FR-BPM-027 | System shall support Dynamic Forms Runtime integration through reusable form references without owning form definitions. |
| FR-BPM-028 | System shall support configurable Decision Tables for routing, approvals and business decisions without application code changes. |
| FR-BPM-029 | System shall support workflow simulation and dry-run validation before publishing workflow definitions. |
| FR-BPM-030 | System shall provide a reusable Workflow Template Library supporting version-controlled reusable templates across ERP modules. |

---

## 13. Module Features

| Feature Area | Capabilities |
|--------------|--------------|
| Design Studio | Templates · Template Library · Definitions · Visual Designer · Versioning · Publishing |
| Execution | Engine · Instances · Tasks · User / Approval tasks |
| Routing | Sequential · Parallel · Conditional Branching · Decision Rules · Decision Tables · Business Rules |
| Context | Variables · Forms mapping · Dynamic Forms Runtime Integration (reference only) |
| Assignment | Dynamic · Role · Delegation |
| Governance | Escalation · SLA · Timers · Reminders |
| Triggers | Event · Manual · Scheduled · API |
| Comms | Email · In-app (Foundation Notification) |
| Observability | History · Audit · Monitoring · KPI · Analytics · Recovery · Simulation · Dry Run Validation · Reports |

---

## 14. Business Rules

1. **Single enterprise Workflow Engine** — all business approvals flow through Workflow Engine (C-04 / DG-03); no module-local approval bypass.
2. **Orchestration only** — Workflow does not own business transactional data; modules remain SoR.
3. **C-01** — no duplicate employee / customer / vendor / product / department masters.
4. **Foundation alignment** — FRD-25 extends / productizes Foundation Workflow Engine; it does not redesign FRD-01 or create a competing engine.
5. **Published versions are immutable** for in-flight and historical audit integrity.
6. **In-flight instances** remain on the definition version they started unless an explicit migration policy is applied.
7. **Notifications** use Foundation Notification Engine; BPM does not invent a parallel notification SoR.
8. **Audit** significant design publishes and all runtime actions; integrate with Foundation Audit.
9. **Peer access** via services / events / UUID refs only — no peer ORM writes.
10. **Finance journals** (if any fee/posting side-effect ever configured) only via `PostingService.post_system_journal()`.
11. **Analytics** remains read-oriented for enterprise BI; BPM owns operational workflow metrics surfaces.
12. **Integration Hub** is transport-only for external triggers / connectors.
13. **Portal modules** (Customer / Vendor) continue to use seeded workflow codes; BPM Designer governs templates/definitions without rewriting portal SoR boundaries.
14. **Dynamic forms are referenced only.** Workflow shall never become the system of record for form definitions. Forms remain owned by the future Low-Code Platform (Sprint 26).

---

## 15. Workflow Lifecycle

```text
Draft Template / Definition
        ↓
Design (Visual Designer · Rules · Decision Tables · SLA · Assignment · Form References)
        ↓
Simulate / Dry Run Validate
        ↓
Validate
        ↓
Publish (versioned)
        ↓
Trigger (Event · Manual · Schedule · API)
        ↓
Instance Running
        ↓
Tasks (User / Approval · Sequential / Parallel · Branch)
        ↓
Reminders · Escalation · Delegation (as applicable)
        ↓
Complete / Reject / Cancel
        ↓
History · Audit · Analytics · Reports
```

Failed path: **Failed → Recover (operator) → Resume / Terminate (policy)** — without rewriting business SoR records.

---

## 16. Notifications

Notification events shall include (non-exhaustive):

- Task assigned / reassigned
- Approval requested / approved / rejected
- Delegation completed
- SLA warning / SLA breached
- Escalation triggered
- Reminder due
- Instance completed / cancelled / failed / recovered
- Definition published / retired

Channels: **email** and **in-app** via Foundation Notification Engine. External channel fan-out may use Integration Hub transport only.

---

## 17. Reports

Workflow operational reports shall include:

- Open instances by module / status
- Task aging and SLA breach
- Escalation volume
- Delegation volume
- Average cycle time / KPI trends
- Failed instance and recovery outcomes
- Publish / version inventory

Process analytics may feed Analytics (read patterns) without BPM becoming enterprise BI SoR.

---

## 18. Audit Requirements

- Audit template / definition create, update, publish, retire.
- Audit all runtime actions: approve, reject, delegate, escalate, reassign, recover, cancel.
- Retain workflow history sufficient for compliance reconstruction.
- Link instances to business entity references (module + entity UUID).
- Integrate with Foundation Audit Engine for enterprise audit continuity.

---

## 19. Security Requirements

- RBAC for design, publish, operate, recover, and audit roles.
- Tenant (and company where applicable) isolation on workflow design and runtime artifacts.
- Segregation of duties: designer vs publisher vs operator vs auditor (policy-enforced).
- No elevation of BPM roles into peer module write authority.
- Secure trigger surfaces (API / scheduled / event) under Foundation Security.
- Preserve Architecture Lock security posture.

---

## 20. Integration Requirements

| Module | Integration Pattern |
|--------|---------------------|
| Foundation | Workflow Engine (C-04) · Notification · Audit · RBAC / Security — **mandatory platform backbone** |
| Security | Authentication, authorization, role resolution for assignment |
| Organization | Company / branch / department context for routing (C-01 org masters) |
| Finance | Document approval orchestration; journals only via PostingService if ever required |
| Sales | Order / quotation approval orchestration (Sales remains SoR) |
| Procurement | RFQ / PO / invoice approval orchestration (Procurement remains SoR) |
| Inventory | Receipt / transfer approval orchestration (Inventory remains SoR) |
| Manufacturing | Production / release approval orchestration |
| CRM | Opportunity / quote approval orchestration |
| HR | Leave / attendance / action approval orchestration |
| Payroll | Payroll run approval orchestration |
| Recruitment | Offer / requisition approval orchestration |
| Projects | Change request / timesheet approval orchestration |
| Assets | Disposal / transfer approval orchestration |
| Service | Service request / work-order approval orchestration |
| Helpdesk | Ticket escalation / approval orchestration |
| Document | Document approval / checkout orchestration (Document remains SoR) |
| GRC | Policy / exception / audit-action orchestration |
| Analytics | Read-oriented process KPI / metrics consumption |
| Integration Hub | External / API / event transport for triggers and connectors only |
| Customer Portal | Portal `PT_*` workflows governed via enterprise engine; portal remains envelope SoR boundary |
| Vendor Portal | Portal `VP_*` workflows governed via enterprise engine; portal remains envelope SoR boundary |
| Low-Code Platform (Sprint 26) | Dynamic Forms Runtime — form definitions owned by Low-Code; Workflow references / orchestrates only |
| Future modules | Must consume Workflow Engine via service contracts; no local approval bypass |

---

## 21. Non Functional Requirements

| Area | Requirement |
|------|-------------|
| Architecture | Clean Architecture · DDD · Modular Monolith · Architecture Lock v1.1 |
| Consistency | Single engine semantics across modules (C-04 / DG-03) |
| Scalability | Support high volume of concurrent instances and tasks |
| Reliability | Durable instance state; recoverable failures |
| Observability | History, audit, KPI, monitoring, simulation |
| Usability | Visual designer usable by non-developers |
| Extensibility | New modules onboard via contracts without redesigning BPM core |
| Compliance | Tenant isolation; immutable published versions; full action audit |

---

## 22. Acceptance Criteria

1. FRD documents design, execution, monitoring, and governance capabilities listed in §7.
2. FRD affirms business modules remain SoR; workflow orchestrates only.
3. FRD affirms C-04 / DG-03 — no approval bypass.
4. FRD affirms C-01 — no duplicate masters.
5. FRD affirms Foundation Workflow / Notification / Audit alignment — no competing engines.
6. FRD covers templates, Template Library, definitions, visual designer, versioning, publishing.
7. FRD covers instances, tasks, sequential/parallel approvals, branching, rules, decision tables, variables, forms mapping.
8. FRD covers Dynamic Forms Runtime Integration by reference only; Low-Code Platform owns forms.
9. FRD covers assignment, delegation, escalation, SLA, timers, reminders.
10. FRD covers event / manual / scheduled / API triggers.
11. FRD covers email / in-app notifications, history, audit, monitoring, KPI, analytics, recovery, simulation, dry-run validation, reports.
12. FRD lists integrations for Foundation through Vendor Portal, Low-Code Platform, and future modules.
13. Architecture Lock v1.1 preserved; no redesign of prior FRDs / ERDs.
14. No ERD / schema / API / code / migrations included in this FRD.

---

## 23. Assumptions

1. Foundation Workflow Engine (FRD-01 / ERD_01) remains the architectural backbone for approvals.
2. Existing seeded module workflows (e.g. `PT_*`, `VP_*`, and prior domain `*_` workflow codes) continue to operate and will be governable under BPM Designer without rewriting business SoR.
3. Business modules already (or will) start workflow instances via Foundation service patterns.
4. Organization and Security provide the identity and org context for assignment.
5. Dynamic form definitions will be provided by the future Low-Code Platform (Sprint 26); Workflow stores references only.
6. Sprint 25 implementation follows after architect review and ERD_25 design lock.

---

## 24. Constraints

1. Architecture Lock v1.1 immutable.
2. No redesign of FRD-01 through FRD-24 or ERD-01 through ERD-24.
3. No parallel approval engine outside C-04 / DG-03.
4. No peer ORM writes; service / event / UUID integration only.
5. C-01 masters only.
6. Business data SoR remains in business modules.
7. Form definitions SoR remains with Low-Code Platform (Sprint 26).
8. This FRD is requirements-only — no schema, API, or implementation prescriptions.

---

## 25. Traceability

| Artifact | Reference |
|----------|-----------|
| BRD | FR-005 Workflow Management; Approval Workflow Architecture |
| Architecture Lock | v1.1 — Workflow Engine (C-04 / DG-03) |
| Foundation | FRD-01 / ERD_01 Workflow Engine |
| Prior release | ERP Core v1.19-beta |
| Consuming domains | FRD-02 … FRD-24 |
| Future forms owner | Low-Code Platform (Sprint 26) |
| Next design | ERD_25 (Sprint 25 — after architect review) |

---

## 26. Future Enhancements

- Richer BPMN import/export interchange
- AI-assisted routing suggestions (advisory only; engine remains deterministic/auditable)
- Enterprise Workflow Simulation
- Impact Analysis
- Dry Run Validation
- Process Optimization
- Deeper external RPA / Integration Hub choreography patterns
- Mobile-optimized task inbox UX

*(Enhancements must not violate Architecture Lock, C-01, or C-04 / DG-03.)*

---

## 27. Phase Gate

| # | Gate Criterion | Status |
|---|----------------|--------|
| 1 | Documents Workflow & BPM Designer purpose and orchestration-only SoR boundary | ✅ |
| 2 | Covers expected capabilities in §7 without implementation artifacts | ✅ |
| 3 | Affirms C-04 / DG-03 single Workflow Engine | ✅ |
| 4 | Affirms C-01 and no peer business SoR takeover | ✅ |
| 5 | Integrates Foundation + all listed ERP modules + future modules | ✅ |
| 6 | Dynamic Forms Runtime Integration by reference; Low-Code owns forms | ✅ |
| 7 | Decision Tables and Simulation / Dry Run Validation documented | ✅ |
| 8 | No redesign of prior FRDs / ERDs | ✅ |
| 9 | Architecture Lock v1.1 preserved | ✅ |
| 10 | Ready for Architect Review ahead of Sprint 25 ERD | ✅ |

**Phase Gate: PASS — Ready for Architect Review**

---

## 28. Document Status

| Field | Value |
|-------|--------|
| **FRD Status** | Locked — Ready for Future Reference |
| **Design** | Pending ERD_25 (after architect review) |
| **Implementation** | Not started (Sprint 25) |
| **Prior Release** | ERP Core v1.19-beta |
| **Architecture Lock** | v1.1 — Unchanged |
| **Next** | Documentation Complete |

---

**FRD-25 Workflow & Business Process Management (BPM) Designer is locked and ready for future reference.**
