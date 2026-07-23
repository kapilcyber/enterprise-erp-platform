# FRD-26 — Low-Code Platform Domain

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document ID** | FRD-26 |
| **Document Title** | Low-Code Platform Domain |
| **Domain** | Low-Code Platform |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Classification** | Internal — Confidential |
| **Aligned To** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · FRD-01 Foundation · FRD-25 Workflow & BPM Designer · ERP Core v1.20-beta |
| **Sprint** | Sprint 26 (planning) |
| **Predecessor Release** | ERP Core v1.20-beta |
| **Planned Delivery** | ERP Core v1.21-beta (planned) |

### Cross References

- Platform: FRD-01 Foundation (RBAC · Notification · Audit · Workflow Engine) · FRD-02 Organization · FRD-03 Master Data
- Design-time consumer: FRD-25 Workflow & BPM Designer (form references only; BPM does not own forms)
- Consuming business domains: FRD-04 … FRD-24 and future modules
- Architecture: Architecture Lock v1.1
- Prior release: ERP Core v1.20-beta

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial FRD-26 Low-Code Platform for Sprint 26 architect review. Establishes enterprise SoR for dynamic forms, page composition, components, expressions, and runtime rendering. No redesign of prior modules. Architect review improvements: Version Compatibility Policy, Form Ownership Lifecycle, Performance Targets, Component Compatibility Policy, FRD Dependency Summary. |
| 1.1 | 2026-07-22 | Editorial Lock after Architecture Review. No functional changes. |

---

## 2. Vision

Provide a **centralized Low-Code Platform** that enables enterprise configuration of **dynamic forms**, **page layouts**, **reusable UI components**, **data bindings**, **expressions**, and **runtime rendering** across the ERP — so business and IT configurators can extend capture screens and guided experiences **without changing application code**, while **business modules remain Systems of Record**.

This domain becomes the **forms and composition authority** consumed by Workflow & BPM Designer, portals, and transactional modules. It **does not** become a second ERP, a competing workflow engine, a master-data store, or a peer-module database writer.

---

## 3. Business Objectives

1. Enable configurable dynamic forms reusable across ERP modules and BPM tasks.
2. Provide a page / screen composition capability for guided enterprise experiences.
3. Offer a governed component library for consistent UX and validation patterns.
4. Bind forms and pages to authoritative module data via contracts (UUID / services), never peer ORM.
5. Support expressions and rules for visibility, validation, defaults, and calculated fields.
6. Emit runtime events that modules and BPM can consume without Low-Code owning business outcomes.
7. Integrate tightly with Workflow & BPM Designer form references (FRD-25) as the forms SoR.
8. Enforce versioning, publishing, and immutability of published definitions for auditability.
9. Deliver a secure multi-tenant runtime with Foundation RBAC, Audit, and Notification alignment.
10. Preserve Architecture Lock v1.1: Clean Architecture, DDD, Modular Monolith, C-01–C-06, DG guardrails.

---

## 4. Scope

Sprint 26 Low-Code Platform functional requirements for:

- Form definition design and catalog
- Page / screen builder (composition of forms and components)
- Component library governance
- Data source bindings to ERP modules (read/write through owning module contracts)
- Expression language for UI logic (not a second business SoR rules engine replacing BPM Decision Tables)
- Client/runtime event model
- Workflow & BPM form-reference fulfillment
- Security, versioning, publishing, runtime render/submit
- Audit, operational reporting, integrations
- Acceptance and ownership boundaries for all existing ERP domains

---

## 5. Out of Scope

- Redesign of Architecture Lock v1.1 or any locked FRD/ERD (FRD-01 … FRD-25)
- Owning business transactional data (PO, invoice, leave, ticket, journal, etc.)
- Duplicate masters (employee, customer, vendor, product, department) — **C-01**
- Competing Workflow / Approval Engine — **C-04 / DG-03** (BPM / Foundation remain approval path)
- Competing Notification SoR — **C-05** (Foundation Notification delivers)
- Competing Audit SoR — **C-06** (Foundation Audit)
- Peer ORM writes or cross-module database access — **C-02**
- Full general-purpose application IDE / code generation replacing ERP modules
- Arbitrary server-side scripting that mutates peer schemas
- BPM decision tables / escalation / SLA redesign (owned by FRD-25)
- End-user mobile native SDKs beyond platform runtime contracts (future enhancement)
- AI-generated forms as unchecked production publish without human governance (future advisory only)
- Schema, API, ERD, or implementation prescriptions in this FRD

