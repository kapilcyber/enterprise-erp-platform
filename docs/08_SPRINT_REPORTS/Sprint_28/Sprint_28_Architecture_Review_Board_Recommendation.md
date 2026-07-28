# Architecture Review Board — Sprint 28 Recommendation

## Permanent Enterprise Architecture Review Board

This review is conducted by the **Permanent Enterprise Architecture Review Board**.

| Rule | Statement |
|------|-----------|
| **Permanence** | This review board is **permanent for Sprint 28 onward**. |
| **Experience** | Every member has **20+ years** of enterprise architecture experience. |
| **Gate** | **Implementation cannot begin** without **unanimous approval** of this board. |

### Permanent Board Composition (20+ years each)

| # | Role |
|---|------|
| 1 | Enterprise Solution Architect |
| 2 | Chief Enterprise Architect |
| 3 | ERP Product Architect |
| 4 | Principal Software Engineer |
| 5 | Enterprise Backend Architect |
| 6 | API Platform Architect |
| 7 | Security Architect |
| 8 | Database Architect |
| 9 | Cloud Architect |
| 10 | Platform Reliability Architect |
| 11 | Clean Architecture & DDD Specialist |
| 12 | Technical Documentation Lead |
| 13 | QA Architect |

---

## Document Control

| Field | Value |
|-------|--------|
| **Document** | Sprint 28 Architecture Review Board Recommendation |
| **Sprint** | 28 — API Developer Portal |
| **Version** | **1.1** |
| **Status** | **Locked — Ready for Future Reference** |
| **Next Stage** | **FRD-28 Draft** |
| **Architecture Lock** | v1.1 — must remain unchanged |
| **Prior release baseline** | ERP Core v1.22-beta (Sprint 27 closed) |
| **Mode** | Recommendation only — no FRD, ERD, schema, APIs, or implementation |
| **Classification** | Internal — Confidential |

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-27 | Initial Architecture Review Board Recommendation for Sprint 28 — API Developer Portal. Unanimous APPROVED WITH CONSTRAINTS. No FRD, ERD, tables, APIs, SQL, migrations, or implementation. Architecture Lock v1.1 preserved. |
| 1.1 | 2026-07-27 | Editorial Lock only. Added Permanent Enterprise Architecture Review Board banner; metadata Version 1.1 / Locked — Ready for Future Reference / Next Stage FRD-28 Draft; Enterprise API Platform Design Principles; API Capability Classification; ASCII architecture overview; Implementation Recommendation Flow; Version Compatibility Matrix; Risk severity classification; Permanent Architectural Constraints; permanent closing. No ownership, scope, dependency, entity-count, phase, risk-text, or recommendation changes. No redesign. |

---

## Authoritative Planning Baseline

| Rule | Statement |
|------|-----------|
| **Authority** | This recommendation is the **authoritative planning baseline** for Sprint 28. |
| **Conformance** | **FRD-28**, **ERD-28**, **Backend Planning**, **Implementation**, **Validation**, **Release Documentation**, and **Sprint Reports** must conform to this recommendation. |
| **Deviation** | Any future deviation requires **unanimous approval** from the Permanent Enterprise Architecture Review Board. |
| **Architecture Lock** | Architecture Lock v1.1 remains **immutable**. |

---

## Mandatory baseline review (completed)

| Baseline | Status |
|----------|--------|
| BRD v1.0 | Reviewed — API-first · REST/Webhooks/OAuth · Developers stakeholder · Integration Hub · Stage 6 Integrations |
| SDD v1.1 (file `ERP_SDD_v1.0.md`, ADR-002 aligned) | Reviewed — OpenAPI auto-generated · Integration Hub · API Gateway layer · C-02/C-03 |
| DBS v1.1 (file `ERP_DBS_v1.0.md`, version 1.1) | Reviewed — schema/prefix/UUID/soft-delete standards already sufficient |
| Architecture Lock v1.1 | Reviewed — modular monolith · Clean Architecture · no peer DB · Integration Hub for integrations |
| Master FRD | Reviewed — consolidates FRD-01–22 only (FRD-23–27 exist as locked peers; Master FRD lag noted) |
| FRD-01–27 (locked) | Reviewed — no existing FRD for API Developer Portal |
| ERD-01–27 (locked) | Reviewed — no existing ERD for API Developer Portal |
| Sprint 26 (Low-Code) · Sprint 27 (AI) | Reviewed — metadata/control-plane pattern established and closed |

