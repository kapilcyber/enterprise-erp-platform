# FRD-28 — API Developer Portal Domain

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document ID** | FRD-28 |
| **Document Title** | API Developer Portal Domain |
| **Domain** | API Developer Portal |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Classification** | Internal — Confidential |
| **Aligned To** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · FRD-01 Foundation · FRD-19 Document · FRD-21 Integration Hub · FRD-23 Customer Portal · FRD-24 Vendor Portal · Sprint 28 ARB Recommendation Locked v1.1 · ERP Core v1.22-beta |
| **Sprint** | Sprint 28 (planning) |
| **Predecessor Release** | ERP Core v1.22-beta |
| **Planned Delivery** | ERP Core v1.23-beta (planned) |
| **Next Stage** | ERD-28 Entity Planning |
| **Planned Module (planning)** | `apps/api/src/modules/devportal/` |
| **Planned API Mount** | `/api/v1/devportal` |
| **Schema / Prefix** | TBD under DBS naming standards at ERD-28 (planning hint: `devportal` / `dp_*`) |
| **Business Tables (planning target)** | **~18–20** (ARB range **16–22**; exact count locked at ERD-28) |

### Cross References

- Platform: FRD-01 Foundation (Authentication · Authorization · RBAC · Audit · Notification · Workflow Engine) · FRD-02 Organization · FRD-03 Master Data
- Mandatory connectivity: FRD-21 Integration Hub (credentials · OAuth clients · usage · rate limits · transport — **unchanged SoR**)
- Document artifacts: FRD-19 Document Management (file SoR; UUID refs only)
- Distinct portals (no merge): FRD-23 Customer Portal · FRD-24 Supplier / Vendor Portal
- Non-SoR peers: FRD-25 Workflow & BPM Designer · FRD-26 Low-Code Platform · FRD-27 Enterprise AI Platform
- Planning baseline: [Sprint 28 Architecture Review Board Recommendation](../08_SPRINT_REPORTS/Sprint_28/Sprint_28_Architecture_Review_Board_Recommendation.md) (Locked v1.1)
- Architecture: Architecture Lock v1.1
- Prior release: ERP Core v1.22-beta

### Related Documents

| Document | Location / Reference |
|----------|----------------------|
| Master-FRD | [Master-FRD.md](./Master-FRD.md) |
| Architecture Lock v1.1 | [ERP_Architecture_Lock_Report_v1.1.md](../05_ARCHITECTURE_LOCK/ERP_Architecture_Lock_Report_v1.1.md) |
| Sprint 28 ARB Recommendation | [Sprint_28_Architecture_Review_Board_Recommendation.md](../08_SPRINT_REPORTS/Sprint_28/Sprint_28_Architecture_Review_Board_Recommendation.md) |
| FRD-21 Integration Hub | [FRD-21-Integration-Hub-Enterprise-Platform-Services.md](./FRD-21-Integration-Hub-Enterprise-Platform-Services.md) |
| FRD-23 Customer Portal | [FRD-23-Customer-Portal-Domain.md](./FRD-23-Customer-Portal-Domain.md) |
| FRD-24 Vendor Portal | [FRD-24-Supplier-Vendor-Portal-Domain.md](./FRD-24-Supplier-Vendor-Portal-Domain.md) |

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-28 | Reconstruct and lock FRD-28 API Developer Portal from Sprint 28 Architecture Review Board Recommendation Locked v1.1 (repository document restore). Establishes Developer Portal as DX / catalog / entitlement / documentation-sandbox metadata layer. No redesign of prior modules. Integration Hub and Foundation ownership unchanged. No ERD, tables, SQL, migrations, APIs, or implementation. Architecture Lock v1.1 preserved. |
| 1.1 | 2026-07-28 | Editorial Lock after Permanent Enterprise Architecture Review Board unanimous approval. Added Enterprise Developer Experience Principles, Enterprise Developer Journey, Developer Portal Lifecycle, and documentation-level Future Considerations roadmap items. Metadata Version 1.1. No functional, ownership, scope, FR, NFR, risk, phase, or architecture changes. Ready for ERD-28 Entity Planning. |

---

## 2. Purpose

Provide an **enterprise API Developer Portal** that enables authenticated **developers and partner integrators** to discover published API products, register applications, manage subscription/entitlement metadata, access documentation and sandbox registration metadata, and obtain operational DX visibility — **without becoming** the System of Record for Integration Hub connectivity, Foundation identity, business transactional data, Customer Portal, Vendor Portal, Low-Code, BPM, or AI Platform.