---

## 6. Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| Business Process Owners | Configurable capture forms for processes without IT coding cycles |
| Process Designers / BPM Designers | Bind BPM user/approval tasks to published Low-Code forms |
| Module Product Owners (Finance … Portals) | Extend screens while retaining module SoR and validations |
| Enterprise Architects | Architecture Lock compliance; modular boundaries |
| Security / Compliance | RBAC, tenant isolation, audit of publish and runtime submit |
| IT Configurators / Citizen Developers (governed) | Design forms/pages within approved component and data-source catalogs |
| Platform Engineering | Runtime performance, versioning, safe expression evaluation |
| QA / Validation | Acceptance against FRD gates prior to ERD/implementation |
| End Users | Consistent, accessible rendered forms and pages at runtime |

---

## 7. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-LC-001 | System shall provide a Low-Code Platform for designing, versioning, publishing, and rendering dynamic forms and composed pages without application code changes. |
| FR-LC-002 | System shall be the **System of Record for form definitions, page definitions, component catalog entries, and expression definitions** used by the platform. |
| FR-LC-003 | System shall never become the System of Record for business documents or master data; owning modules remain SoR. |
| FR-LC-004 | System shall support a form catalog searchable by module, category, status, and tags. |
| FR-LC-005 | System shall support draft / published / retired lifecycle for form and page definitions. |
| FR-LC-006 | System shall ensure published definitions are immutable for audit and in-flight runtime integrity. |
| FR-LC-007 | System shall support cloning of form and page definitions into new draft versions. |
| FR-LC-008 | System shall support a page builder that composes forms, layout regions, and approved components. |
| FR-LC-009 | System shall provide a governed component library (inputs, selects, grids, sections, attachments, display-only, etc.). |
| FR-LC-010 | System shall support data sources that bind to ERP module contracts by module code and entity type (UUID-oriented). |
| FR-LC-011 | System shall support field-level binding to data source attributes without storing peer business rows in Low-Code tables as SoR. |
| FR-LC-012 | System shall support expressions for visibility, requiredness, enablement, defaults, and calculated values. |
| FR-LC-013 | System shall support client and runtime events (load, change, submit, cancel, custom named events) with governed handlers. |
| FR-LC-014 | System shall fulfill Workflow & BPM Designer form references (UUID/key) for task and definition binding without BPM owning forms. |
| FR-LC-015 | System shall render published forms/pages at runtime for authenticated, authorized users under tenant isolation. |
| FR-LC-016 | System shall submit runtime payloads to the owning business module contract; Low-Code shall not write peer ORM models. |
| FR-LC-017 | System shall enforce Foundation RBAC permissions for design-time and runtime actions. |
| FR-LC-018 | System shall audit design publishes and significant runtime submits via Foundation Audit. |
| FR-LC-019 | System shall support operational reports on form usage, publish status, and runtime errors (Analytics may consume metrics read-only). |
| FR-LC-020 | System shall integrate with Document Management by reference for file/attachment fields (Document remains document SoR). |
| FR-LC-021 | System shall support localization metadata for labels and messages on forms/pages. |
| FR-LC-022 | System shall prevent unsafe expression execution (no unrestricted OS/network/peer-DB access from expressions). |
| FR-LC-023 | System shall support validation rules (field and form level) evaluated at design-time preview and runtime submit. |
| FR-LC-024 | System shall be consumable by all existing and future ERP modules via service contracts only. |
| FR-LC-025 | System shall never replace C-01 masters or invent duplicate party/item directories. |

---

## 8. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-LC-001 | Multi-tenant isolation on all design and runtime artifacts (`tenant` context mandatory). |
| NFR-LC-002 | Company / branch scoping where applicable for enterprise ERP tenancy patterns. |
| NFR-LC-003 | Soft-delete / retire patterns for definitions; no uncontrolled physical purge of published history needed for audit. |
| NFR-LC-004 | Optimistic concurrency / version stamps on editable draft definitions. |
| NFR-LC-005 | Runtime render and submit latency suitable for interactive enterprise use under expected concurrent load. |
| NFR-LC-006 | Expression evaluation must be deterministic, sandboxed, and time/memory bounded. |
| NFR-LC-007 | Availability and recoverability aligned with platform ERP SLAs. |
| NFR-LC-008 | Accessibility-aware runtime rendering baselines (labels, required indicators, keyboard navigation expectations). |
| NFR-LC-009 | Observability: structured logs for publish, render failures, and submit contract failures. |
| NFR-LC-010 | Scalability: definitions reusable across modules; runtime stateless where feasible. |
| NFR-LC-011 | Security: least privilege; no secrets in form definitions; no peer DB credentials in Low-Code config. |
| NFR-LC-012 | Compliance: publish and submit actions auditable for regulated processes. |

