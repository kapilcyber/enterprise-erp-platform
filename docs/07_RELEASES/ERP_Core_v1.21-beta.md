# ERP Core v1.21-beta — Release Notes

| Field | Value |
|-------|--------|
| **Document Type** | Enterprise Release Notes |
| **Release Name** | ERP Core v1.21-beta |
| **Release Status** | Release Ready |
| **Architecture Lock** | v1.1 — Maintained |
| **Prepared As** | Enterprise Solution Architect · ERP Product Architect · Technical Documentation Lead · Release Manager · Principal Software Engineer |
| **Classification** | Internal — Confidential |
| **Predecessor** | [ERP Core v1.20-beta](./ERP_Core_v1.20-beta.md) |
| **Primary Deliverable** | Sprint 26 — Low-Code Platform |

---

## 1. Release Overview

| Field | Value |
|-------|--------|
| **Version** | ERP Core v1.21-beta |
| **Status** | Release Ready |
| **Date** | 2026-07-22 |
| **Previous Release** | ERP Core v1.20-beta |
| **Sprint Delivered** | Sprint 26 — Low-Code Platform |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-26 Locked v1.1 · ERD-26 Entity Planning Locked v1.1 · ERD-26 Locked v1.1 |
| **Recommended Git Tag** | `v1.21-beta` |

Sprint 26 delivered the **Low-Code Platform** backend as the enterprise design-time metadata foundation for dynamic forms and pages — form category → definition → version → sections / fields → component library → data sources / expressions / bindings → event handlers / localization → page definition / version / regions → publish history / runtime submission correlation / preview sessions — while **business modules remain Systems of Record**. Low-Code stores **design and operational metadata only**. Peer bindings use **UUID / services only** — **no peer ORM writes**. Preview never mutates business data. Runtime submission is a correlation envelope only. Publish history complements Foundation Audit and does not replace it.

---

## 2. Reference Documents

| Document | Role |
|----------|------|
| FRD-26 Locked v1.1 | Functional requirements (locked) |
| ERD-26 Entity Planning Locked v1.1 | Entity planning (locked) |
| ERD-26 Detailed Locked v1.1 | Detailed ERD (locked) |
| Architecture Lock v1.1 | Architecture baseline (locked) |
| Sprint 26 Completion Report | Engineering completion record |
| Sprint 26 Validation Report | Quality-gate validation |
| Sprint 26 Validation Fix Report | Ruff / MyPy remediation confirmation |
| Sprint 26 Phase 1–4 Completion Reports | Phase delivery records |

Engineering reports are archived under `docs/08_SPRINT_REPORTS/Sprint_26/`.

---

## 3. Sprint Summary

| Attribute | Value |
|-----------|--------|
| **Sprint** | Sprint 26 |
| **Domain** | Low-Code Platform |
| **Phases** | Phase 1 · Phase 2A · Phase 2B · Phase 2C · Phase 3A · Phase 3B · Phase 4 |
| **Module** | `apps/api/src/modules/lowcode/` |
| **Schema / Prefix** | `lowcode` / `lc_` |
| **Business Tables** | **18 of 18** (ERD-26 complete) |
| **API Mount** | `/api/v1/lowcode` |
| **Alembic Head** | `0519_seed_lowcode_phase4_permissions` |
| **Low-Code Tests** | **90 passed** |
| **Sprint Validation** | **PASS** |

| Phase | Scope | Outcome |
|-------|--------|---------|
| Phase 1 | Form Category · Form Definition · Form Version | Complete |
| Phase 2A | Form Sections · Form Fields | Complete |
| Phase 2B | Component Library (component · component version) | Complete |
| Phase 2C | Data Sources · Expressions · Expression Bindings | Complete |
| Phase 3A | Event Handlers · Localization | Complete |
| Phase 3B | Page Builder Metadata (page definition · version · region) | Complete |
| Phase 4 | Publish History · Runtime Submission · Preview Session | Complete |

---

## 4. Architecture Status