This domain becomes the **developer experience (DX) / API product catalog / entitlement metadata authority**. It **does not** become a second Integration Hub, a full API Gateway product, a second IAM, a business SoR, or a peer-module database writer.

---

## 3. Vision

Establish the API Developer Portal as the **developer self-service and API product catalog layer** for the Enterprise ERP Platform:

```text
Business Modules
        ↓
Integration Hub
        ↓
API Products
        ↓
Developer Portal
        ↓
Developer Applications
        ↓
Subscriptions
        ↓
API Consumers
```

- One governed path for **API product catalog** metadata (what is published for external consumption)
- One governed path for **developer identity & organization** metadata (portal-style; Foundation remains Auth SoR)
- One governed path for **application registration** metadata bound to Integration Hub credentials/OAuth via UUID
- One governed path for **subscription / plan / entitlement** metadata
- One governed path for **documentation catalog** and **sandbox/environment** metadata
- One governed path for **portal operational reports** (usage projected from Integration Hub)

Business modules remain **Systems of Record**. Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow authority. Integration Hub remains connectivity / credential / usage / rate-limit metadata SoR. Document Management remains file SoR. Customer Portal and Vendor Portal remain distinct audience portals. AI Platform remains intelligence metadata SoR.

API Developer Portal **consumes** those domains through **service contracts and UUID references only**.

### Enterprise API Platform Design Principles

| Principle | Statement |
|-----------|-----------|
| **API First** | Platform capabilities are exposed and governed as APIs before portal UX convenience. |
| **Contract First** | Cross-module integration uses published service contracts and OpenAPI contracts — never peer ORM. |
| **Metadata First** | Developer Portal delivers catalog, entitlement, and DX metadata before live gateway/runtime product depth. |
| **Documentation First** | Published API documentation and artifact references are first-class portal concerns. |
| **Security by Default** | AuthN/AuthZ, RBAC, secret refs, and audit paths apply before developer enablement. |
| **Zero Duplicate Ownership** | Portal must not duplicate Foundation, Integration Hub, Customer/Vendor Portal, or AI SoR. |
| **UUID-only Integration** | Peer references are UUID-only; no peer-schema foreign keys. |
| **Service-first Communication** | Reads/writes to peer domains occur only through Application Services / contracts. |
| **Backward Compatibility** | Published API product and documentation versions must support controlled compatibility. |
| **Version-first Design** | API products, OpenAPI artifacts, subscriptions, and docs are version-aware by design. |
| **Developer Experience First** | Portal scope optimizes developer self-service without becoming business SoR or transport SoR. |

### API Capability Classification

| Classification | Capabilities |
|----------------|--------------|
| **Core** | Developer identity & access metadata · Application registration metadata (Hub UUID bindings) · API product catalog (products · versions · environment bindings) · Subscription / plan / entitlement metadata · RBAC namespace + Foundation workflows for account/app/subscription approval |
| **Extension** | Documentation catalog (guides · changelog · OpenAPI artifact references) · Sandbox / environment registration metadata · Portal operational reports (usage projected from Integration Hub) · Try-it session metadata (non-gateway) |
| **Future** | Production frontend product · GraphQL / gRPC developer surfaces (SDD future) · Full API Gateway product (Kong/Envoy — deferred per ERD-21) · Customer Portal / Vendor Portal merge (explicitly forbidden) |

---

## Enterprise Developer Experience Principles

Documentation principles only. No new functionality.

| Principle | Statement |
|-----------|-----------|
| **Developer First** | Portal capabilities optimize the developer and partner integrator experience without becoming business SoR. |
| **API First** | Platform capabilities are exposed and governed as APIs before portal UX convenience. |
| **Contract First** | Cross-module integration uses published service contracts and OpenAPI contracts — never peer ORM. |
| **Discoverability First** | API products, documentation, and sandbox metadata must be discoverable through the portal catalog. |
| **Self-Service First** | Developers can register applications, request subscriptions, and access docs within governed RBAC and workflow gates. |
| **Security by Default** | AuthN/AuthZ, RBAC, secret refs, and audit paths apply before developer enablement. |
| **Zero Duplicate Ownership** | Portal must not duplicate Foundation, Integration Hub, Customer/Vendor Portal, or AI SoR. |
| **UUID-only Integration** | Peer references are UUID-only; no peer-schema foreign keys. |
| **Version-first Design** | API products, OpenAPI artifacts, subscriptions, and docs are version-aware by design. |
| **Backward Compatibility** | Published API product and documentation versions must support controlled compatibility. |