### Performance Targets

Enterprise interactive targets (architectural expectations; not implementation prescriptions):

| Target | Expectation |
|--------|-------------|
| Draft preview | Completes within acceptable interactive latency for designer workflows |
| Published form rendering | Target ≤ **2 seconds** under normal enterprise load |
| Publish validation | Target ≤ **10 seconds** for definition validation prior to publish |
| Runtime submit validation | Target ≤ **3 seconds** for Low-Code validation, **excluding** downstream owning-module processing |

Targets guide capacity and UX quality; they do not alter SoR boundaries or Architecture Lock constraints.

---

## 9. User Roles

| Role | Responsibilities |
|------|------------------|
| **Low-Code Admin** | Platform configuration, component catalog governance, global publish policy |
| **Form Designer** | Create/edit draft forms, bind fields, expressions, validate, submit for publish |
| **Page Designer** | Compose pages from forms/components, layout regions, navigation sections |
| **Module Configurator** | Map published forms/pages to module entry points within allowed data sources |
| **BPM Designer** | Select published Low-Code forms for BPM form references (via BPM permissions) |
| **Publisher / Process Owner** | Approve publish / retire of forms and pages |
| **Runtime User** | Fill and submit rendered forms/pages per module or BPM task context |
| **Auditor** | Read-only access to definition history metadata and audit-relevant publish trails |
| **Platform Operator** | Operational monitoring of runtime errors; no silent SoR mutation |

Roles are realized through Foundation RBAC permission codes; Low-Code does not invent a parallel identity store.

---

## 10. Platform Capabilities

| Capability | Description |
|------------|-------------|
| Form Studio | Design dynamic forms: fields, sections, validators, bindings, expressions |
| Page Studio | Compose pages from forms, layout containers, and catalog components |
| Component Catalog | Governed reusable UI building blocks with typed properties |
| Data Source Registry | Registered module-backed sources (contracts), not raw SQL to peer schemas |
| Expression Studio | Author/test UI logic expressions with sandbox constraints |
| Preview | Design-time preview against sample/runtime-safe contexts |
| Publish Governance | Draft → validate → publish → retire; one active published lineage policy per definition identity |
| Runtime Host | Render + collect + submit to owning module / BPM task context |
| Event Bus (logical) | Named UI events for handlers and external module reactions |
| Catalog Search | Discover forms/pages by module, tags, status |
| Localization Pack | Labels/messages metadata |
| Ops Dashboard | Usage and error summaries (operational) |

---

## 11. Dynamic Forms

| Concern | Requirement |
|---------|-------------|
| Definition | Forms are versioned definition artifacts owned by Low-Code |
| Structure | Sections, fields, field types, options sources, help text, placeholders |
| Validation | Required, format, range, cross-field rules |
| Binding | Fields bind to data source attributes or BPM/runtime context variables |
| Reuse | Same published form may be referenced by multiple modules and BPM versions |
| Preview | Designers can preview without publishing |
| Immutability | Published form versions cannot be silently edited |
| Retirement | Retired forms remain resolvable for historical instances; blocked for new bindings by policy |
| BPM | BPM stores form UUID/key only; Low-Code resolves definition at design and runtime |

**SoR statement:** Low-Code owns **form definitions**. Business modules own **submitted business data**.

---

## 12. Page Builder

| Concern | Requirement |
|---------|-------------|
| Purpose | Compose enterprise screens from forms, layout regions, and components |
| Layout | Regions/containers (header, body, sidebar, actions) without hardcoding module UI |
| Embedding | Embed one or more published forms by reference |
| Navigation | Optional multi-step / wizard page flows within Low-Code composition |
| Actions | Submit, save draft (if owning module supports), cancel, custom action events |
| Context | Page receives module + entity context (UUID) from host module or BPM task |
| Permissions | Page design and runtime access controlled by RBAC |
| Non-goals | Page builder shall not redefine ERP navigation IA as a second menu SoR |