| Principle | Confirmation |
|-----------|--------------|
| **Architecture Lock v1.1** | **Preserved** — no Architecture Lock changes |
| **FRD-26 / ERD-26** | **Locked and implemented** (backend table scope) |
| **Clean Architecture** | Router → Service → Repository → Database maintained |
| **DDD** | Low-Code domain enums, exceptions, entities, engines |
| **Modular Monolith** | New `modules/lowcode` package; no service-boundary redesign |
| **No duplicate masters** | Confirmed |
| **No peer ORM writes** | Confirmed — UUID refs only for business SoR / BPM task |
| **Published immutability** | Confirmed — Draft editable · Published immutable · Retired read-only |
| **Append-oriented publish history** | Confirmed — complements Foundation Audit |
| **Previous modules** | Unchanged except required Low-Code wiring (router / Alembic / permissions) |

Stack unchanged: FastAPI · SQLAlchemy 2.0 · Alembic · PostgreSQL · Redis · Celery · Next.js (Low-Code frontend deferred).

---

## 5. Ownership Boundaries

### Low-Code owns only

| Ownership | Examples |
|-----------|----------|
| Design metadata | Forms · sections · fields · components · expressions · events · localization · pages · regions |
| Publish history | Append-oriented publish / retire trail (actor · timestamp · reason · version transition) |
| Preview sessions | Design-time draft / published preview metadata · sample context · expiration |
| Runtime submission correlation | Published form/page UUID · `module_code` · `entity_id` · optional `bpm_task_id` · status · correlation id |

### Low-Code does NOT own

| Concern | Owner |
|---------|--------|
| Business transactions / System of Record | Business modules |
| Workflow engine | Foundation Workflow / BPM |
| Notification delivery | Foundation Notification |
| Enterprise audit warehouse | Foundation Audit |
| Document storage | Document Management |
| Rendering engine / runtime UI rendering | Future Low-Code Runtime / UI (deferred) |
| Transport | Integration Hub |

---

## 6. Major Highlights

| Capability | Delivery |
|------------|----------|
| **Low-Code Module** | `apps/api/src/modules/lowcode/` — Clean Architecture package |
| **Form Design Spine** | Category · Definition · Version (Draft / Publish / Retire / Clone) |
| **Form Structure** | Sections · Fields |
| **Component Library** | Component · Component Version |
| **Data & Logic Metadata** | Data Source registry · Expression · Expression Binding |
| **Events & Localization** | Event Handler · Localization Entry |
| **Page Builder Metadata** | Page Definition · Page Version · Page Region |
| **Operational Metadata** | Publish History · Runtime Submission · Preview Session |
| **Application Facade** | `LowcodeApplicationService` wires phase services |

**Supporting delivered items:** Low-Code document numbering (`FC-` / `FRM-` / `FVER-` / `SEC-` / `FLD-` / `CMP-` / `CVER-` / `DS-` / `EXP-` / `EXB-` / `EVT-` / `LOC-` / `PG-` / `PVER-` / `PREG-` / `PH-` / `RSUB-` / `PREV-`), RBAC roles (`LOWCODE_ADMIN`, `FORM_DESIGNER`, `FORM_PUBLISHER`, `LOWCODE_AUDITOR`), and Foundation Audit for entity change logging.

---

## 7. Low-Code Platform

| Item | Value |
|------|--------|
| **Schema** | `lowcode` |
| **Prefix** | `lc_` |
| **Business Tables** | **18** |
| **ERD** | ERD-26 Low-Code Platform (locked) |
| **FRD** | FRD-26 Low-Code Platform Domain (locked) |
| **API mount** | `/api/v1/lowcode` |

**Tables:** `lc_form_category`, `lc_form_definition`, `lc_form_version`, `lc_form_section`, `lc_form_field`, `lc_component`, `lc_component_version`, `lc_data_source`, `lc_expression`, `lc_expression_binding`, `lc_event_handler`, `lc_localization_entry`, `lc_page_definition`, `lc_page_version`, `lc_page_region`, `lc_publish_history`, `lc_runtime_submission`, `lc_preview_session`.

### 7.1 Phase 1 — Form Design Spine

| Table | Capability |
|-------|------------|
| `lc_form_category` | Category CRUD · archive / restore |
| `lc_form_definition` | Stable form identity · archive / restore · seed Draft v1 |
| `lc_form_version` | Draft · Publish · Retire · Clone · validate-publish · **one Published version per Definition** |

### 7.2 Phase 2A — Form Structure