---

## 4. Business Objectives

1. Enable secure developer and partner self-service for account, organization/team, and session metadata management.
2. Provide an enterprise **API product catalog** describing which platform APIs are published for external consumption.
3. Support **application registration** metadata bound to Integration Hub OAuth clients / API credentials by UUID — never duplicate secret storage.
4. Govern **subscription / plan / entitlement** metadata controlling which apps may call which products/scopes.
5. Provide a **documentation catalog** with guides, changelog entries, and OpenAPI artifact **references** (DMS UUID or published snapshot refs).
6. Support **sandbox / environment registration** metadata for non-production pointers.
7. Provide **portal operational reports** with usage **projected from** Integration Hub via services.
8. Enforce Foundation RBAC (`devportal.*`) and Foundation workflows for account / application / subscription approvals.
9. Preserve Architecture Lock v1.1: Clean Architecture, DDD, Modular Monolith, C-01–C-06, no peer ORM writes.
10. Elaborate BRD Stage 6 / API Requirements / Developers stakeholder without inventing a conflicting product or redesigning completed modules.

---

## Enterprise Developer Journey

ASCII only. Reflects existing business processes — no workflow redesign.

```text
Developer
        ↓
Portal Account
        ↓
Application Registration
        ↓
API Product Discovery
        ↓
Subscription
        ↓
Approval
        ↓
Sandbox
        ↓
Production Consumption
```

---

## 5. Scope

Sprint 28 API Developer Portal functional requirements for:

- Developer identity and access metadata (accounts, orgs/teams, invites, sessions)
- Application registration metadata with Integration Hub UUID bindings
- API product catalog (products, versions, environment bindings)
- Subscription / plan / entitlement metadata
- Documentation catalog (guides, changelog, OpenAPI artifact references)
- Sandbox / environment registration metadata
- Try-it session metadata (non-gateway; Extension)
- Portal operational reports (DX metrics; Hub usage projections)
- Security, versioning, publishing, audit, notifications, workflows
- Acceptance and ownership boundaries for all existing ERP domains

**Correct architectural role (locked by ARB):**

> API Developer Portal = developer self-service + API product catalog + subscription/entitlement metadata + documentation/sandbox experience metadata, integrating with Integration Hub, Foundation, and DMS **through contracts only**.

---

## 6. Out of Scope

- Redesign of Architecture Lock v1.1 or any locked FRD/ERD (FRD-01 … FRD-27 / ERD-01 … ERD-27)
- Second Integration Hub / second credential vault
- Full API Gateway product (Kong / Envoy) — remains deferred per ERD-21
- Owning business APIs or business transactional data
- Replacing `/docs` / `/openapi.json` platform OpenAPI generation (FastAPI remains generator per SDD)
- Duplicate Integration Hub ownership of credentials, OAuth clients, connectors, webhooks, events, queues, API usage metering, or rate-limit enforcement metadata
- Duplicate Foundation ownership of AuthN / AuthZ / users / RBAC / JWT / Audit / Notification / Workflow Engine
- Customer Portal / Vendor Portal merge or shared SoR
- AI gateway / AI rate-limit ownership (FRD-27)
- Peer ORM writes or cross-module database access — **C-02**
- Duplicate masters — **C-01**
- Production frontend product (may defer UI like Sprint 26/27 unless separately authorized)
- GraphQL / gRPC developer surfaces (SDD future)
- Schema, SQL, ERD Mermaid, migrations, routes, models, repositories, services, or implementation prescriptions in this FRD

---

## 7. Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| External / partner developers | Self-service discovery, registration, docs, sandbox metadata |
| Internal platform API owners | Publish API products and documentation without losing Hub/Foundation SoR |
| API Product Managers | Catalog, plans, entitlements, version compatibility |
| Integration Hub owners | Preserve credential / usage / rate-limit SoR |
| Foundation / Security | AuthN/AuthZ, RBAC, audit, secret hygiene |
| Customer / Vendor Portal owners | Ensure audience and SoR remain distinct |
| Enterprise Architects | Architecture Lock compliance; zero duplicate ownership |
| QA / Validation | Acceptance against FRD gates prior to ERD/implementation |
| Analytics | Optional read-only DX metrics consumption |

---