**ARB conflict scan:** No hard conflict that blocks Sprint 28 **if** Developer Portal is scoped as a **developer experience / catalog / entitlement metadata layer** and does **not** absorb Integration Hub, Foundation IAM, Customer/Vendor Portal, or a full API Gateway product.

---

## Enterprise API Platform Design Principles

Editorial only. Principles reinforce Architecture Lock v1.1 and the existing Sprint 28 recommendation — they do not redesign ownership or scope.

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

---

## API Capability Classification

No new capabilities. Classification of capabilities already recommended in §4 Scope only.

| Classification | Capabilities (from existing recommendation) |
|----------------|-----------------------------------------------|
| **Core** | Developer identity & access metadata · Application registration metadata (Hub UUID bindings) · API product catalog (products · versions · environment bindings) · Subscription / plan / entitlement metadata · RBAC namespace + Foundation workflows for account/app/subscription approval |
| **Extension** | Documentation catalog (guides · changelog · OpenAPI artifact references) · Sandbox / environment registration metadata · Portal operational reports (usage projected from Integration Hub) · Try-it session metadata (non-gateway; Phase 3) |
| **Future** | Production frontend product · GraphQL / gRPC developer surfaces (SDD future) · Full API Gateway product (Kong/Envoy — deferred per ERD-21) · Customer Portal / Vendor Portal merge (explicitly forbidden) |

---

## Architecture Overview (ASCII)

Documentation only. Reflects existing ownership and dependency recommendation — no redesign.

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

---

## Implementation Recommendation Flow

Documentation only. No implementation details.

```text
Architecture Review
        ↓
FRD
        ↓
ERD Planning
        ↓
Detailed ERD
        ↓
Backend Planning
        ↓
Implementation
        ↓
Validation
        ↓
Release
```

---

## Architectural Governance Chain

ASCII only. No implementation details.

```text
Architecture Review Board
        ↓
FRD
        ↓
ERD Planning
        ↓
Detailed ERD
        ↓
Backend Planning
        ↓
Implementation
        ↓
Validation
        ↓
Release
        ↓
Production
```

---

## Version Compatibility Matrix

Documentation-level compatibility only. No implementation.

| Artifact | Compatibility concern |
|----------|----------------------|
| **API Product Version** | Portal catalog version of a published API product must map to a stable product identity |
| **API Version** | Platform API path version (e.g. `/api/v1`) remains platform-owned; portal binds products to published versions |
| **Documentation Version** | Doc/guide/changelog version must align to the referenced API Product Version |
| **Subscription Version** | Entitlement/subscription metadata must reference a specific API Product Version (or compatible set) |
| **SDK Version** | Optional future SDK packaging version must track OpenAPI / API Product Version (not owned in Sprint 28 implementation) |
| **OpenAPI Version** | OpenAPI artifact reference / snapshot version; FastAPI remains generator — portal catalogs references only |

---

## 1. Overall architectural assessment

Sprint 28 is a **valid next platform domain**, but it is **not already named** as a locked module in BRD/SDD/Architecture Lock. It fits the post–FRD-22 pattern used for Customer Portal, Vendor Portal, BPM, Low-Code, and AI:

- New bounded context under `modules/<domain>/`
- Own schema + prefix
- **Contracts / UUID only** to peers
- **No redesign** of completed modules
- Prefer **metadata / control-plane first**; defer full runtime/UI where Architecture Lock already defers gateway product depth

**Critical distinction**

| Existing capability | Owner today | Developer Portal must **not** become |
|---------------------|-------------|--------------------------------------|
| OpenAPI / Swagger generation | FastAPI platform (`/docs`, `/openapi.json`) per SDD | Owner of OpenAPI generation |
| API credentials · OAuth clients · API usage · rate limits · connectors · webhooks | **Integration Hub** (FRD-21 / ERD-21 · 20 tables) | Duplicate credential/usage/rate-limit SoR |
| Full API Gateway (Kong/Envoy-class) | Explicitly **out of scope** in ERD-21 Phase 1 | Gateway product replacement |
| AuthN / AuthZ / users / RBAC / JWT | **Foundation** | Second IAM |
| Customer self-service | **Customer Portal** (FRD-23) | Customer UX |
| Supplier self-service | **Vendor Portal** (FRD-24) | Supplier UX |
| AI rate limits / AI gateway policies | **AI Platform** (FRD-27) | AI traffic governance |