---

## 13. Component Library

| Concern | Requirement |
|---------|-------------|
| Catalog | Versioned catalog of approved components |
| Types | Text, number, date/time, boolean, select/multi-select, lookup (module-backed), table/grid (display or limited edit per policy), section, divider, rich text (sanitized), attachment (Document ref), read-only display |
| Properties | Typed props, default values, validation hooks |
| Governance | New components require platform admin approval before designer use |
| Consistency | Components enforce shared UX and accessibility baselines |
| Extensibility | Future component additions must not bypass security sandbox |

### Component Compatibility Policy

- Published forms remain compatible with the component version used during publishing.
- New component versions must not silently break existing published forms.
- Breaking changes require explicit versioning.
- Deprecated components remain resolvable until retirement policy allows removal.

---

## 14. Data Sources

| Concern | Requirement |
|---------|-------------|
| Registry | Named data sources registered per module capability |
| Contract | Each source declares module code, entity type, allowed operations (read / write / lookup) |
| Identity | Business rows referenced by UUID; Low-Code does not duplicate masters |
| Lookup | Lookups resolve through owning module services (e.g., Master Data, Organization) |
| Write path | Writes/submits execute only via owning module APIs/services |
| Forbidden | Direct SQL against peer schemas; peer ORM imports; bypassing module validation |
| Caching | Optional short-lived lookup cache; must not become SoR |
| BPM context | Runtime may merge BPM variables with data source context without Low-Code owning BPM variables SoR |

---

## 15. Expressions & Rules

| Concern | Requirement |
|---------|-------------|
| Purpose | Drive UI behavior: visible / hidden / enabled / required / default / calculate |
| Scope | Field, section, form, and page-level expressions |
| Safety | Sandboxed evaluation; no unrestricted I/O, no peer DB, no OS commands |
| Determinism | Same inputs yield same outputs for auditability |
| Testing | Design-time expression test against sample context |
| Boundary vs BPM | BPM Decision Tables / Business Rules own process routing; Low-Code expressions own UI behavior |
| Boundary vs Module | Module business invariants remain enforced by the owning module on submit |

---

## 16. Event System

| Concern | Requirement |
|---------|-------------|
| Events | `onLoad`, `onChange`, `onValidate`, `onSubmit`, `onCancel`, custom named events |
| Handlers | Governed handler types (expression, module callback contract, emit integration event) |
| BPM | Events may signal task UI completion readiness; approval outcome remains BPM/Foundation |
| Integration | External side effects use Integration Hub patterns where cross-system transport is required |
| Non-goals | Event system is not a replacement for BPM triggers or Foundation Notification Engine |

---

## 17. Workflow Integration

| Concern | Requirement |
|---------|-------------|
| Ownership | Low-Code = form/page SoR; BPM = workflow definition/runtime SoR |
| Reference | BPM `form_reference` (and equivalents) store Low-Code form UUID/key only |
| Publish rule | BPM should bind only to **Published** Low-Code forms (policy) |
| Runtime | BPM user/approval tasks render the referenced published form version |
| Submit | Task submit payload returns to BPM/module contract; Low-Code does not create workflow instances |
| Version pin | In-flight BPM tasks retain the form version resolved at task creation/start per policy |
| No takeover | Low-Code shall not redesign BPM engines, SLA, escalation, or history |

This fulfills FRD-25 requirement that **forms remain owned by Low-Code Platform**.

---

## 18. Security & Permissions

| Concern | Requirement |
|---------|-------------|
| Identity | Foundation authentication / session only |
| RBAC | Design-time and runtime permissions via Foundation Security |
| Tenant isolation | Mandatory on all artifacts and runtime resolutions |
| Field security | Sensitive fields may declare masking / role-restricted visibility metadata |
| Expression safety | Prevent injection and privilege escalation via expressions |
| Secrets | No credentials stored in definitions |
| Least privilege | Runtime users only get forms/pages authorized for their roles and module context |
| Cross-module | No peer DB access; C-02 compliant |

---

## 19. Versioning & Publishing

