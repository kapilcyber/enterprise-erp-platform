# ERD-28 — Entity Planning  
## API Developer Portal

| Field | Value |
|-------|--------|
| **Document** | ERD-28 API Developer Portal Entity Planning |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Document Status** | Locked |
| **Next Stage** | ERD-28 Detailed ERD |
| **Schema / Prefix (proposed)** | `devportal` / `dp_` |
| **Business Entities (recommended)** | Exactly **18** |
| **Aligned To** | FRD-28 (Locked v1.1) · Architecture Lock v1.1 (C-01–C-06) · Sprint 28 ARB Recommendation Locked v1.1 · FRD-01 Foundation · FRD-19 Document · FRD-21 Integration Hub · FRD-23 Customer Portal · FRD-24 Vendor Portal |
| **Prior Release** | ERP Core v1.22-beta |
| **Planned Delivery** | ERP Core v1.23-beta (planned) |

> **Planning only.** No Mermaid, SQL, columns, indexes, PK/FK diagrams, migrations, APIs, repository design, service layer, or implementation in this document.

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-28 | Initial Entity Planning for API Developer Portal. Exactly **18** entities from Permanent Enterprise Architecture Review Board unanimously approved ERD-28 Entity Planning Analysis. Draft — Ready for Architect Review. No Detailed ERD, Mermaid, SQL, APIs, or implementation. Architecture Lock v1.1 preserved. |
| 1.1 | 2026-07-28 | Editorial Lock after Permanent Enterprise Architecture Review Board unanimous approval. Added Entity Dependency Summary; metadata Version 1.1 / Locked — Ready for Future Reference; closing statement refined. No entity added, removed, or renamed. Still exactly **18** entities. Architecture Lock v1.1 preserved. Ready for ERD-28 Detailed ERD. |

---

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document ID** | ERD-28-EP |
| **Document Title** | API Developer Portal — Entity Planning |
| **Domain** | API Developer Portal |
| **Classification** | Internal — Confidential |
| **Authoritative Baselines** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · Master FRD · FRD-01…FRD-28 (FRD-28 Locked v1.1) · ERD-01…ERD-27 · Sprint 26/27 documentation · Sprint 28 ARB Recommendation Locked v1.1 · Approved ERD-28 Entity Planning Analysis |
| **Permanent ARB** | 13 architects · 20+ years enterprise experience each · unanimous approval required |

---

## 2. Purpose

Entity Planning freezes the **complete business-entity inventory** for the API Developer Portal before Detailed ERD and backend implementation.

Later ERD design and implementation **must use only these entities**. No new Developer Portal entities may appear during implementation without formal Permanent Enterprise Architecture Review Board approval.

This document exists to:

- Translate FRD-28 Locked v1.1 capabilities into a governed entity set of exactly **18** entities
- Preserve Architecture Lock v1.1 and cross-module ownership boundaries
- Prevent over-normalization and SoR duplication with Integration Hub, Foundation, Customer Portal, Vendor Portal, and AI Platform
- Provide a planning baseline for ERD-28 Detailed ERD

**API Developer Portal owns DX / catalog / entitlement / documentation-sandbox metadata only.**  
**Integration Hub remains connectivity SoR. Foundation remains security SoR.**

---

## 3. Entity Design Principles

| Principle | Application |
|-----------|-------------|
| **Developer Portal owns DX metadata only** | Catalog, entitlement, documentation, sandbox, and portal operational metadata — not business documents or transport |
| **Zero duplicate ownership** | Never duplicate Foundation, Integration Hub, Customer Portal, Vendor Portal, or AI SoR |
| **UUID references only** | Peer domains referenced by UUID / contracts — never peer-schema FKs |
| **No peer ORM** | Developer Portal never writes peer-module ORM models |
| **Hub bindings as attributes** | Integration Hub OAuth/credential UUIDs live on `dp_application` — no portal secret-store entity |
| **Version-first catalog** | API Product Versions use Draft → Publish → Retire; published versions are never silently replaced |
| **Avoid over-normalization** | Justified merges only (see inventory merge rationale) |
| **Foundation ownership preserved** | AuthN · AuthZ · RBAC · Audit · Notification · Workflow Engine unchanged |
| **Integration Hub ownership preserved** | Credentials · OAuth clients · usage · rate limits · connectors · transport unchanged |
| **Clean Architecture · DDD · Modular Monolith** | Required at implementation time; not prescribed here as schema |

---

## 4. Entity Classification

Documentation categories only. No implementation. Entity count remains exactly **18**.