## 8. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-28-001 | System shall provide an API Developer Portal for developer self-service, API product catalog, subscription/entitlement metadata, and documentation/sandbox experience metadata. |
| FR-28-002 | System shall be the **System of Record for Developer Portal DX metadata only** (developer org/account/session metadata, application registration metadata, API product catalog metadata, subscription/entitlement metadata, documentation catalog metadata, sandbox/environment metadata, portal reports). |
| FR-28-003 | System shall never become the System of Record for business documents, masters, Integration Hub connectivity artifacts, Foundation identity, Customer Portal, Vendor Portal, Low-Code, BPM, or AI intelligence metadata. |
| FR-28-004 | System shall manage developer account lifecycle (draft → submit → approve → active / lock / suspend / retire) under Foundation workflow. |
| FR-28-005 | System shall manage developer organization / team metadata and invites without replacing Foundation users as Auth SoR. |
| FR-28-006 | System shall manage portal sessions with active / expired / revoked lifecycle (Foundation remains Auth SoR). |
| FR-28-007 | System shall manage application registration metadata with **UUID references** to Integration Hub `int_oauth_client` and/or `int_api_credential` (create-via-contract permitted; secret storage never duplicated). |
| FR-28-008 | System shall provide an API product catalog with products, versions, and environment bindings. |
| FR-28-009 | System shall support draft / published / retired lifecycle for API product versions where versioning applies. |
| FR-28-010 | System shall ensure published API product versions are not silently replaced (version-first / backward-compatibility principles). |
| FR-28-011 | System shall manage subscription / plan / entitlement metadata binding applications to API product versions / scopes. |
| FR-28-012 | System shall provide a documentation catalog for guides, changelog entries, and OpenAPI artifact **references** (DMS UUID or published snapshot refs). |
| FR-28-013 | System shall **not** own FastAPI OpenAPI generation; portal catalogs/publishes references only. |
| FR-28-014 | System shall manage sandbox / environment registration metadata (non-production pointers). |
| FR-28-015 | System shall support try-it session metadata as non-gateway Extension capability. |
| FR-28-016 | System shall produce portal operational reports with read/export permissions; usage metrics projected from Integration Hub via services. |
| FR-28-017 | System shall enforce Foundation Authentication and RBAC namespace **`devportal.*`** for all portal design-time and self-service actions. |
| FR-28-018 | System shall use Foundation Workflow for account / application / subscription approvals (C-04). |
| FR-28-019 | System shall emit significant portal mutations to Foundation Audit (C-06); portal does not own the audit warehouse. |
| FR-28-020 | System shall use Foundation Notification for portal operational notifications (C-05); portal does not own delivery. |
| FR-28-021 | System shall consume Document Management by UUID for documentation artifacts; Document remains file SoR. |
| FR-28-022 | System shall integrate with Integration Hub by UUID/contracts only for credentials, OAuth clients, usage, and rate-limit metadata — **no peer ORM**. |
| FR-28-023 | System shall never write peer ORM models; all peer mutations occur only via owning module services. |
| FR-28-024 | System shall enforce tenant isolation on all Developer Portal artifacts. |
| FR-28-025 | System shall keep Customer Portal and Vendor Portal ownership and audiences distinct — no merge. |
| FR-28-026 | System shall not own AI gateway or AI rate-limit policies (FRD-27). |
| FR-28-027 | System shall not implement a full API Gateway product (Kong/Envoy); entitlement metadata only. |
| FR-28-028 | System shall support Analytics read-only consumption of portal DX metrics where required; Analytics remains reporting SoR. |

---

## 9. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-28-001 | Multi-tenant isolation on all Developer Portal artifacts, sessions, subscriptions, and reports. |
| NFR-28-002 | Company / branch scoping where enterprise tenancy patterns require it. |
| NFR-28-003 | Soft-delete / retire patterns for mutable portal metadata; preserve audit-relevant history. |
| NFR-28-004 | Optimistic concurrency / version stamps on editable drafts. |
| NFR-28-005 | Availability and recoverability aligned with platform ERP SLAs for portal control-plane services. |
| NFR-28-006 | Observability: structured logs/metrics for catalog publishes, subscription changes, and Hub projection failures. |
| NFR-28-007 | Scalability: stateless request handling where feasible; async jobs for report/projection refresh where needed. |
| NFR-28-008 | Security: least privilege; secrets never stored in portal tables; Hub/vault remain secret SoR. |
| NFR-28-009 | Privacy: developer PII minimization and retention controls for portal accounts/sessions. |
| NFR-28-010 | Resilience: Hub projection/report failures must fail safely without inventing usage numbers. |
| NFR-28-011 | Compliance: significant portal actions auditable via Foundation Audit. |
| NFR-28-012 | Performance: interactive catalog/browse/self-service latency suitable for enterprise DX under normal load. |
| NFR-28-013 | Clean Architecture: Router → Service → Repository → Database; domain independent of transport. |
| NFR-28-014 | DDD: bounded context for Developer Portal; aggregates aligned at ERD-28. |
| NFR-28-015 | Modular Monolith: new `modules/devportal` package; no service-boundary redesign. |