```text
Draft Form / Page
        ↓
Design (Components · Bindings · Expressions · Events)
        ↓
Preview / Validate
        ↓
Publish (immutable version)
        ↓
Runtime Consume (Modules · BPM · Portals)
        ↓
Retire (block new bindings; preserve historical resolve)
```

| Rule | Statement |
|------|-----------|
| Immutability | Published versions are immutable |
| Lineage | Definitions retain version history |
| Clone | New drafts may clone from published/retired |
| Binding policy | New BPM/module bindings prefer latest published unless pinned |
| In-flight | Active runtime usages continue on resolved version until completed |

### Version Compatibility Policy

- Runtime always resolves the exact published version that was bound at publish/binding time.
- Existing runtime sessions and BPM tasks continue using their resolved version.
- New bindings may use newer published versions according to governance.
- Published versions are never silently replaced.
- Version upgrades must be explicit and auditable.

---

## 20. Runtime

| Concern | Requirement |
|---------|-------------|
| Resolve | Locate published form/page by id/key/version policy |
| Render | Produce render model for web clients (contract-level; no UI framework lock-in in FRD) |
| Context | Accept tenant, user, module, entity UUID, BPM task context |
| Validate | Client + server validation before submit handoff |
| Submit | Handoff payload to owning module or BPM task completion contract |
| Errors | Surface field and form errors without leaking internal stack traces |
| Offline | Not required for Sprint 26 core (future) |
| Idempotency | Submit handoff supports idempotent client retries where module contract allows |

---

## 21. Audit & Logging

| Concern | Requirement |
|---------|-------------|
| Design audit | Create/update/publish/retire of definitions via Foundation Audit |
| Runtime audit | Significant submits and authorization failures auditable |
| Correlation | Correlate Low-Code runtime events with BPM task id / module entity UUID |
| Retention | Align with enterprise audit retention policies |
| Non-duplication | Do not create a competing audit warehouse SoR |

---

## 22. Reporting

| Report Area | Purpose |
|-------------|---------|
| Definition inventory | Forms/pages by module, status, version |
| Publish activity | Who published/retired what and when |
| Runtime usage | Render/submit volumes (operational) |
| Error rates | Validation and contract failure summaries |
| BPM binding coverage | Forms referenced by published BPM versions |

Analytics module may consume metrics **read-only**; Low-Code owns operational report surfaces for platform admins.

---

## 23. Integrations

| System | Integration Pattern |
|--------|---------------------|
| Foundation Security / RBAC | Permissions, tenant context |
| Foundation Audit | Design + runtime audit |
| Foundation Notification | Optional notify-on-publish / assign (C-05); Low-Code does not own delivery |
| Workflow & BPM Designer | Form UUID references; runtime render for tasks |
| Master Data / Organization | Lookup data sources via services (C-01) |
| Business modules (Finance … Portals) | Host pages/forms; SoR for business data |
| Document Management | Attachment fields by document UUID |
| Integration Hub | External connector transport only (C-03) |
| Analytics | Read-oriented metrics consumption |

**Forbidden:** peer ORM writes; bypassing module validation; bypassing C-04 approvals by “form-only” pseudo-approvals.

---

## 24. Business Rules

1. **Forms SoR is Low-Code** — BPM and modules reference; they do not own form definitions.
2. **Business SoR remains in modules** — submit never writes peer tables from Low-Code.
3. **C-01** — no duplicate masters; lookups use Master Data / Organization.
4. **C-02** — no cross-module database access.
5. **C-03** — external systems via Integration Hub.
6. **C-04 / DG-03** — approvals remain Workflow Engine / BPM; forms do not replace approvals.
7. **C-05** — notifications via Foundation Notification.
8. **C-06** — audits via Foundation Audit.
9. **Published immutability** for audit and in-flight integrity.
10. **Expressions are UI logic** — not a second enterprise decision engine replacing BPM decision tables.
11. **Component catalog is governed** — unapproved components cannot be used in publishable definitions.
12. **Tenant isolation is mandatory**.
13. **Architecture Lock v1.1 is immutable** for this FRD.

---

## 25. Acceptance Criteria