| Classification | Entities |
|----------------|----------|
| **Core** | `dp_developer_account` · `dp_developer_organization` · `dp_developer_team` · `dp_developer_membership` · `dp_developer_invite` · `dp_portal_session` · `dp_application` · `dp_api_product` · `dp_api_product_version` · `dp_api_product_environment` · `dp_plan` · `dp_subscription` · `dp_entitlement` |
| **Extension** | `dp_documentation_entry` · `dp_openapi_artifact_reference` · `dp_sandbox_environment` · `dp_tryit_session` |
| **Operational** | `dp_portal_report` |
| **Future Ready** | *(none as Sprint 28 entities — see Future Reserved Capabilities)* |

---

## 5. Entity Inventory

Exactly **18** entities. Approved inventory only — no add · no remove · no rename.

### Coverage → Entity Mapping (justified merges)

| FRD / Planning Concern | Entity Decision |
|------------------------|-----------------|
| Developer account lifecycle | `dp_developer_account` |
| Developer organization | `dp_developer_organization` |
| Developer team | `dp_developer_team` |
| Org/team membership | `dp_developer_membership` |
| Invites | `dp_developer_invite` |
| Portal sessions | `dp_portal_session` |
| Application registration · Hub OAuth/credential UUID bindings | `dp_application` (**Hub UUID attributes merged** — no separate credential-binding entity) |
| API Product identity | `dp_api_product` |
| API Product Version | `dp_api_product_version` |
| Environment bindings | `dp_api_product_environment` |
| Plan | `dp_plan` |
| Subscription | `dp_subscription` |
| Entitlement / scopes | `dp_entitlement` |
| Guides · changelog | **Merged** into `dp_documentation_entry` (entry type) |
| OpenAPI artifact references (DMS UUID / snapshot) | `dp_openapi_artifact_reference` |
| Sandbox / environment registration | `dp_sandbox_environment` |
| Try-it session (non-gateway) | `dp_tryit_session` |
| Portal operational reports · Hub usage projection | `dp_portal_report` |
| AuthN/AuthZ/RBAC/JWT · Audit warehouse · Notification delivery · Workflow Engine | **Not portal entities** — Foundation |
| OAuth secrets · API credentials · usage metering · rate limits · connectors | **Not portal entities** — Integration Hub |
| API Gateway product | **Out of scope** — ERD-21 deferral |

### 1. `dp_developer_account`

| Field | Value |
|-------|--------|
| **Entity Name** | Developer Account |
| **Purpose** | Portal developer identity metadata (draft → submit → approve → active / lock / suspend / retire). |
| **Ownership** | API Developer Portal |
| **Aggregate** | Developer Identity |
| **Merge rationale** | — |
| **Notes** | Foundation remains Auth SoR. Portal account is DX metadata only — not a parallel user store. |

### 2. `dp_developer_organization`

| Field | Value |
|-------|--------|
| **Entity Name** | Developer Organization |
| **Purpose** | Developer organization metadata for partner/internal developer groupings. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Developer Identity |
| **Merge rationale** | — |
| **Notes** | Does not replace Organization domain masters (C-01). |

### 3. `dp_developer_team`

| Field | Value |
|-------|--------|
| **Entity Name** | Developer Team |
| **Purpose** | Team metadata under a developer organization. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Developer Identity |
| **Merge rationale** | Kept separate from Organization per approved analysis (orgs/teams first-class). |
| **Notes** | Not Foundation RBAC groups. |

### 4. `dp_developer_membership`

| Field | Value |
|-------|--------|
| **Entity Name** | Developer Membership |
| **Purpose** | Membership of a developer account in an organization and/or team. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Developer Identity |
| **Merge rationale** | — |
| **Notes** | Links account ↔ org/team; role metadata only within portal. |

### 5. `dp_developer_invite`

| Field | Value |
|-------|--------|
| **Entity Name** | Developer Invite |
| **Purpose** | Invitation lifecycle for onboarding developers to orgs/teams. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Developer Identity |
| **Merge rationale** | Kept separate from Membership for approval-workflow clarity (approved analysis). |
| **Notes** | Approvals via Foundation Workflow (C-04). |

### 6. `dp_portal_session`

| Field | Value |
|-------|--------|
| **Entity Name** | Portal Session |
| **Purpose** | Developer portal session metadata (active / expired / revoked). |
| **Ownership** | API Developer Portal |
| **Aggregate** | Developer Identity |
| **Merge rationale** | — |
| **Notes** | Does not replace Foundation session/JWT SoR. |

### 7. `dp_application`