| Table | Capability |
|-------|------------|
| `lc_form_section` | Section metadata · display order · draft version gate |
| `lc_form_field` | Field metadata · field key uniqueness · component / data-source UUID refs |

### 7.3 Phase 2B — Component Library

| Table | Capability |
|-------|------------|
| `lc_component` | Component catalog · archive / restore |
| `lc_component_version` | Draft · Publish · Retire · Clone · property metadata |

### 7.4 Phase 2C — Data & Logic

| Table | Capability |
|-------|------------|
| `lc_data_source` | Registry only · module contract references (C-01 / C-02) — modules own data |
| `lc_expression` | Expression metadata · publish / retire |
| `lc_expression_binding` | Binding metadata to form / section / field targets |

### 7.5 Phase 3A — Events & Localization

| Table | Capability |
|-------|------------|
| `lc_event_handler` | Event handler metadata only — **no execution** |
| `lc_localization_entry` | Locale / key / translated value metadata · publish / retire |

### 7.6 Phase 3B — Page Builder Metadata

| Table | Capability |
|-------|------------|
| `lc_page_definition` | Stable page identity · archive / restore · seed Draft v1 |
| `lc_page_version` | Draft · Publish · Retire · Clone · **one Published version per Definition** |
| `lc_page_region` | Region types · layout JSON · embedded form/component UUID refs |

### 7.7 Phase 4 — Operational Metadata

| Table | Capability |
|-------|------------|
| `lc_publish_history` | Append-oriented publish / retire trail · actor · timestamp · reason |
| `lc_runtime_submission` | Correlation envelope only · Published versions · `module_code` + `entity_id` |
| `lc_preview_session` | Design-time draft / published preview · TTL · close / expire — **no business mutation** |

---

## 8. API Summary

| Metric | Value |
|-------:|
| **Low-Code Route Count** | **110** |
| **Low-Code OpenAPI Paths** | **74** |
| **Low-Code OpenAPI Operations** | **110** |
| **Platform FastAPI Routes** | **1981** |
| **Platform OpenAPI Paths** | **1239** |
| **Platform OpenAPI Operations** | **1977** |

**Mount:** `/api/v1/lowcode`

Covered resource groups: categories · definitions · versions · sections · fields · structure · components · component-versions · data-sources · expressions · expression-bindings · event-handlers · localization-entries · pages · page-versions · page-regions · publish-history · runtime-submissions · preview-sessions.

Swagger (`/docs`) and OpenAPI (`/openapi.json`) register Low-Code APIs under `/api/v1/lowcode/*`.

---

## 9. Database Summary

| Item | Value |
|------|--------|
| **New Schema** | `lowcode` |
| **Low-Code Business Tables** | **18** |
| **Alembic Head** | `0519_seed_lowcode_phase4_permissions` |
| **Migration range (this release delta)** | `0492_create_lowcode_schema` → `0519_seed_lowcode_phase4_permissions` |
| **Prior head (v1.20-beta)** | `0491_seed_bpm_phase5_permissions` |

```text
0491_seed_bpm_phase5_permissions
        ↓
0492_create_lowcode_schema
        ↓
… Sprint 26 Phase 1–4 migrations …
        ↓
0519_seed_lowcode_phase4_permissions
```

---

## 10. Alembic

| Check | Result |
|-------|--------|
| **Current Head** | `0519_seed_lowcode_phase4_permissions` |
| **Head Count** | 1 (single head) |
| **Chain** | Continuous `0492` → `0519` (28 Sprint 26 revisions) |
| **Status** | **PASS** |

---

## 11. OpenAPI

| Check | Result |
|-------|--------|
| OpenAPI generation | **PASS** |
| Swagger `/docs` | **PASS** |
| Low-Code paths registered | **74** |
| Low-Code operations | **110** |
| Platform OpenAPI paths | **1239** |

---

## 12. Release Statistics

| Field | Value |
|-------|--------|
| **Sprint** | 26 |
| **Module** | Low-Code Platform |
| **Tables** | **18** |
| **Routes** | **110** |
| **OpenAPI Paths** | **74** |
| **OpenAPI Operations** | **110** |
| **Tests** | **90** |
| **Validation** | **PASS** |
| **Alembic Head** | `0519_seed_lowcode_phase4_permissions` |
| **Ruff** | **PASS** |
| **MyPy** | **PASS** |
| **Architecture Lock** | Preserved |
| **FRD-26** | Preserved |
| **ERD-26** | Preserved |