| # | Criterion |
|---|-----------|
| 1 | FRD defines Low-Code as forms/pages/components SoR without owning business transactional data |
| 2 | FRD affirms BPM form-reference integration without BPM owning forms |
| 3 | FRD prohibits peer ORM writes and duplicate masters (C-01 / C-02) |
| 4 | FRD affirms C-04 / C-05 / C-06 boundaries |
| 5 | Versioning / publishing / immutability rules are explicit |
| 6 | Dynamic Forms, Page Builder, Component Library, Data Sources, Expressions, Events, Runtime are covered |
| 7 | Security, Audit, Reporting, Integrations are covered |
| 8 | No schema, API, ERD, or implementation prescriptions included |
| 9 | Ready for Architect Review ahead of ERD-26 |
| 10 | Architecture Lock v1.1 preserved |

---

## 26. Cross Module Ownership

| Area | Owner |
|------|--------|
| Form / page / component / expression definitions | **Low-Code Platform (this FRD)** |
| Business documents and ledgers | Owning business module |
| Masters (party/item/org) | Master Data / Organization (C-01) |
| Workflow design & runtime | Workflow & BPM Designer + Foundation Workflow Engine |
| Form references on BPM versions | BPM stores UUID/key; Low-Code resolves |
| Notifications | Foundation Notification |
| Audit | Foundation Audit |
| Documents/files | Document Management |
| External transport | Integration Hub |
| Enterprise BI | Analytics (read-only consumption) |

### Form Ownership Lifecycle

- Business modules own business processes.
- Low-Code owns form/page definitions.
- Business owners approve publish.
- Publishers publish.
- Runtime users consume only published artifacts.
- Retired definitions remain available for historical resolution.

---

## 27. Architecture Compliance

| Principle | Compliance Statement |
|-----------|----------------------|
| Architecture Lock v1.1 | Preserved; no lock changes |
| Modular Monolith | New Low-Code module package; no service mesh redesign |
| Clean Architecture / DDD | Required at implementation time (out of FRD detail scope) |
| C-01 | No duplicate masters |
| C-02 | No peer DB access |
| C-03 | External via Integration Hub |
| C-04 / DG-03 | No parallel approval engine |
| C-05 | No parallel notification SoR |
| C-06 | No parallel audit SoR |
| BPM boundary | Complements FRD-25; does not redesign BPM |
| Prior modules | No redesign of completed modules |

---

## 28. Future Expansion

- Visual theme tokens / design-system packaging
- Deeper portal-specific page shells (Customer / Vendor) without portal SoR takeover
- Mobile-optimized runtime packs
- Advisory AI form drafting with mandatory human publish approval
- Broader marketplace of certified component packs
- Enhanced offline / draft sync (policy-controlled)

*(Enhancements must not violate Architecture Lock, C-01–C-06, or BPM ownership boundaries.)*

---

## 29. Phase Gate

| # | Gate Criterion | Status |
|---|----------------|--------|
| 1 | Documents Low-Code purpose and SoR boundary (forms vs business data) | ✅ |
| 2 | Covers required capability sections without implementation artifacts | ✅ |
| 3 | Affirms BPM form-reference ownership split (FRD-25 alignment) | ✅ |
| 4 | Affirms C-01–C-06 and no peer ORM writes | ✅ |
| 5 | Versioning / publishing / runtime / security / audit covered | ✅ |
| 6 | No redesign of prior FRDs / Architecture Lock | ✅ |
| 7 | Ready for Architect Review ahead of Sprint 26 ERD | ✅ |

**Phase Gate: PASS — Ready for Architect Review**

---

## FRD Dependency Summary

| Dependency | Purpose |
|------------|---------|
| Foundation | Identity, RBAC, tenant context, Audit (C-06), Notification delivery (C-05), Workflow Engine alignment (C-04) |
| Organization | Organizational scope and department/context lookups without duplicating org masters |
| Master Data | Party/item lookup data sources under C-01 single-source-of-truth |
| Workflow & BPM Designer | Consumes Low-Code form UUID/key references for task/form binding; BPM remains workflow SoR |
| Document Management | Attachment fields reference documents by UUID; Document remains document SoR |
| Integration Hub | External connector transport only (C-03); no peer DB shortcuts |
| Analytics | Read-only consumption of Low-Code operational metrics |
| Business Modules | Host forms/pages and remain Systems of Record for submitted business data |

---

## Document Status

| Field | Value |
|-------|--------|
| **FRD Status** | Locked — Ready for Future Reference |
| **Next** | Documentation Complete |

---

## 30. Closing Statement

FRD-26 Low-Code Platform Domain is locked and ready for future reference.