**Correct architectural role for Sprint 28**

> **API Developer Portal = developer self-service + API product catalog + subscription/entitlement metadata + documentation/sandbox experience metadata**, integrating with Integration Hub, Foundation, and DMS **through contracts only**.

It is analogous to Customer/Vendor Portal (envelope/self-service) + Low-Code/AI (metadata-first), **not** a second Integration Hub.

---

## 2. Dependency verification

| Dependency | Required | Integration mode |
|------------|----------|------------------|
| Foundation (Auth · RBAC · Audit · Notification · Workflow) | **Mandatory** | Services only |
| Organization / tenant context | **Mandatory** | UUID + context filters |
| Integration Hub | **Mandatory** | UUID refs to credentials / OAuth clients / usage / rate limits — **no peer ORM** |
| Document Management | **Recommended** | UUID refs for published docs / OpenAPI artifacts |
| Analytics | Optional | Read-only metrics consumption |
| All business modules (Finance…AI) | **Contract-only** | Consume published API contracts / OpenAPI paths — never own their data |
| Customer Portal / Vendor Portal | **None as SoR** | Distinct audiences; no shared ownership |
| Low-Code / BPM / AI | **None as SoR** | No redesign; optional future UUID hooks only |

Upstream readiness: Foundation → Integration Hub → Portals → BPM → Low-Code → AI are complete. Dependency chain for a **platform DX layer** is satisfied.

---

## 3. Ownership verification

| Concern | Owner (unchanged) |
|---------|-------------------|
| Business SoR (all FRD-03–20 domains) | Existing business modules |
| Connectivity / transport / connectors / webhooks / events / queues | Integration Hub |
| API credential & OAuth client **secrets/config SoR** | Integration Hub |
| API usage metering & rate-limit **enforcement metadata (integration)** | Integration Hub |
| Identity · JWT · RBAC · users | Foundation |
| Workflow approvals | Foundation / BPM |
| Notifications delivery | Foundation Notification (+ Hub transport where already defined) |
| Document file storage | Document Management |
| Customer / Vendor self-service | Customer Portal / Vendor Portal |
| Form/page design metadata | Low-Code |
| Intelligence metadata | AI Platform |
| **Developer org · apps · API products · subscriptions · portal UX metadata · doc catalog · sandbox registration** | **API Developer Portal (proposed)** |

**Forbidden ownership transfers:** none of the completed modules may be redesigned or stripped of SoR to “fit” the portal.

---

## 4. Scope recommendation for Sprint 28

### In scope (recommended)

1. **Developer identity & access metadata** — developer accounts, orgs/teams, invites, sessions (portal-style; Foundation remains Auth SoR)  
2. **Application registration metadata** — apps/clients with **UUID refs** to Integration Hub `int_oauth_client` / `int_api_credential` (or create-via-contract; never duplicate secret storage)  
3. **API product catalog** — products, versions, environment bindings (metadata of which platform APIs are published for external consumption)  
4. **Subscription / plan / entitlement metadata** — which apps may call which products/scopes  
5. **Documentation catalog** — guides, changelog entries, OpenAPI artifact **references** (DMS UUID or published snapshot refs — not FastAPI codegen ownership)  
6. **Sandbox / environment registration metadata** — non-production environment pointers  
7. **Portal operational reports** — DX metrics; usage **projected from** Integration Hub via services  
8. **RBAC namespace** (e.g. `devportal.*`) + Foundation workflows for account/app/subscription approval  

### Explicitly out of scope

- Redesign of any FRD-01–27 module  
- Second Integration Hub / second credential vault  
- Full API Gateway product (Kong/Envoy) — remains deferred per ERD-21  
- Owning business APIs or business data  
- Replacing `/docs` / `/openapi.json` platform generation  
- Customer Portal / Vendor Portal merge  
- AI gateway / AI rate-limit ownership  
- Production frontend product (may defer UI like Sprint 26/27)  
- GraphQL / gRPC developer surfaces (SDD future)  

**Proposed technical packaging (planning only):** new module e.g. `modules/devportal/` · schema/prefix TBD under DBS rules · mount e.g. `/api/v1/devportal` · release target **ERP Core v1.23-beta (planned)**.

---

## 5. Risks and assumptions

### Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-28-01 | Overlap with Integration Hub (credentials, usage, rate limits) | **High** | Hard ownership matrix in FRD-28; UUID/contract only |
| R-28-02 | Accidental “API Gateway” scope creep | **Critical** | Keep ERD-21 deferral; portal stores entitlement metadata only |
| R-28-03 | Confusion with Customer/Vendor Portal | **Medium** | Distinct audience (developers/partners building integrations) |
| R-28-04 | Master FRD lag (01–22 only) | **Low** | FRD-28 as locked peer; Master FRD consolidation is doc debt, not a redesign |
| R-28-05 | Treating auto-OpenAPI as portal SoR | **Medium** | Portal catalogs/publishes references; FastAPI remains generator |
| R-28-06 | Secret storage in portal tables | **High** | Secrets remain Hub/vault; portal stores refs only |

### Assumptions

- Sprint 28 follows the established **metadata-first backend** delivery pattern.  
- Integration Hub remains the **connectivity SoR**.  
- Architecture Lock v1.1 is **not** modified; module is additive.  
- Frontend may be deferred unless separately authorized.  
- “API Developer Portal” elaborates BRD Stage 6 / API Requirements / Developers stakeholder — it does not invent a conflicting product.

---

## 6. Suggested implementation phases

| Phase | Focus | Intent |
|-------|--------|--------|
| **Phase 0** | Schema shell · module scaffold · Alembic bootstrap | Foundation only |
| **Phase 1** | Developer identity · org/team · application registration · API product/version catalog | Core DX spine |
| **Phase 2** | Plans · subscriptions · entitlements · Hub credential/OAuth **UUID bindings** | Access governance metadata |
| **Phase 3** | Documentation catalog · environments/sandbox metadata · try-it session metadata (non-gateway) | DX content & sandbox |
| **Phase 4** | Usage/report projections · hardening · permissions seed · validation gate | Operational close |

Then: Validation → Validation Fix (if needed) → Release Notes (v1.23-beta) → Completion Report — same governance path as Sprint 26/27.

---

## 7. Estimated entity count

| Estimate | Count | Rationale |
|----------|------:|-----------|
| **ARB planning range** | **16–22** | Between Low-Code (18) and Portal/Integration (20) |
| **Recommended FRD target** | **~18–20** | Enough for catalog + identity + subscription + docs + reports without Hub duplication |
| **Not a 34-class domain** | — | AI-scale inventory is inappropriate for a DX envelope |

Final locked count must wait for FRD-28 / ERD-28 — **do not invent tables now**.

---

## 8. Whether BRD requires changes

| Verdict | Detail |
|---------|--------|
| **No mandatory redesign** | BRD already requires REST · Webhooks · OAuth · API-first · Developers as users · Integration Hub · Stage 6 External Integrations |
| **Optional editorial addendum** | Clarify “API Developer Portal” as the self-service developer experience layer under Stage 6 / API Requirements — **additive wording only** |
| **Primary vehicle** | **FRD-28** (new locked FRD), not a BRD rewrite |

---

## 9. Whether SDD requires changes

| Verdict | Detail |
|---------|--------|
| **No Architecture Lock / ADR redesign** | Stack, Clean Architecture, C-01–C-06, DG rules unchanged |
| **No mandatory SDD rewrite** | OpenAPI auto-generation and Integration Hub already defined |
| **Optional editorial note** | Document Developer Portal as DX/catalog/entitlement layer consuming Hub + OpenAPI — after FRD-28 lock |

---

## 10. Whether DBS requires changes

| Verdict | Detail |
|---------|--------|
| **No DBS standard changes** | UUID PK · schema-per-domain · prefix · soft-delete · version · tenant/company already locked |
| **New schema allowed by existing rules** | Prefix/schema chosen in ERD-28 under DBS naming standards |

---

## 11. Final unanimous ARB recommendation

| # | Role | Verdict |
|---|------|---------|
| 1 | Enterprise Solution Architect | **APPROVED WITH CONSTRAINTS** |
| 2 | Chief Enterprise Architect | **APPROVED WITH CONSTRAINTS** |
| 3 | ERP Product Architect | **APPROVED WITH CONSTRAINTS** |
| 4 | Principal Software Engineer | **APPROVED WITH CONSTRAINTS** |
| 5 | Enterprise Backend Architect | **APPROVED WITH CONSTRAINTS** |
| 6 | API Platform Architect | **APPROVED WITH CONSTRAINTS** |
| 7 | Security Architect | **APPROVED WITH CONSTRAINTS** |
| 8 | Database Architect | **APPROVED WITH CONSTRAINTS** |
| 9 | Cloud Architect | **APPROVED WITH CONSTRAINTS** |
| 10 | Platform Reliability Architect | **APPROVED WITH CONSTRAINTS** |
| 11 | Clean Architecture & DDD Specialist | **APPROVED WITH CONSTRAINTS** |
| 12 | Technical Documentation Lead | **APPROVED WITH CONSTRAINTS** |
| 13 | QA Architect | **APPROVED WITH CONSTRAINTS** |

