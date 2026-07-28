# ERP Core v1.23-beta — Release Notes

| Field | Value |
|-------|--------|
| **Document Type** | Enterprise Release Notes |
| **Release Name** | ERP Core v1.23-beta |
| **Release Status** | Release Ready |
| **Architecture Lock** | v1.1 — Maintained |
| **Prepared As** | Enterprise Solution Architect · ERP Product Architect · Technical Documentation Lead · Release Manager · Principal Software Engineer · API Platform Architect |
| **Classification** | Internal — Confidential |
| **Predecessor** | [ERP Core v1.22-beta](./ERP_Core_v1.22-beta.md) |
| **Primary Deliverable** | Sprint 28 — API Developer Portal |

---

## 1. Release Information

| Field | Value |
|-------|--------|
| **Version** | ERP Core v1.23-beta |
| **Release Name** | ERP Core v1.23-beta |
| **Sprint** | Sprint 28 — API Developer Portal |
| **Status** | Release Ready |
| **Release Date** | TBD |
| **Architecture Lock** | v1.1 — Preserved |
| **Previous Release** | ERP Core v1.22-beta |
| **FRD / ERD** | FRD-28 Locked v1.1 · ERD-28 Entity Planning Locked v1.1 · ERD-28 Detailed ERD Locked v1.1 |
| **Backend Planning** | Sprint 28 Backend Planning Locked v1.1 |
| **Recommended Git Tag** | `v1.23-beta` |

---

## 2. Release Overview

Sprint 28 delivered the **API Developer Portal** backend as the enterprise DX / catalog / entitlement / documentation-sandbox / portal-operations **metadata** foundation — developer identity → application registration → API product catalog → plans / subscriptions / entitlements → documentation / OpenAPI artifact references → sandbox / try-it → portal operational reports — while **Integration Hub**, **Foundation**, **Document Management**, and **Analytics** remain Systems of Record for their domains.

Developer Portal stores **portal operational metadata only**. Peer bindings use **UUID / service contracts only** — **no peer ORM**. FastAPI remains the OpenAPI generator. Document Management remains document SoR. Integration Hub remains OAuth / credential / gateway / usage metering SoR. Try-it and sandbox are metadata-only (no live invoke / no runtime provisioning).

**API Developer Portal backend is completed.**

---

## 3. Reference Documents

| Document | Role |
|----------|------|
| BRD v1.0 | Business requirements baseline |
| SDD v1.1 | Solution design baseline |
| DBS v1.1 | Database standards baseline |
| Architecture Lock v1.1 | Architecture baseline (locked) |
| FRD-28 Locked v1.1 | Functional requirements (locked) |
| ERD-28 Entity Planning Locked v1.1 | Entity planning (locked) |
| ERD-28 Detailed ERD Locked v1.1 | Detailed ERD (locked) |
| Sprint 28 Backend Planning Locked v1.1 | Backend planning (locked) |
| Sprint 28 Phase 0–4 Completion Reports | Phase delivery records |
| Sprint 28 Validation Report | Quality-gate validation (**PASS**) |

Engineering reports are archived under `docs/08_SPRINT_REPORTS/Sprint_28/`.

---

## 4. Sprint Coverage

| Attribute | Value |
|-----------|--------|
| **Sprint** | Sprint 28 |
| **Domain** | API Developer Portal |
| **Phases** | Phase 0 · Phase 1 · Phase 2 · Phase 3 · Phase 4 |
| **Module** | `apps/api/src/modules/devportal/` |
| **Schema / Prefix** | `devportal` / `dp_` |
| **Business Tables** | **18 of 18** (ERD-28 complete) |
| **API Mount** | `/api/v1/devportal` |
| **Alembic Head** | `0581_seed_devportal_phase4_permissions` |
| **Devportal Tests** | **66 passed** |
| **Sprint Validation** | **PASS** |

| Phase | Scope | Outcome |
|-------|--------|---------|
| **Phase 0** | Devportal schema shell · module scaffold · Alembic bootstrap · Clean Architecture package skeleton | Complete — 0 / 18 entities (foundation only) |
| **Phase 1** | Developer identity · application · API product catalog | Complete — **10 / 18** |
| **Phase 2** | Plans · subscriptions · entitlements | Complete — **13 / 18** |
| **Phase 3** | Documentation · OpenAPI artifact refs · sandbox · try-it | Complete — **17 / 18** |
| **Phase 4** | Portal report · hardening · permission seed close | Complete — **18 / 18** |