---

## 10. User Roles

| Role | Responsibilities |
|------|------------------|
| **Developer Portal Admin** | Full `devportal.*` including approve / lock / revoke; catalog governance |
| **API Product Manager** | API product / version / plan / entitlement governance; mid-level approvals |
| **Developer** | Self-service applications, subscriptions, docs, sandbox metadata (no approve / lock) |
| **Partner Developer** | External integrator subset under tenant/partner policy |
| **API Auditor** | Read-only access to portal audit-relevant trails, publish/subscription history, reports |
| **Security / Compliance Officer** | Oversight of secret-ref hygiene, RBAC, and access grants |

Roles are realized through Foundation RBAC permission codes; Developer Portal does not invent a parallel identity store.

Namespace (planned): **`devportal.*`** (final seed naming aligned to Foundation RBAC conventions at ERD/implementation time — this FRD does not prescribe schema).

---

## 11. Business Processes

### 11.1 Developer account onboarding
Draft account → submit → Foundation workflow approval → activate → optional lock/suspend → retire.

### 11.2 Organization / team management
Developer org/team metadata and invites managed in portal; Foundation users remain Auth SoR.

### 11.3 Application registration
Register application metadata → bind Integration Hub OAuth/credential UUID via contract → submit/approve as required → active/retire.

### 11.4 API product publish
Draft API product / version → review → publish (immutable published version) → bind environments → retire when obsolete.

### 11.5 Subscription & entitlement
Select plan/product version → submit subscription → approve → active entitlement scopes → suspend/retire.

### 11.6 Documentation & sandbox
Publish documentation catalog entries and OpenAPI artifact references; register sandbox/environment metadata; optional try-it session metadata (non-gateway).

### 11.7 Operational reporting
Portal reports refresh DX metrics; usage projected from Integration Hub services; export under RBAC.

---

## 12. Business Rules

1. **Developer Portal is DX / catalog / entitlement metadata SoR only.**
2. **Business SoR remains in modules** — portal never writes peer business tables.
3. **Integration Hub remains connectivity SoR** — credentials, OAuth clients, usage, rate limits, connectors, webhooks, transport.
4. **Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow SoR.**
5. **C-01** — no duplicate masters.
6. **C-02** — no cross-module database access; no peer ORM writes.
7. **C-03** — external connectivity patterns align with Integration Hub.
8. **C-04 / DG-03** — approvals remain Workflow Engine / BPM / Foundation; portal metadata approvals are not business document approvals.
9. **C-05** — notifications via Foundation Notification.
10. **C-06** — enterprise audit via Foundation Audit.
11. **Published API product versions are not silently replaced.**
12. **Secrets never belong in portal tables** — UUID refs / vault keys only.
13. **FastAPI remains OpenAPI generator** — portal catalogs references only.
14. **Customer Portal and Vendor Portal remain distinct** — no merge.
15. **Full API Gateway product remains out of scope** (ERD-21 deferral preserved).
16. **Architecture Lock v1.1 is immutable** for this FRD.
17. **Entity inventory exact count is locked at ERD-28** within ARB target ~18–20 (range 16–22).

---

## 13. Ownership Boundaries

| Concern | Owner |
|---------|--------|
| Developer org · apps · API products · subscriptions · portal UX metadata · doc catalog · sandbox registration | **API Developer Portal (this FRD)** |
| API credential & OAuth client secrets/config · connectors · webhooks · events · queues · API usage metering · rate-limit enforcement metadata · transport | **Integration Hub** |
| Identity · JWT · RBAC · users · Audit warehouse · Notification delivery · Workflow Engine | **Foundation** |
| Workflow design / BPM runtime orchestration | **BPM** (+ Foundation Workflow) |
| Customer self-service | **Customer Portal** |
| Supplier self-service | **Vendor Portal** |
| Form/page design metadata | **Low-Code** |
| Intelligence metadata | **AI Platform** |
| Document file storage | **Document Management** |
| Enterprise BI / reporting | **Analytics** (optional read-only DX metrics) |
| Business transactions / masters | **Business modules / Master Data** |