### Unanimous decision

**PROCEED to Sprint 28 FRD-28 drafting under the following binding constraints:**

1. **Architecture Lock v1.1 — preserved (no modification).**  
2. **No redesign** of any completed module (Foundation through Enterprise AI Platform).  
3. API Developer Portal owns **developer experience / catalog / entitlement / documentation-sandbox metadata only**.  
4. **Integration Hub remains SoR** for connectors, credentials, OAuth clients, transport, integration usage, and integration rate-limit metadata.  
5. **Foundation remains SoR** for AuthN/AuthZ/RBAC/Audit/Notification/Workflow.  
6. Integration with all modules is **contracts / UUID / services only** — **no peer ORM**.  
7. Full API Gateway product remains **out of scope** (consistent with ERD-21).  
8. **Do not create ERD/tables/APIs/migrations** until FRD-28 is locked.  
9. Target entity inventory **~18–20** (range 16–22) pending FRD/ERD lock.  
10. BRD/SDD/DBS: **no mandatory redesign**; optional editorial clarifications only.

**Next authorized step:** FRD-28 Draft — still documentation-only until explicitly authorized.

---

## Permanent Architectural Constraints

Summary of existing constraints only. No new constraints introduced.

| # | Constraint |
|---|------------|
| 1 | Architecture Lock v1.1 preserved — no modification |
| 2 | No redesign of completed modules (Foundation through Enterprise AI Platform) |
| 3 | API Developer Portal owns DX / catalog / entitlement / documentation-sandbox metadata only |
| 4 | Integration Hub remains connectivity / credential / usage / rate-limit metadata SoR |
| 5 | Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow SoR |
| 6 | Contracts / UUID / services only — no peer ORM |
| 7 | Full API Gateway product remains out of scope (ERD-21) |
| 8 | No ERD / tables / APIs / migrations until FRD-28 is locked |
| 9 | Entity inventory target ~18–20 (range 16–22) pending FRD/ERD lock |
| 10 | BRD / SDD / DBS — no mandatory redesign |
| 11 | Unanimous Permanent ARB approval required before implementation |
| 12 | Customer Portal, Vendor Portal, Low-Code, BPM, and AI ownership unchanged |

---

## Permanent Implementation Rules

These rules become mandatory for every future Sprint 28 implementation phase.

---

Every implementation phase shall begin with:

• Permanent Enterprise Architecture Review Board review

• Locked document verification

• Architecture conflict scan

• Ownership verification

Every implementation phase shall end with:

• Validation Gate

• Architect Review Checklist

• Enterprise Risk Review

• Completion Report

Validation Fix is permitted ONLY for:

• Ruff

• MyPy

• Pytest

• FastAPI/OpenAPI

• Import issues

• Static analysis findings

Validation Fix SHALL NOT introduce:

• new functionality

• new entities

• new APIs

• schema changes

• migrations

• architecture changes

• ownership changes

Release Documentation SHALL:

• summarize only completed implementation

• never introduce implementation

• never redesign documentation

Sprint Completion Report SHALL:

• summarize the completed sprint

• preserve Architecture Lock

• preserve all locked baselines

Git Release SHALL occur ONLY AFTER:

• Validation PASS

• Validation Fix PASS (if required)

• Release Documentation

• Sprint Completion Report

Every future Sprint implementation must preserve:

• Architecture Lock v1.1

• Locked BRD

• Locked SDD

• Locked DBS

• Locked FRD

• Locked ERD

• Locked Backend Planning

This section defines the permanent implementation governance standard for Sprint 28 and all future Enterprise ERP modules unless superseded by unanimous approval of the Permanent Enterprise Architecture Review Board.

---

## Closing Statement

Recommendation Complete.

Architecture Lock v1.1 preserved.

Ready for FRD-28.

This recommendation becomes the authoritative planning baseline for Sprint 28 until superseded by a future unanimous Permanent Enterprise Architecture Review Board decision.