### Phase Summaries

| Phase | Summary |
|-------|---------|
| **Phase 0** | Established the `devportal` schema shell, module package layout (domain · routers · service · repository · models · adapters), and migration chain start. No business entities. Architecture Lock preserved. |
| **Phase 1** | Delivered Developer Identity, Application Registration, and API Product Catalog metadata (10 tables). Hub OAuth/credential bindings are UUID attributes only. |
| **Phase 2** | Delivered Access Governance metadata (3 tables) — plan · subscription · entitlement. Entitlements are metadata only; Gateway remains enforcement owner. |
| **Phase 3** | Delivered Documentation Catalog and Sandbox Experience metadata (4 tables). Guides/tutorials/changelog/release_notes via `entry_type`. OpenAPI artifact refs store Document UUID + snapshot metadata only. Sandbox/try-it are metadata-only — **no K8s provisioning · no live API invoke**. |
| **Phase 4** | Delivered Portal Report operational metadata (1 table). Report definition / filters / config / export preferences / schedule metadata. Hub usage projected via adapter — Hub remains metering SoR. Analytics remains enterprise reporting SoR. |

---

## 5. Architecture Summary

| Principle | Confirmation |
|-----------|--------------|
| **Architecture Lock v1.1** | **Preserved** — no Architecture Lock changes |
| **Modular Monolith** | New `modules/devportal` package; no service-boundary redesign |
| **DDD** | Devportal domain enums, exceptions, entities, engines |
| **Clean Architecture** | Router → Service → Engine → Repository → Model maintained |
| **UUID-only references** | Confirmed — peer refs (`oauth_client_id`, `api_credential_id`, `document_id`, `workflow_instance_id`, `analytics_report_id`) only |
| **No peer ORM** | Confirmed — Developer Portal never writes peer-module ORM models |
| **Developer Portal owns portal metadata only** | Confirmed — not Integration Hub, Foundation IAM, Document, Analytics SoR |
| **FastAPI remains OpenAPI generator** | Confirmed |
| **Document Management remains document SoR** | Confirmed |
| **Integration Hub remains gateway / OAuth / usage SoR** | Confirmed |
| **FRD-28 / ERD-28** | **Locked and implemented** (backend table scope) |
| **Previous modules** | Unchanged except required Devportal wiring (router / Alembic / permissions) |

Stack unchanged: FastAPI · SQLAlchemy 2.0 · Alembic · PostgreSQL · Redis · Celery · Next.js (Developer Portal frontend deferred).

---

## 6. Ownership Boundaries

### Developer Portal owns only

| Ownership | Examples |
|-----------|----------|
| Developer identity metadata | Organization · team · account · membership · invite · portal session |
| Application registration metadata | Application · Hub OAuth/credential **UUID** bindings |
| API product catalog metadata | Product · version · environment binding metadata |
| Access governance metadata | Plan · subscription · entitlement (metadata only) |
| Documentation catalog metadata | Documentation entry · OpenAPI artifact **reference** |
| Sandbox experience metadata | Sandbox environment · try-it session (non-gateway) |
| Portal operations metadata | Portal report definitions · export preferences · Hub usage **projection** |

### Developer Portal does NOT own

| Concern | Owner |
|---------|--------|
| Authentication · Authorization · RBAC · JWT · users | Foundation |
| Workflow engine / approvals warehouse | Foundation Workflow |
| Enterprise audit warehouse | Foundation Audit |
| OAuth clients · API credentials · secrets | Integration Hub |
| Gateway routing / runtime enforcement / rate limits | Integration Hub |
| API usage metering SoR | Integration Hub |
| Document file storage / binary documents | Document Management |
| OpenAPI generation | FastAPI platform |
| Analytics warehouse / BI / ETL / aggregations | Analytics |
| Customer / Vendor self-service portals | Customer Portal / Vendor Portal |
| AI intelligence metadata | AI Platform |