**Forbidden ownership transfers:** none of the completed modules may be redesigned or stripped of SoR to “fit” the portal.

### Critical Distinction

| Existing capability | Owner today | Developer Portal must **not** become |
|---------------------|-------------|--------------------------------------|
| OpenAPI / Swagger generation | FastAPI platform (`/docs`, `/openapi.json`) per SDD | Owner of OpenAPI generation |
| API credentials · OAuth clients · API usage · rate limits · connectors · webhooks | Integration Hub | Duplicate credential/usage/rate-limit SoR |
| Full API Gateway (Kong/Envoy-class) | Deferred (ERD-21) | Gateway product replacement |
| AuthN / AuthZ / users / RBAC / JWT | Foundation | Second IAM |
| Customer self-service | Customer Portal | Customer UX |
| Supplier self-service | Vendor Portal | Supplier UX |
| AI rate limits / AI gateway policies | AI Platform | AI traffic governance |

---

## 14. Integration Contracts

| System | Integration Pattern |
|--------|---------------------|
| Foundation Security / RBAC | Authentication, authorization, tenant context |
| Foundation Audit | Portal publish / approve / lock / subscription change audit events (C-06) |
| Foundation Notification | Portal operational notifications (C-05); portal does not own delivery |
| Foundation Workflow / BPM | Account / application / subscription approvals (C-04) |
| Integration Hub | UUID refs to credentials / OAuth clients; usage / rate-limit projections via services (C-03); **no peer ORM** |
| Document Management | Documentation artifact UUID; Document remains file SoR |
| Organization | Organizational scope without duplicating org masters |
| Analytics | Optional read-only DX metrics consumption |
| Business modules (Finance … AI) | Consume published API contracts / OpenAPI paths only — never own their data |
| Customer Portal / Vendor Portal | None as SoR; distinct audiences |
| Low-Code / BPM / AI | None as SoR; optional future UUID hooks only |

**Forbidden:** peer ORM writes; portal-local secret vaults; portal-owned OpenAPI generation; portal-owned API Gateway product; merge with Customer/Vendor Portal.

---

## 15. Security Requirements

| Concern | Requirement |
|---------|-------------|
| Identity | Foundation authentication / session only |
| Authorization | Foundation RBAC `devportal.*` for all portal actions |
| Tenant isolation | Mandatory on artifacts, sessions, subscriptions, reports |
| Secret management | Secrets in Hub/vault only; portal stores refs |
| Least privilege | Developers receive minimum catalog/subscription scope |
| Approval gates | Account / application / subscription changes under workflow where required |
| Cross-module | No peer DB access; C-02 compliant |
| Audit | Significant mutations emit Foundation Audit events |
| Abuse prevention | Portal does not replace Hub rate limits; may surface entitlement metadata only |

---

## 16. Audit Requirements

| Concern | Requirement |
|---------|-------------|
| Audit owner | Foundation Audit (C-06) |
| Audited actions (minimum) | Account approve/lock; application bind/approve; product publish/retire; subscription approve/suspend; documentation publish |
| Portal role | Emit audit events; never become enterprise audit warehouse |
| Retention | Follow Foundation / enterprise retention policy |

---

## 17. Workflow Requirements

| Concern | Requirement |
|---------|-------------|
| Workflow owner | Foundation Workflow Engine (C-04); BPM alignment where required |
| Planned approval classes | Developer account · Application registration · Subscription / entitlement |
| Portal role | Initiate / participate in workflows; does not replace Workflow Engine |
| Example workflow codes (planning names) | `DP_ACCOUNT_APPROVAL` · `DP_APPLICATION_APPROVAL` · `DP_SUBSCRIPTION_APPROVAL` (final codes at ERD/implementation seed time) |

---

## 18. Reporting Requirements

| Concern | Requirement |
|---------|-------------|
| Portal reports | DX operational reports (active developers, applications, subscriptions, catalog publishes, session metrics) |
| Usage metrics | **Projected from Integration Hub** via services — portal is not usage SoR |
| Permissions | `devportal.report:read` / `devportal.report:export` (final codes at seed time) |
| Analytics | May consume portal metrics read-only |

---

## 19. Version Compatibility Policy