| Field | Value |
|-------|--------|
| **Entity Name** | Application |
| **Purpose** | Application registration metadata for consumer apps; binds to Integration Hub OAuth client / API credential by UUID. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Application Registration |
| **Merge rationale** | **Hub OAuth/credential UUID bindings merged as attributes** — no portal secret-store or credential-binding entity. |
| **Notes** | Secrets remain Integration Hub / vault. Create-via-contract permitted; never duplicate Hub SoR. |

### 8. `dp_api_product`

| Field | Value |
|-------|--------|
| **Entity Name** | API Product |
| **Purpose** | Stable catalog identity for an API product published for external/developer consumption. |
| **Ownership** | API Developer Portal |
| **Aggregate** | API Product Catalog |
| **Merge rationale** | — |
| **Notes** | Does not own business APIs or OpenAPI generation. |

### 9. `dp_api_product_version`

| Field | Value |
|-------|--------|
| **Entity Name** | API Product Version |
| **Purpose** | Versioned catalog unit (Draft / Published / Retired); published versions are immutable. |
| **Ownership** | API Developer Portal |
| **Aggregate** | API Product Catalog |
| **Merge rationale** | — |
| **Notes** | Version Compatibility Policy: subscriptions bind to exact published product versions. |

### 10. `dp_api_product_environment`

| Field | Value |
|-------|--------|
| **Entity Name** | API Product Environment |
| **Purpose** | Environment binding metadata for API product versions (e.g. sandbox vs production pointers). |
| **Ownership** | API Developer Portal |
| **Aggregate** | API Product Catalog |
| **Merge rationale** | Kept separate from Version per FRD environment-binding requirement (approved analysis). |
| **Notes** | Metadata only — not a gateway or runtime router. |

### 11. `dp_plan`

| Field | Value |
|-------|--------|
| **Entity Name** | Plan |
| **Purpose** | Access/plan metadata governing subscription offerings. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Access Governance |
| **Merge rationale** | — |
| **Notes** | Not Integration Hub rate-limit policy. |

### 12. `dp_subscription`

| Field | Value |
|-------|--------|
| **Entity Name** | Subscription |
| **Purpose** | Subscription metadata binding applications to plans / API product versions. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Access Governance |
| **Merge rationale** | — |
| **Notes** | Subject to Foundation workflow approval where required. |

### 13. `dp_entitlement`

| Field | Value |
|-------|--------|
| **Entity Name** | Entitlement |
| **Purpose** | Entitlement / scope metadata granted under a subscription. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Access Governance |
| **Merge rationale** | Kept separate from Subscription per approved ownership list (Subscription metadata · Entitlement metadata). |
| **Notes** | Entitlement metadata only — not Hub usage metering or rate-limit enforcement. |

### 14. `dp_documentation_entry`

| Field | Value |
|-------|--------|
| **Entity Name** | Documentation Entry |
| **Purpose** | Documentation catalog entries for guides and changelog items. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Documentation Catalog |
| **Merge rationale** | **Guides + changelog merged** into one entity via entry type (avoid over-normalization). |
| **Notes** | Aligns to API Product Version per Version Compatibility Policy. |

### 15. `dp_openapi_artifact_reference`

| Field | Value |
|-------|--------|
| **Entity Name** | OpenAPI Artifact Reference |
| **Purpose** | Reference metadata for OpenAPI artifacts (DMS UUID or published snapshot ref). |
| **Ownership** | API Developer Portal |
| **Aggregate** | Documentation Catalog |
| **Merge rationale** | Kept separate from Documentation Entry so OpenAPI refs remain explicit (FR-28-012/013). |
| **Notes** | FastAPI remains OpenAPI generator; portal catalogs references only. Document Management remains file SoR. |

### 16. `dp_sandbox_environment`

| Field | Value |
|-------|--------|
| **Entity Name** | Sandbox Environment |
| **Purpose** | Non-production sandbox / environment registration metadata. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Sandbox Experience |
| **Merge rationale** | — |
| **Notes** | Pointers/metadata only — not a runtime sandbox executor or gateway. |

### 17. `dp_tryit_session`

| Field | Value |
|-------|--------|
| **Entity Name** | Try-it Session |
| **Purpose** | Try-it session metadata for DX experimentation (non-gateway). |
| **Ownership** | API Developer Portal |
| **Aggregate** | Sandbox Experience |
| **Merge rationale** | — |
| **Notes** | Extension capability; must not become API Gateway or live invoke SoR. |

### 18. `dp_portal_report`

| Field | Value |
|-------|--------|
| **Entity Name** | Portal Report |
| **Purpose** | Portal operational report metadata; DX metrics with usage **projected from Integration Hub** via services. |
| **Ownership** | API Developer Portal |
| **Aggregate** | Portal Operations |
| **Merge rationale** | — |
| **Notes** | Portal is not usage metering SoR. Analytics may consume read-only. |