---

## 7. Major Deliverables

| Capability | Delivery |
|------------|----------|
| **Devportal Module** | `apps/api/src/modules/devportal/` — Clean Architecture package |
| **Developer Identity** | Organization · Team · Account · Membership · Invite · Portal Session |
| **Application Registration** | Application (+ Hub UUID bind validation via adapter) |
| **API Product Catalog** | API Product · Product Version · Product Environment |
| **Access Governance** | Plan · Subscription · Entitlement |
| **Documentation Catalog** | Documentation Entry · OpenAPI Artifact Reference |
| **Sandbox Experience** | Sandbox Environment · Try-it Session |
| **Portal Operations** | Portal Report (Hub usage projection via contract) |
| **Application Facade** | `DevportalApplicationService` wires phase services |

**Supporting delivered items:** `devportal.*` RBAC roles/permissions (Phase 1–4 seeds), Foundation Audit for entity change logging, publish/lifecycle validation engines, Integration Hub / Document / Analytics / Foundation adapters (UUID / contract only).

### 7.1 Entity Inventory (18 / 18)

#### Developer Identity (6)

| Table | Capability |
|-------|------------|
| `dp_developer_organization` | Developer organization registry |
| `dp_developer_team` | Team under organization |
| `dp_developer_account` | Developer account lifecycle |
| `dp_developer_membership` | Org/team membership |
| `dp_developer_invite` | Invite lifecycle |
| `dp_portal_session` | Portal session metadata |

#### Application Registration (1)

| Table | Capability |
|-------|------------|
| `dp_application` | Application registration · Hub OAuth/credential UUID bindings |

#### API Product Catalog (3)

| Table | Capability |
|-------|------------|
| `dp_api_product` | API product identity |
| `dp_api_product_version` | Version spine · publish / retire |
| `dp_api_product_environment` | Environment binding metadata (not gateway) |

#### Access Governance (3)

| Table | Capability |
|-------|------------|
| `dp_plan` | Plan offering · publish / retire |
| `dp_subscription` | Application ↔ Product Version ↔ Plan binding |
| `dp_entitlement` | Scope metadata under subscription — **no runtime enforcement** |

#### Documentation Catalog (2)

| Table | Capability |
|-------|------------|
| `dp_documentation_entry` | Guides · tutorials · changelog · release notes (`entry_type`) |
| `dp_openapi_artifact_reference` | Document UUID + version/snapshot metadata — **no binary · no generation** |

#### Sandbox Experience (2)

| Table | Capability |
|-------|------------|
| `dp_sandbox_environment` | Sandbox **metadata only** — no runtime provisioning |
| `dp_tryit_session` | Try-it **metadata only** — no live invoke / forwarding |

#### Portal Operations (1)

| Table | Capability |
|-------|------------|
| `dp_portal_report` | Operational report definition metadata · Hub usage projection via adapter |

**Total: 18 entities.**

---

## 8. Security Summary

| Control | Confirmation |
|---------|--------------|
| **RBAC** | `devportal.*` permissions (**146**) across **18** resources; roles seeded Phase 1–4 |
| **Export** | `devportal.report:read` / `:export` aligned to FR-28-016 |
| **Tenant isolation** | Tenant-/company-scoped repositories; no cross-tenant leakage by design |
| **Secrets** | No portal secret columns; Hub UUID refs only |
| **Gateway / invoke** | No gateway invoke · no try-it live call · fail-closed where applicable |
| **Audit ownership** | Foundation Audit remains the enterprise audit warehouse; portal emits change events — does not own audit SoR |

---

## 9. Validation Summary

| Gate | Result |
|------|--------|
| **Validation Gate** | Sprint 28 Validation Report — **PASS** |
| **Validation Fix** | **Not required** |
| **Final Result** | **PASS** |

| Check | Status |
|-------|--------|
| Alembic Head | **PASS** — `0581_seed_devportal_phase4_permissions` |
| FastAPI Startup | **PASS** |
| Swagger `/docs` | **PASS** |
| OpenAPI | **PASS** — **117** `/api/v1/devportal/*` paths · **18** resource prefixes |
| Devportal Router Registration | **PASS** |
| Ruff | **PASS** |
| MyPy | **PASS** |
| Pytest | **PASS** — **66** (devportal unit · security · integration) |
| Architecture Validation | **PASS** |
| Sprint 28 Final Validation | **PASS** |