---

## 13. Quality Gates

| Gate | Status |
|------|--------|
| Alembic Head | **PASS** — `0519_seed_lowcode_phase4_permissions` |
| FastAPI Startup | **PASS** |
| Swagger `/docs` | **PASS** |
| OpenAPI | **PASS** |
| Low-Code Router Registration | **PASS** |
| Ruff | **PASS** |
| MyPy | **PASS** |
| Pytest | **PASS** — **90** (Low-Code unit · security · integration) |
| Architecture Validation | **PASS** |
| Sprint 26 Final Validation | **PASS** |

---

## 14. Known Deferred Work

| Item | Notes |
|------|--------|
| **Rendering Engine** | Not in this release — metadata ownership only |
| **Frontend Form Designer** | Deferred |
| **Frontend Page Builder** | Deferred |
| **Runtime Rendering** | Deferred |
| **Publish Validation enhancements** | Structure validation integration into form publish (future) |
| **Version Clone enhancements** | Deep-copy form sections/fields with new UUIDs (future) |

---

## 15. Implementation Summary

| Deliverable | Confirmation |
|-------------|--------------|
| ERD-26 business tables | **18 / 18 complete** |
| Tests | **90 passed** |
| Ruff | **PASS** |
| MyPy | **PASS** |
| Validation | **PASS** |
| Single Alembic head | **PASS** |
| OpenAPI | **PASS** |
| Architecture Lock v1.1 | **Preserved** |
| FRD-26 | **Preserved** |
| ERD-26 | **Preserved** |
| Backend | **Complete** |
| Frontend | Deferred |

---

## 16. Release Summary

| Item | Confirmation |
|------|----------------|
| Release document | `docs/07_RELEASES/ERP_Core_v1.21-beta.md` |
| Prior releases unmodified | `ERP_Core_v1.0-alpha.md` · `v1.1-beta` … · `v1.20-beta` unchanged |
| **Version** | **ERP Core v1.21-beta** |
| **Status** | **Release Ready** |
| **Modules** | Foundation · Organization · Master Data · Finance · Sales · Procurement · Inventory · Manufacturing · Quality · CRM · HR · Payroll · Recruitment · Project · Asset · Service · Helpdesk · Document · GRC · Analytics · Integration · E-Commerce · Customer Portal · Vendor Portal · Workflow & BPM Designer · **Low-Code Platform** |
| **Alembic head** | **`0519_seed_lowcode_phase4_permissions`** |
| **Low-Code tables** | **18 / 18** |
| **Low-Code tests** | **90 passed** |
| **Routes** | **1981** FastAPI · **1239** OpenAPI · **110** Low-Code |
| **Quality gates** | Ruff · MyPy · Pytest · Architecture · Alembic · OpenAPI — **PASS** |
| **Ready for Git Tag** | **`v1.21-beta`** |

---

## 17. Version Timeline

| Version | Date | Scope | Alembic Head | Tests |
|---------|------|--------|--------------|-------|
| **v1.19-beta** | 2026-07-20 | Sprints 0–24 (+ Supplier / Vendor Portal) | `0464_seed_vp_workflows` | Vendor Portal hub + suite |
| **v1.20-beta** | 2026-07-22 | Sprints 0–25 (+ Workflow & BPM Designer) | `0491_seed_bpm_phase5_permissions` | **136 BPM passed** |
| **v1.21-beta** | 2026-07-22 | Sprints 0–26 (+ Low-Code Platform) | `0519_seed_lowcode_phase4_permissions` | **90 Low-Code passed** |

```text
v1.20-beta ──(+ Sprint 26 Low-Code Platform)──► v1.21-beta
```

---

## 18. Closing Statement

ERP Core v1.21-beta delivers the complete backend implementation of the Low-Code Platform while preserving Architecture Lock v1.1 and enterprise ownership boundaries.

Sprint 26 is fully completed, validated, documented, and archived.

**Low-Code Backend is officially complete (18 / 18).**

---

## Archive Note

Sprint 26 engineering reports are archived under:

`docs/08_SPRINT_REPORTS/Sprint_26/`

Release Notes remain the official customer-facing release documentation in `docs/07_RELEASES/`.