**Business Entities: 18** · **Schema (proposed): `devportal`** · **Prefix (proposed): `dp_`**

---

## 6. Aggregate Boundaries

| Aggregate | Conceptual Root | Members |
|-----------|-----------------|---------|
| **Developer Identity** | Developer Account / Organization | `dp_developer_account` · `dp_developer_organization` · `dp_developer_team` · `dp_developer_membership` · `dp_developer_invite` · `dp_portal_session` |
| **Application Registration** | Application | `dp_application` |
| **API Product Catalog** | API Product | `dp_api_product` · `dp_api_product_version` · `dp_api_product_environment` |
| **Access Governance** | Plan / Subscription | `dp_plan` · `dp_subscription` · `dp_entitlement` |
| **Documentation Catalog** | Documentation Entry | `dp_documentation_entry` · `dp_openapi_artifact_reference` |
| **Sandbox Experience** | Sandbox Environment | `dp_sandbox_environment` · `dp_tryit_session` |
| **Portal Operations** | Portal Report | `dp_portal_report` |

DDD aggregate boundaries are planning guidance for Detailed ERD. No relationship cardinality or schema is prescribed here.

---

## 7. Cross-Module Ownership

| Concern | Owner |
|---------|--------|
| Developer org · team · account · membership · invite · session · application · API products/versions/environments · plans · subscriptions · entitlements · documentation catalog · OpenAPI artifact refs · sandbox · try-it · portal reports | **API Developer Portal (this ERD)** |
| Authentication · Authorization · RBAC · JWT · users · Audit warehouse · Notification delivery · Workflow Engine | **Foundation** |
| API credentials · OAuth clients · secrets · connectors · webhooks · events · queues · API usage metering · rate-limit enforcement metadata · transport | **Integration Hub** |
| Document file storage | **Document Management** |
| Customer self-service | **Customer Portal** |
| Supplier self-service | **Vendor Portal** |
| Forms / pages | **Low-Code** |
| Workflow design / BPM runtime | **BPM** (+ Foundation Workflow) |
| Intelligence metadata | **AI Platform** |
| Enterprise BI / reporting warehouse | **Analytics** (optional read-only DX metrics) |
| Business transactions / masters | **Business modules / Master Data** |
| Full API Gateway product | **Out of scope** (ERD-21 deferral) |

**Forbidden:** peer ORM writes · portal secret vaults · portal-owned OpenAPI generation · portal-owned API Gateway · merge with Customer/Vendor Portal.

---

## 8. Dependency Overview

ASCII only. Planning visualization — **not an ERD**.

```text
Developer
        ↓
Application
        ↓
API Product
        ↓
Plan
        ↓
Subscription
        ↓
Entitlement
        ↓
Documentation
        ↓
Sandbox
        ↓
Portal Report
```

### Cross-module contract dependencies (planning)

```text
Foundation (Auth · RBAC · Audit · Notification · Workflow)
        ↓
Developer Portal (DX / catalog / entitlement metadata)
        ↓
Integration Hub (credential / OAuth UUID · usage projection)
        ↓
Document Management (artifact UUID refs)
```

ASCII only. No Mermaid. No relationship cardinality. No schema.

---

## 9. Recommended Implementation Order

Planning guidance only — **not** a sprint execution plan and **not** implementation:

| Order | Group | Entities (indicative) |
|------:|-------|------------------------|
| 1 | Developer Identity | `dp_developer_account` · `dp_developer_organization` · `dp_developer_team` · `dp_developer_membership` · `dp_developer_invite` · `dp_portal_session` |
| 2 | Application Registration | `dp_application` |
| 3 | API Product Catalog | `dp_api_product` · `dp_api_product_version` · `dp_api_product_environment` |
| 4 | Access Governance | `dp_plan` · `dp_subscription` · `dp_entitlement` |
| 5 | Documentation Catalog | `dp_documentation_entry` · `dp_openapi_artifact_reference` |
| 6 | Sandbox Experience | `dp_sandbox_environment` · `dp_tryit_session` |
| 7 | Portal Operations | `dp_portal_report` |

No APIs, migrations, repositories, or services are prescribed here.

---

## 10. Phase Distribution

Must match the approved ERD-28 Entity Planning Analysis and FRD-28 Locked v1.1 phases — **unchanged**.