---

## 10. Implementation Statistics

| Field | Value |
|-------|--------|
| **Sprint** | 28 |
| **Module** | API Developer Portal |
| **Entities / Tables** | **18** |
| **Devportal Routes** | **153** |
| **Devportal OpenAPI Paths** | **117** |
| **Tests** | **66 passed** |
| **Validation** | **PASS** |
| **Alembic Head** | `0581_seed_devportal_phase4_permissions` |
| **Permissions** | **146** `devportal.*` |
| **Ruff** | **PASS** |
| **MyPy** | **PASS** |
| **Architecture Lock** | Preserved |
| **FRD-28** | Preserved |
| **ERD-28** | Preserved |

---

## 11. API Summary

| Metric | Value |
|-------:|
| **Devportal Route Count** | **153** |
| **Devportal OpenAPI Paths** | **117** |

**Mount:** `/api/v1/devportal`

Covered resource groups: organizations · teams · accounts · memberships · invites · sessions · applications · api-products · api-product-versions · api-product-environments · plans · subscriptions · entitlements · documentation-entries · openapi-artifact-references · sandbox-environments · tryit-sessions · reports.

Swagger (`/docs`) and OpenAPI (`/openapi.json`) register Developer Portal APIs under `/api/v1/devportal/*`.

**Forbidden surfaces (by design):** Gateway invoke/enforce · OpenAPI generation takeover · binary document storage · sandbox K8s provisioning · try-it live forwarding · Analytics warehouse / BI / ETL · Hub secret materialization.

---

## 12. Database Summary

| Item | Value |
|------|--------|
| **New Schema** | `devportal` |
| **Devportal Business Tables** | **18** |
| **Alembic Head** | `0581_seed_devportal_phase4_permissions` |
| **Migration range (this release delta)** | `0559_create_devportal_schema` → `0581_seed_devportal_phase4_permissions` |
| **Prior head (v1.22-beta)** | `0558_seed_ai_phase4_permissions` |

```text
0558_seed_ai_phase4_permissions
        ↓
0559_create_devportal_schema
        ↓
… Sprint 28 Phase 0–4 migrations …
        ↓
0581_seed_devportal_phase4_permissions
```

---

## 13. Alembic

| Check | Result |
|-------|--------|
| **Current Head** | `0581_seed_devportal_phase4_permissions` |
| **Head Count** | 1 (single head) |
| **Chain** | Continuous `0559` → `0581` (Sprint 28 revisions · **23**) |
| **Status** | **PASS** |

---

## 14. Known Deferred Work

Only items already documented in Sprint 28 locked planning and completion reports. No new deferred work invented.

| Item | Notes |
|------|--------|
| **Frontend / Developer Portal UI** | Deferred unless separately authorized |
| **Live try-it / gateway invoke** | Explicitly out of ownership — Hub / gateway runtime |
| **Sandbox runtime / Kubernetes provisioning** | Explicitly out of ownership — metadata only |
| **OpenAPI generation ownership** | Remains FastAPI platform |
| **Binary document storage** | Remains Document Management |
| **Usage metering SoR / rate-limit enforcement** | Remains Integration Hub |
| **Analytics warehouse / BI / ETL** | Remains Analytics |
| **Billing / payment processing** | Out of Sprint 28 scope |

---

## 15. Release Readiness

| Deliverable | Confirmation |
|-------------|--------------|
| ERD-28 business tables | **18 / 18 complete** |
| Tests | **66 passed** |
| Ruff | **PASS** |
| MyPy | **PASS** |
| Validation | **PASS** |
| Single Alembic head | **PASS** |
| OpenAPI | **PASS** |
| Architecture Lock v1.1 | **Preserved** |
| FRD-28 | **Preserved** |
| ERD-28 | **Preserved** |
| Backend | **Complete** |
| Frontend / live gateway-tryit runtimes | Deferred (already documented) |

**Sprint 28 backend is production-ready from an architecture perspective**, subject to future UI / runtime integrations already documented in Backend Planning Locked v1.1 and Phase completion reports.