| Artifact | Compatibility concern |
|----------|----------------------|
| **API Product Version** | Portal catalog version of a published API product must map to a stable product identity |
| **API Version** | Platform API path version (e.g. `/api/v1`) remains platform-owned; portal binds products to published versions |
| **Documentation Version** | Doc/guide/changelog version must align to the referenced API Product Version |
| **Subscription Version** | Entitlement/subscription metadata must reference a specific API Product Version (or compatible set) |
| **SDK Version** | Optional future SDK packaging version must track OpenAPI / API Product Version (not owned in Sprint 28 implementation) |
| **OpenAPI Version** | OpenAPI artifact reference / snapshot version; FastAPI remains generator — portal catalogs references only |

- Published versions are never silently replaced.
- Version upgrades must be explicit and auditable.
- Existing subscriptions continue on their resolved product versions unless explicitly migrated under policy.

---

## 20. Implementation Phases (Approved — Unchanged)

Per Sprint 28 ARB Recommendation Locked v1.1 — **do not change**:

| Phase | Focus | Intent |
|-------|--------|--------|
| **Phase 0** | Schema shell · module scaffold · Alembic bootstrap | Foundation only |
| **Phase 1** | Developer identity · org/team · application registration · API product/version catalog | Core DX spine |
| **Phase 2** | Plans · subscriptions · entitlements · Hub credential/OAuth **UUID bindings** | Access governance metadata |
| **Phase 3** | Documentation catalog · environments/sandbox metadata · try-it session metadata (non-gateway) | DX content & sandbox |
| **Phase 4** | Usage/report projections · hardening · permissions seed · validation gate | Operational close |

Then: Validation → Validation Fix (if needed) → Release Notes (v1.23-beta) · Completion Report — same governance path as Sprint 26/27.

**Entity planning target:** ~18–20 business tables (ARB range 16–22). Exact inventory locked at ERD-28.

---

## Developer Portal Lifecycle

ASCII lifecycle only. Documentation only — no redesign of existing workflows or phases.

```text
Draft
        ↓
Review
        ↓
Approve
        ↓
Publish
        ↓
Consume
        ↓
Retire
```

---

## 21. Risks & Assumptions

### Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-28-01 | Overlap with Integration Hub (credentials, usage, rate limits) | **High** | Hard ownership matrix in this FRD; UUID/contract only |
| R-28-02 | Accidental “API Gateway” scope creep | **Critical** | Keep ERD-21 deferral; portal stores entitlement metadata only |
| R-28-03 | Confusion with Customer/Vendor Portal | **Medium** | Distinct audience (developers/partners building integrations) |
| R-28-04 | Master FRD lag (01–22 only) | **Low** | FRD-28 as locked peer; Master FRD consolidation is doc debt, not a redesign |
| R-28-05 | Treating auto-OpenAPI as portal SoR | **Medium** | Portal catalogs/publishes references; FastAPI remains generator |
| R-28-06 | Secret storage in portal tables | **High** | Secrets remain Hub/vault; portal stores refs only |

### Assumptions

1. Foundation AuthN/AuthZ/RBAC/Audit/Notification/Workflow remain available platform services.
2. Integration Hub remains the connectivity SoR and exposes stable contracts for credential/OAuth UUID and usage projections.
3. Document Management can provide authorized artifact access by UUID for documentation references.
4. Architecture Lock v1.1 remains final and unmodified.
5. Sprint 28 follows the established **metadata-first backend** delivery pattern.
6. Frontend may be deferred unless separately authorized.
7. “API Developer Portal” elaborates BRD Stage 6 / API Requirements / Developers stakeholder — it does not invent a conflicting product.
8. Exact entity inventory is finalized at ERD-28 within the approved ARB range.

---

## 22. Future Considerations

- Production frontend / DX UI product over existing APIs (separately authorized)
- GraphQL / gRPC developer surfaces (SDD future)
- Full API Gateway product (Kong/Envoy) — remains deferred; not a Developer Portal ownership transfer
- Optional SDK packaging versioning aligned to OpenAPI / API Product Version
- Deeper partner marketplace patterns under the same catalog/entitlement model
- Master FRD consolidation to include FRD-23 … FRD-28 (documentation debt only)

### Documentation-Level Roadmap References

Roadmap references only. No implementation.