| Phase | Focus | Entities | Cumulative |
|-------|--------|----------|------------|
| **Phase 0** | Schema shell · module scaffold · Alembic bootstrap | *(none)* | **0 / 18** |
| **Phase 1** | Developer identity · application · API product catalog | `dp_developer_account` · `dp_developer_organization` · `dp_developer_team` · `dp_developer_membership` · `dp_developer_invite` · `dp_portal_session` · `dp_application` · `dp_api_product` · `dp_api_product_version` · `dp_api_product_environment` | **10 / 18** |
| **Phase 2** | Plans · subscriptions · entitlements | `dp_plan` · `dp_subscription` · `dp_entitlement` | **13 / 18** |
| **Phase 3** | Documentation · sandbox · try-it | `dp_documentation_entry` · `dp_openapi_artifact_reference` · `dp_sandbox_environment` · `dp_tryit_session` | **17 / 18** |
| **Phase 4** | Portal reports · hardening · permissions seed · validation | `dp_portal_report` | **18 / 18** |

Then: Validation → Validation Fix (if needed) → Release Notes · Completion Report — per Permanent Implementation Rules.

---

## 11. Future Reserved Capabilities

Documentation only. **No entities** in Sprint 28 inventory.

| Roadmap Item | Notes |
|--------------|-------|
| Developer Marketplace | Future certified partner integration catalog |
| SDK Registry | Future SDK packages versioned against OpenAPI / API Product Version |
| Webhook Catalog | Future discoverability of Hub webhooks (Hub remains SoR) |
| GraphQL Explorer | Future DX surface if GraphQL authorized (SDD future) |
| Plugin Marketplace | Future governed plugin discovery without portal owning execution |
| Future API Discovery enhancements | Search/tagging improvements over locked catalog |
| Production frontend / DX UI | Separately authorized |
| Full API Gateway (Kong/Envoy) | Remains deferred per ERD-21 — **not** a portal ownership transfer |

---

## Entity Dependency Summary

Documentation only. No new entities. No implementation.

| Aggregate | Primary Dependency |
|-----------|--------------------|
| Developer Identity | Foundation |
| Application Registration | Integration Hub |
| API Product Catalog | Integration Hub |
| Access Governance | Foundation |
| Documentation Catalog | Document Management |
| Sandbox Experience | Integration Hub |
| Portal Operations | Analytics |

---

## 12. Permanent Architectural Constraints

| # | Constraint |
|---|------------|
| 1 | Architecture Lock v1.1 is FINAL — no modification |
| 2 | Exactly **18** entities — no add · no remove · no rename without unanimous Permanent ARB approval |
| 3 | API Developer Portal owns DX / catalog / entitlement / documentation-sandbox / portal operational metadata only |
| 4 | Integration Hub remains connectivity / credential / usage / rate-limit SoR |
| 5 | Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow SoR |
| 6 | Contracts / UUID / services only — **no peer ORM** |
| 7 | Full API Gateway product remains out of scope |
| 8 | Customer Portal and Vendor Portal remain distinct — no merge |
| 9 | AI Platform ownership unchanged |
| 10 | No Detailed ERD, Mermaid, SQL, APIs, migrations, or implementation in this document |
| 11 | BRD / SDD / DBS — no mandatory redesign |
| 12 | Unanimous Permanent ARB approval required before implementation |

---

## 13. Metadata

| Field | Value |
|-------|--------|
| **Version** | **1.1** |
| **Status** | **Locked — Ready for Future Reference** |
| **Document Status** | **Locked** |
| **Next Stage** | **ERD-28 Detailed ERD** |
| **Entity Count** | **18** |
| **Schema / Prefix (proposed)** | `devportal` / `dp_` |
| **Architecture Lock** | v1.1 — Preserved |

---

## 14. Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-28 | Initial Entity Planning for API Developer Portal (exactly 18 entities). Draft — Ready for Architect Review. Aligned to FRD-28 Locked v1.1 and Permanent ARB approved Entity Planning Analysis. No Detailed ERD, Mermaid, SQL, APIs, or implementation. Architecture Lock v1.1 preserved. |
| 1.1 | 2026-07-28 | Editorial Lock after Permanent Enterprise Architecture Review Board unanimous approval. Added Entity Dependency Summary; metadata Version 1.1 / Locked — Ready for Future Reference / Document Status Locked. No entity added, removed, or renamed. Still exactly **18** entities. No functional or ownership changes. Ready for ERD-28 Detailed ERD. |

---

## 15. Closing Statement

ERD-28 Entity Planning is now Locked and becomes the baseline for all future Detailed ERD, backend implementation, validation, and release activities.

No architectural or ownership changes were introduced.

No Detailed ERD, Mermaid, SQL, APIs, Migrations, Backend Planning, or Implementation are included in this document.