---

## 16. Related Documents

| Document | Location / Role |
|----------|-----------------|
| **BRD** | BRD v1.0 |
| **SDD** | SDD v1.1 |
| **DBS** | DBS v1.1 |
| **Architecture Lock** | Architecture Lock v1.1 |
| **FRD** | FRD-28 Locked v1.1 |
| **ERD** | ERD-28 Entity Planning Locked v1.1 · ERD-28 Detailed ERD Locked v1.1 |
| **Backend Planning** | Sprint 28 Backend Planning Locked v1.1 |
| **Validation** | Sprint 28 Validation Report (**PASS**) |
| **Phase Reports** | Sprint 28 Phase 0–4 Completion Reports |

---

## 17. Release Summary

| Item | Confirmation |
|------|----------------|
| Release document | `docs/07_RELEASES/ERP_Core_v1.23-beta.md` |
| Prior releases unmodified | `ERP_Core_v1.0-alpha.md` · `v1.1-beta` … · `v1.22-beta` unchanged |
| **Version** | **ERP Core v1.23-beta** |
| **Status** | **Release Ready** |
| **Release Date** | **TBD** |
| **Modules** | Foundation · Organization · Master Data · Finance · Sales · Procurement · Inventory · Manufacturing · Quality · CRM · HR · Payroll · Recruitment · Project · Asset · Service · Helpdesk · Document · GRC · Analytics · Integration · E-Commerce · Customer Portal · Vendor Portal · Workflow & BPM Designer · Low-Code Platform · Enterprise AI Platform · **API Developer Portal** |
| **Alembic head** | **`0581_seed_devportal_phase4_permissions`** |
| **Devportal tables** | **18 / 18** |
| **Devportal tests** | **66 passed** |
| **Routes** | **153** Devportal · **117** Devportal OpenAPI paths |
| **Quality gates** | Ruff · MyPy · Pytest · Architecture · Alembic · OpenAPI — **PASS** |
| **Ready for Git Tag** | **`v1.23-beta`** |

---

## 18. Version Timeline

| Version | Date | Scope | Alembic Head | Tests |
|---------|------|--------|--------------|-------|
| **v1.21-beta** | 2026-07-22 | Sprints 0–26 (+ Low-Code Platform) | `0519_seed_lowcode_phase4_permissions` | **90 Low-Code passed** |
| **v1.22-beta** | TBD | Sprints 0–27 (+ Enterprise AI Platform) | `0558_seed_ai_phase4_permissions` | **79 AI passed** |
| **v1.23-beta** | TBD | Sprints 0–28 (+ API Developer Portal) | `0581_seed_devportal_phase4_permissions` | **66 Devportal passed** |

```text
v1.22-beta ──(+ Sprint 28 API Developer Portal)──► v1.23-beta
```

---

## 19. Closing Statement

ERP Core v1.23-beta delivers the complete backend implementation of the API Developer Portal while preserving Architecture Lock v1.1 and enterprise ownership boundaries.

Sprint 28 is fully completed, validated, documented, and archived.

**API Developer Portal Backend is officially complete.**

**Architecture Lock preserved.**

---

## Archive Note

Sprint 28 engineering reports are archived under:

`docs/08_SPRINT_REPORTS/Sprint_28/`

Release Notes remain the official customer-facing release documentation in `docs/07_RELEASES/`.

---

## Validation Checklist (Release Documentation)

| Check | Result |
|-------|--------|
| ✓ Only release note created | Confirmed |
| ✓ No implementation modified | Confirmed |
| ✓ No migrations modified | Confirmed |
| ✓ No APIs modified | Confirmed |
| ✓ No locked documents modified | Confirmed |
| ✓ Architecture Lock referenced | Confirmed — v1.1 Preserved |
| ✓ Sprint 28 statistics included | Confirmed — 18 entities · Alembic `0581` · 66 tests · 153 routes · 117 OpenAPI paths |
| ✓ Ownership preserved | Confirmed — Hub / Foundation / Document / Analytics SoR · Portal metadata only |
| ✓ Validation PASS referenced | Confirmed — Sprint 28 Validation Report |