| Roadmap Item | Notes |
|--------------|-------|
| **Developer Marketplace** | Future catalog of certified partner integrations under the same entitlement model |
| **SDK Registry** | Future registry of SDK packages versioned against OpenAPI / API Product Version |
| **Webhook Catalog** | Future discoverability surface for Hub webhook definitions (Hub remains SoR) |
| **GraphQL Explorer** | Future DX surface if/when GraphQL is authorized (SDD future) |
| **Plugin Marketplace** | Future governed plugin discovery without portal owning plugin execution |
| **Future API Discovery enhancements** | Search, tagging, and cross-product discovery improvements over the locked catalog model |

*(Enhancements must not violate Architecture Lock, C-01–C-06, or ownership boundaries of Foundation, Integration Hub, Customer Portal, Vendor Portal, Document, Analytics, Low-Code, BPM, AI, or business modules.)*

---

## 23. Acceptance Criteria

| # | Criterion |
|---|-----------|
| 1 | FRD defines API Developer Portal as DX / catalog / entitlement / documentation-sandbox metadata SoR without owning business transactional data |
| 2 | FRD affirms Foundation ownership of AuthN/AuthZ/RBAC/Audit/Notification/Workflow Engine |
| 3 | FRD affirms Integration Hub ownership of credentials, OAuth clients, usage, rate limits, connectors, and transport |
| 4 | FRD affirms Customer Portal and Vendor Portal remain distinct; no merge |
| 5 | FRD affirms Document owns files; Analytics owns reporting; AI owns intelligence metadata; Low-Code owns forms/pages; BPM owns workflow design |
| 6 | FRD prohibits peer ORM writes and duplicate masters (C-01 / C-02) |
| 7 | FRD affirms C-03 / C-04 / C-05 / C-06 boundaries |
| 8 | Core / Extension / Future capability classification matches ARB Recommendation |
| 9 | Approved implementation phases match ARB Recommendation without change |
| 10 | Entity planning target ~18–20 (range 16–22) stated; exact inventory deferred to ERD-28 |
| 11 | Risks R-28-01 … R-28-06 preserved with severities |
| 12 | No schema, API, ERD Mermaid, SQL, migrations, or implementation prescriptions included |
| 13 | Architecture Lock v1.1 preserved |
| 14 | Ready for ERD-28 Entity Planning |

---

## 24. Phase Gate

| # | Gate Criterion | Status |
|---|----------------|--------|
| 1 | Documents Developer Portal purpose, vision, and SoR boundary (DX metadata vs Hub/Foundation/business) | ✅ |
| 2 | Covers required functional, NFR, ownership, integration, security, audit, workflow, reporting sections without implementation artifacts | ✅ |
| 3 | Affirms Foundation / Integration Hub / Customer Portal / Vendor Portal / Document / Analytics / AI / Low-Code / BPM ownership splits | ✅ |
| 4 | Affirms C-01–C-06 and no peer ORM writes / UUID-only references / service contracts | ✅ |
| 5 | Design principles, capability classification, version compatibility, phases, risks preserved from ARB | ✅ |
| 6 | No redesign of prior FRDs / Architecture Lock / Sprint 26–27 / ARB Recommendation | ✅ |
| 7 | Ready for ERD-28 Entity Planning | ✅ |

**Phase Gate: PASS — Ready for ERD-28 Entity Planning**

---

### FRD Dependency Summary

| Dependency | Purpose |
|------------|---------|
| Foundation | Identity, RBAC, tenant context, Audit (C-06), Notification delivery (C-05), Workflow Engine (C-04) |
| Organization | Organizational scope without duplicating org masters |
| Integration Hub | Credential/OAuth UUID bindings; usage/rate-limit projections; transport SoR (C-03) |
| Document Management | Documentation artifact UUID; Document remains file SoR |
| Analytics | Optional read-only DX metrics consumption |
| Customer Portal / Vendor Portal | Distinct audiences; no shared SoR |
| Business Modules | Published API contracts only; remain Systems of Record |
| Low-Code / BPM / AI | No SoR transfer; optional future UUID hooks only |

---

### Document Status

| Field | Value |
|-------|--------|
| **Version** | 1.1 |
| **FRD Status** | Locked — Ready for Future Reference |
| **Next Stage** | ERD-28 Entity Planning |
| **Next Artifact** | ERD-28 Entity Planning (not created in this step) |
| **Authoritative Planning Baseline** | Sprint 28 ARB Recommendation Locked v1.1 |

---

## 25. Closing Statement

FRD-28 is now Locked and becomes the baseline for all future ERD, backend implementation, validation, and release activities.

No architectural or ownership changes were introduced.

