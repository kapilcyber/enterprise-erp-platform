# Implementation Governance

## Multi-Industry Enterprise ERP Platform

---

| Field | Value |
|-------|--------|
| **Document Title** | Implementation Governance |
| **Document ID** | IG-01 |
| **Filename (canonical)** | `Implementation_Governance_v1.0.md` |
| **Version** | **1.0** |
| **Status** | **Review Candidate (RC)** |
| **Document Status** | **Review Candidate (RC) — Not Locked** |
| **Classification** | Internal — Confidential |
| **Authority** | Permanent Enterprise Architecture Review Board (PEARB) |
| **Effective Date (proposed)** | 2026-07-29 |
| **Scope** | Permanent implementation policy for Phase 0 through Release, including coding, layering, repository conventions, API/database/security/testing rules, STOP criteria, audits, and quality gates |
| **Parent Governance** | `Enterprise_Master_Governance_v1.0.md` |
| **Board Charter** | `Enterprise_Architecture_Review_Board_v1.0.md` |
| **Repository Governance** | `Repository_Governance_v1.0.md` |
| **Documentation Governance** | `Documentation_Governance_v1.0.md` |
| **Architecture Baseline** | Architecture Lock Report v1.1 |
| **Official Historical Baseline** | Sprint 1 through Sprint 28 (complete) |
| **Current Delivery Context** | Sprint 29 and all subsequent sprints |
| **Repository Location** | `docs/05_ARCHITECTURE_LOCK/Governance/` |
| **Supersedes** | None (first official Implementation Governance) |
| **Does Not Replace** | Enterprise Master Governance · PEARB Charter · Repository Governance · Documentation Governance · Architecture Lock v1.1 · BRD · FRD · SDD · DBS · ERD · Backend Planning · Sprint artifacts |

> **Implementation governance only.** This document defines **how implementation must be executed** from Phase 0 through Release while preserving Architecture Lock, Repository Governance, and Documentation Governance. It does **not** replace Architecture Lock, Repository Governance, Documentation Governance, or the PEARB Charter. It does **not** implement code and does **not** authorize architecture redesign.

---

### Document Control

| Role | Responsibility |
|------|----------------|
| **PEARB** | Author, custodian, and sole amendatory authority |
| **Principal Solution Architect** | End-to-end phase fitness and solution integrity |
| **Platform Architect** | Repository convention / module scaffold enforcement |
| **Enterprise Domain Architect** | FRD/ERD fidelity during implementation |
| **Database Architect** | Models · migrations · DBS compliance |
| **Security Architect** | RBAC · tenancy · secrets · security tests |
| **Quality Assurance Architect** | Testing · Validation evidence · quality gates |
| **Delivery Teams / Agents / Vendors** | Mandatory adherence |

### Version History

| Version | Date | Change | Authority |
|---------|------|--------|-----------|
| **1.0** | 2026-07-29 | Initial Implementation Governance (Review Candidate). Defines implementation principles, Phase 0–4 governance, Clean Architecture/DDD/coding rules, repository package conventions, API/database/security/DI/tasks/testing/performance rules, STOP criteria, audits, and quality gates. Complies with Master Governance, PEARB Charter, Repository Governance, Documentation Governance, Architecture Lock v1.1, and Sprint 1–28 baseline. Does not lock; does not authorize implementation by publication. | PEARB — Review Candidate |

### Document Hierarchy

```text
1. Enterprise Master Governance v1.0
2. Architecture Lock v1.1 (+ locked ADRs)
3. Enterprise Architecture Review Board Charter v1.0
4. Repository Governance v1.0
5. Documentation Governance v1.0
6. Implementation Governance v1.0 (this document)
7. BRD · SDD · DBS
8. Sprint ARB Recommendation → FRD → ERD → Backend Planning (Locked)
9. Phase / Validation / Release / Completion artifacts
10. Source code and migrations (must conform upward)
```

This document **shall not** contradict parent governance. Locked Backend Planning remains the sprint implementation planning baseline, subject to Repository First / Implementation Convention Precedence for package/file layout.

---

## Table of Contents

1. [Cover Page and Metadata](#1-cover-page-and-metadata)  
2. [Purpose](#2-purpose)  
3. [Scope](#3-scope)  
4. [Implementation Principles](#4-implementation-principles)  
5. [Phase Governance (Phase 0–4)](#5-phase-governance-phase-04)  
6. [Coding Governance](#6-coding-governance)  
7. [Clean Architecture Governance](#7-clean-architecture-governance)  
8. [DDD Governance](#8-ddd-governance)  
9. [Repository Implementation Rules](#9-repository-implementation-rules)  
10. [API Implementation Rules](#10-api-implementation-rules)  
11. [Database Implementation Rules](#11-database-implementation-rules)  
12. [Security Implementation Rules](#12-security-implementation-rules)  
13. [Dependency Injection Governance](#13-dependency-injection-governance)  
14. [Background Task Governance](#14-background-task-governance)  
15. [Testing Governance](#15-testing-governance)  
16. [Performance Governance](#16-performance-governance)  
17. [Exception Management](#17-exception-management)  
18. [STOP Criteria](#18-stop-criteria)  
19. [Quality Gates](#19-quality-gates)  
20. [Audit Checklist](#20-audit-checklist)  
21. [Compliance Rules](#21-compliance-rules)  
22. [Non-Goals](#22-non-goals)  
23. [Appendices](#23-appendices)  
24. [Definitions & Glossary](#24-definitions--glossary)  
25. [Final Governance Statement](#25-final-governance-statement)  

---

## 1. Cover Page and Metadata

This section is satisfied by the title block, Document Control, Version History, and Document Hierarchy above. Status remains **Review Candidate (RC)**. Version remains **1.0**. This document is **not Locked** and **not Final**.

---

## 2. Purpose

Implementation Governance establishes the permanent policy for executing enterprise ERP development such that:

1. Architecture Lock v1.1 is preserved in every phase.  
2. Repository conventions are followed without invention or duplication.  
3. Documentation Lock is respected (no redesign of Locked FRD/ERD/BP during coding).  
4. Phase 0–4 proceed only under PEARB authorization with measurable entry/exit criteria.  
5. Validation and Release are evidence-based and fail-closed.  
6. Sprint 1–28 compatibility is maintained for all future modules.

---

## 3. Scope

### 3.1 In Scope

| Area | Coverage |
|------|----------|
| Phases | Phase 0–4 authorization, execution, completion |
| Code structure | Module packages, layers, naming, imports |
| Persistence | Models, migrations, DBS/ERD fidelity |
| API | Routers, schemas, mounts, OpenAPI coherence |
| Security | RBAC, tenancy, secrets, security tests |
| Async | Celery tasks registration and idempotency |
| Quality | Tests, static analysis, audits, gates, STOP |
| Post-phase | Validation · Validation Fix · Release readiness (implementation lens) |

### 3.2 Out of Scope

| Area | Governing document |
|------|--------------------|
| Board voting / constitution | PEARB Charter |
| Doc lifecycle / lock status model | Documentation Governance |
| Folder path stability / anti-duplicate trees | Repository Governance |
| Stack immutability / ADRs | Architecture Lock |
| Entity inventory / relationships | Locked FRD / ERD |
| Sprint-specific design content | Locked Backend Planning |

### 3.3 Policy Clarification

This document defines **implementation policy**. It does **not** replace sprint Backend Planning design content. Package layout must follow Repository Governance and living repository conventions even when planning text historically conflicted (editorial alignment required before scaffold).

---

## 4. Implementation Principles

| ID | Principle | Mandate |
|----|-----------|---------|
| IP-01 | **Govern before build** | No phase starts without Locked baselines and PEARB phase authorization. |
| IP-02 | **Repository First** | Living `modules/*` conventions are authoritative for package/file layout. |
| IP-03 | **Implementation Convention Precedence** | Doc conflict with repo → repository wins → editorial align docs → architecture unchanged → do not implement on conflicting prescription. |
| IP-04 | **Documentation Lock** | Do not redesign Locked FRD/ERD/BP during phases. |
| IP-05 | **Architecture Lock** | ADR-001 Modular Monolith · Clean Architecture · DDD; ADR-002 Python/FastAPI stack. |
| IP-06 | **Additive only** | New modules add capability; do not fork parallel architectures. |
| IP-07 | **No duplicates** | No duplicate modules, APIs, entities, migrations, or parallel implementations. |
| IP-08 | **Ownership** | Business modules remain SoR; peers via UUID + adapters only; no peer ORM. |
| IP-09 | **Fail closed** | Adapter/security/validation failures do not invent success states. |
| IP-10 | **Evidence over assertion** | Phase Completion and Validation require audits and gate results. |
| IP-11 | **Sprint compatibility** | New work must resemble Sprint 1–28 established patterns. |
| IP-12 | **STOP over speed** | Urgency never overrides STOP criteria. |

---

## 5. Phase Governance (Phase 0–4)

Phases execute only after: Sprint ARB → FRD → Entity Planning → Detailed ERD → Backend Planning are complete per frozen Sprint Lifecycle, and PEARB authorizes the specific phase.

### 5.1 Cross-Phase Rules

| Rule | Mandate |
|------|---------|
| PH-01 | Phases are sequential; do not skip or reorder. |
| PH-02 | Entity progress must match Backend Planning targets (e.g. 0 → N cumulative). |
| PH-03 | Each phase begins with locked-doc verification · conflict scan · ownership verification. |
| PH-04 | Each phase ends with Validation Gate (phase-scoped) · Architect Review Checklist · Completion Report. |
| PH-05 | Phase Completion Report must list remaining work honestly. |
| PH-06 | No scope expansion beyond Locked ERD/BP without PEARB substantive amendment. |

---

### 5.2 Phase 0 — Scaffold / Bootstrap

| Dimension | Governance |
|-----------|------------|
| **Purpose** | Module package scaffold, registrations, empty model registry, adapter skeletons, Alembic schema shell as planned — **0 business entities** unless Backend Planning explicitly states otherwise |
| **Entry Criteria** | Backend Planning Locked (or RC only if PEARB explicitly authorizes — default: Locked); Repository Convention Alignment complete if conflicts existed; PEARB Phase 0 authorization |
| **Deliverables** | `modules/<module>/` per §9; `router.py` + `routers/` shell; `dependencies.py`; `permissions.py` shell; `schemas.py` shell; `domain/`; `models/` registry; `repository/`; `service/` + `engines/`; `adapters/` skeleton; `tasks.py` shell; shared router include; Celery discovery; Alembic env import; MyPy path; schema shell migration theme as planned |
| **Mandatory Reviews** | Platform Architect (structure); Documentation & Governance (path notes); PEARB Phase 0 gate |
| **Quality Gates** | Architecture · Repository · Layering · Governance (phase-scoped) |
| **Exit Criteria** | Scaffold compiles/imports; registrations present; **0 / N** entities if planned; Phase 0 Completion Report accepted |
| **Completion Conditions** | No business CRUD; no unauthorized entities; no invented folders (`schemas/`, `mappers/`, module `tests/`, module `config.py`) |

---

### 5.3 Phase 1

| Dimension | Governance |
|-----------|------------|
| **Purpose** | Implement first Backend Planning entity cohort (repos · services · engines · routers · migrations · tests) |
| **Entry Criteria** | Phase 0 complete; PEARB Phase 1 authorization; Locked ERD/BP unchanged |
| **Deliverables** | Planned Phase 1 entities only; models/migrations; repositories; services/engines; routers/schemas; unit/security/integration tests under global tests tree; phase Completion Report |
| **Mandatory Reviews** | Domain · Database · Security · Platform · QA |
| **Quality Gates** | Architecture · Layering · Repository · API · Database · Security · Testing · Documentation · Governance |
| **Exit Criteria** | Entity count matches Phase 1 target; gates pass; Completion Report accepted |
| **Completion Conditions** | No peer ORM; RBAC on sensitive routes; ERD fidelity; Ruff/MyPy/Pytest phase-scoped clean |

---

### 5.4 Phase 2

| Dimension | Governance |
|-----------|------------|
| **Purpose** | Incremental entities/capabilities per Backend Planning Phase 2 |
| **Entry Criteria** | Phase 1 complete; PEARB Phase 2 authorization |
| **Deliverables** | Phase 2 entities + supporting layers/tests/migrations; Completion Report |
| **Mandatory Reviews** | Same specialty set as Phase 1; Integration Architect if new peer/adapter touchpoints |
| **Quality Gates** | Full implementation gate set (phase-scoped) |
| **Exit Criteria** | Cumulative entity count matches Phase 2 target |
| **Completion Conditions** | No scope bleed into Phase 3/4 entities; ownership preserved |

---

### 5.5 Phase 3

| Dimension | Governance |
|-----------|------------|
| **Purpose** | Incremental entities including external/adapter depth as planned |
| **Entry Criteria** | Phase 2 complete; PEARB Phase 3 authorization |
| **Deliverables** | Phase 3 entities; adapters as planned; tests; migrations; Completion Report |
| **Mandatory Reviews** | Integration · Security · Database · Performance (as applicable) · PEARB |
| **Quality Gates** | Full set + adapter/ownership emphasis |
| **Exit Criteria** | Cumulative count matches Phase 3 target |
| **Completion Conditions** | External platforms remain external; `secret_ref` only; fail-closed adapter behavior |

---

### 5.6 Phase 4

| Dimension | Governance |
|-----------|------------|
| **Purpose** | Final planned entities; permission seed; hardening; Validation readiness |
| **Entry Criteria** | Phase 3 complete; PEARB Phase 4 authorization |
| **Deliverables** | Final entity cohort; `permissions.py` + seed migration as planned; hardening; full phase tests; Completion Report stating **N / N** |
| **Mandatory Reviews** | Security (permissions) · QA · Database · PEARB |
| **Quality Gates** | Full set + Release Readiness precursor |
| **Exit Criteria** | Exact locked entity count achieved; permissions seeded; Completion Report accepted |
| **Completion Conditions** | Ready for Validation stage; no silent extra entities/tables |

---

## 6. Coding Governance

| Rule | Mandate |
|------|---------|
| CG-01 | Python 3.13+ · FastAPI · SQLAlchemy 2.0 · Pydantic v2 · Celery per Architecture Lock. |
| CG-02 | Absolute imports `modules.<pkg>...` per established practice. |
| CG-03 | Type hints required on public service/repository/engine APIs. |
| CG-04 | No business rules in routers. |
| CG-05 | No ORM in domain/engines. |
| CG-06 | No peer-module model imports for writes. |
| CG-07 | Idempotent tasks; safe retries. |
| CG-08 | Ruff and MyPy must pass for touched packages (phase-scoped). |
| CG-09 | Do not commit secrets. |
| CG-10 | Prefer patterns from established peers (`devportal`, `ai`, etc.) over novelty. |

---

## 7. Clean Architecture Governance

### 7.1 Mandatory Layer Direction

```text
routers/ (API)
    ↓
service/ (Application)
    ↓
service/engines/ + domain/ (Domain policy — ORM-free)
    ↓
repository/ + models/ + adapters/ (Infrastructure)
```

| Rule | Mandate |
|------|---------|
| CA-01 | Dependencies point inward to domain. |
| CA-02 | Routers depend on services/dependencies — not repositories/models directly for writes (follow peer module practice). |
| CA-03 | Engines contain pure policy; no Session/HTTP clients. |
| CA-04 | Repositories encapsulate persistence queries. |
| CA-05 | Adapters isolate Foundation/Hub/external I/O. |
| CA-06 | Bypass of service/engine for business writes is forbidden. |

---

## 8. DDD Governance

| Rule | Mandate |
|------|---------|
| DDD-01 | Bounded context == module package under `modules/<name>/`. |
| DDD-02 | Ubiquitous language matches Locked FRD/ERD names. |
| DDD-03 | Domain enums/exceptions/VOs live in `domain/`. |
| DDD-04 | Lifecycle and invariants live in engines. |
| DDD-05 | Aggregates/transaction boundaries follow Backend Planning / ERD. |
| DDD-06 | Do not invent new domain concepts absent from Locked FRD/ERD. |

---

## 9. Repository Implementation Rules

### 9.1 Canonical Module Layout (mandatory)

```text
modules/<module>/
├── __init__.py
├── router.py
├── routers/
├── dependencies.py
├── permissions.py
├── schemas.py
├── domain/
├── models/
├── repository/
├── service/
│   └── engines/
├── adapters/
└── tasks.py
```

### 9.2 Package Rules

| Package / File | Rule |
|----------------|------|
| **`schemas.py`** | Flat Pydantic v2 DTOs; no `schemas/` package by default |
| **`service/`** | Application services; singular name — not `services/` |
| **`service/engines/`** | ORM-free policy engines |
| **`repository/`** | Persistence repositories |
| **`domain/`** | Enums · exceptions · entities/VOs — ORM-free |
| **`models/`** | SQLAlchemy models matching Detailed ERD |
| **`adapters/`** | Ports for Foundation · Hub · peers · external systems |
| **`router.py`** | Aggregate include for `/api/v1/<module>` |
| **`routers/`** | Thin HTTP handlers only |
| **`dependencies.py`** | Tenant · RBAC · UoW/session helpers |
| **`permissions.py`** | `<module>.*` permission constants |
| **`tasks.py`** | Celery task shells — idempotent |

### 9.3 Forbidden Anti-Patterns

| Anti-pattern | Rule |
|--------------|------|
| `mappers/` package | Forbidden by default — map via `schemas.py` + services |
| Module `config.py` | Forbidden by default |
| Module-local `tests/` | Forbidden — use `apps/api/src/tests/...` |
| Duplicate module package | Forbidden |
| Parallel implementation | Forbidden |

### 9.4 Registrations (mandatory for new modules)

| Concern | Location |
|---------|----------|
| API include | `shared/router.py` (or current shared aggregator) |
| Celery | `workers/celery_app.py` discovery list |
| Alembic | `alembic/env.py` model import |
| MyPy | `pyproject.toml` overrides |

---

## 10. API Implementation Rules

| Rule | Mandate |
|------|---------|
| API-01 | Mount once under `/api/v1/<module>`. |
| API-02 | No duplicate resources for the same SoR capability. |
| API-03 | Request/response via `schemas.py` (Pydantic v2). |
| API-04 | AuthZ via Foundation helpers + `permissions.py`. |
| API-05 | Consistent pagination/sort patterns with peer modules. |
| API-06 | OpenAPI must reflect implemented routes at Validation. |
| API-07 | Error handling fail-closed; do not leak internals. |

---

## 11. Database Implementation Rules

| Rule | Mandate |
|------|---------|
| DB-01 | Models match Locked Detailed ERD exactly (columns/FKs/UUID attrs). |
| DB-02 | Schema name and table prefix per lock. |
| DB-03 | DBS v1.1 naming and standards. |
| DB-04 | Soft-delete · tenant · audit · version stamps as required. |
| DB-05 | Alembic only; single history; no duplicate migrations. |
| DB-06 | No peer-schema FK invention; UUID peer refs where locked. |
| DB-07 | No extra entities beyond Locked inventory. |

---

## 12. Security Implementation Rules

| Rule | Mandate |
|------|---------|
| SEC-01 | Enforce RBAC on mutating and sensitive read routes. |
| SEC-02 | Tenant isolation on all multi-tenant queries. |
| SEC-03 | No plaintext secrets; `secret_ref` only where designed. |
| SEC-04 | Audit significant state changes via Foundation audit patterns. |
| SEC-05 | Security tests under `tests/security/<module>/`. |
| SEC-06 | Permission seed only in authorized phase (typically Phase 4). |

---

## 13. Dependency Injection Governance

| Rule | Mandate |
|------|---------|
| DI-01 | Use FastAPI dependencies via module `dependencies.py` and Foundation shared deps. |
| DI-02 | Services constructed with Session/UoW per peer module practice. |
| DI-03 | Do not invent a second DI container/framework. |
| DI-04 | Permission checks use `require_permission` (or current Foundation equivalent). |
| DI-05 | Test doubles replace repositories/adapters at service boundaries — not by rewriting routers into god-objects. |

---

## 14. Background Task Governance

| Rule | Mandate |
|------|---------|
| BT-01 | Celery tasks live in module `tasks.py` (or established split only if peers already do). |
| BT-02 | Register module in Celery autodiscovery. |
| BT-03 | Tasks must be idempotent and safe under retry. |
| BT-04 | Tasks must not bypass engines for domain policy. |
| BT-05 | No uncontrolled fan-out jobs that invent telemetry SoR behavior. |
| BT-06 | Beat schedules only when Backend Planning/Architecture Lock allow. |

---

## 15. Testing Governance

| Rule | Mandate |
|------|---------|
| TST-01 | Global layout: `apps/api/src/tests/{unit,security,integration}/<module>/`. |
| TST-02 | Unit: engines · validators · service mapping helpers. |
| TST-03 | Security: RBAC · tenant · secret-ref rejection. |
| TST-04 | Integration: module import · DB constraints · soft-delete · version as applicable. |
| TST-05 | Phase-scoped tests required before Phase Completion accept. |
| TST-06 | Validation Fix is hygiene-only unless PEARB expands scope. |

---

## 16. Performance Governance

| Rule | Mandate |
|------|---------|
| PF-01 | List endpoints must paginate. |
| PF-02 | Avoid N+1 query patterns in repositories. |
| PF-03 | Caching only per Backend Planning; no telemetry time-series SoR cache. |
| PF-04 | Heavy work belongs in idempotent async tasks. |
| PF-05 | External adapter calls must have timeouts/fail-closed behavior. |

---

## 17. Exception Management

| Rule | Mandate |
|------|---------|
| EX-01 | Domain exceptions live in `domain/exceptions.py` (or established domain exception modules). |
| EX-02 | Map domain exceptions to HTTP status in router/handler layer consistently with peers. |
| EX-03 | Do not catch-and-ignore architecture/security failures. |
| EX-04 | Adapter failures fail closed — do not invent healthy/success telemetry states. |
| EX-05 | Published/immutable policy violations raise explicit domain errors. |

---

## 18. STOP Criteria

Implementation **must STOP** immediately when any condition holds:

| ID | STOP Condition |
|----|----------------|
| STOP-A | **Architecture violation** — Architecture Lock / ADR / Clean Architecture / DDD breach |
| STOP-R | **Repository violation** — invented folders, duplicate trees, missing registrations, anti-patterns |
| STOP-S | **Security violation** — secrets in code/DB plaintext, missing RBAC/tenant isolation |
| STOP-D | **Duplicate implementation** — duplicate APIs/entities/migrations/modules |
| STOP-P | **Parallel implementation** — second stack/package delivering same capability |
| STOP-PH | **Phase violation** — wrong phase scope, skipped phase, unauthorized start |
| STOP-DOC | **Documentation violation** — coding against non-Locked baseline; redesigning Locked FRD/ERD/BP |
| STOP-G | **Governance violation** — contradicting Master/PEARB/Repository/Documentation/Implementation Governance |

**On STOP:** Halt the phase · record finding · escalate per PEARB · do not continue until cleared.

---

## 19. Quality Gates

| Gate Area | Gate ID | Requirement |
|-----------|---------|-------------|
| **Architecture** | IQG-AR-01 | Architecture Lock preserved; no peer ORM; ownership intact |
| **Layering** | IQG-LY-01 | Clean Architecture direction; engines ORM-free |
| **Repository** | IQG-RP-01 | §9 layout; registrations complete; no anti-patterns |
| **API** | IQG-API-01 | Single mount; schemas; RBAC; OpenAPI coherence |
| **Database** | IQG-DB-01 | ERD fidelity; Alembic integrity; exact entity count |
| **Security** | IQG-SEC-01 | Permissions · tenant · secrets · security tests |
| **Testing** | IQG-TST-01 | Global tests present; Pytest/Ruff/MyPy phase-scoped |
| **Performance** | IQG-PF-01 | Pagination; no unbounded hot paths introduced |
| **Documentation** | IQG-DOC-01 | Completion Report accurate; baselines cited; status honest |
| **Governance** | IQG-GV-01 | Phase authorized; STOP register clear; parent compliance |
| **Release Readiness** | IQG-REL-01 | Phase 4 complete; Validation acceptable precursor evidence |

**Fail-closed:** Failed gate blocks Phase Completion accept.

---

## 20. Audit Checklist

Mandatory implementation audits (phase-scoped; full set at Validation):

### 20.1 Repository Audit
- [ ] Module layout matches §9  
- [ ] No `schemas/`, `mappers/`, module `config.py`, module-local `tests/`  
- [ ] Router · Celery · Alembic · MyPy registrations updated  

### 20.2 Architecture Audit
- [ ] Architecture Lock / ADR compliance  
- [ ] SoR ownership preserved  
- [ ] No parallel architecture  

### 20.3 Layering Audit
- [ ] Router thin  
- [ ] Engines ORM-free  
- [ ] No persistence bypass  

### 20.4 Dependency Audit
- [ ] Approved stack only  
- [ ] No superseded frameworks  

### 20.5 API Audit
- [ ] Mount uniqueness  
- [ ] Schemas/RBAC/OpenAPI  

### 20.6 Database Audit
- [ ] ERD match  
- [ ] Migration lineage  
- [ ] Entity count  

### 20.7 Security Audit
- [ ] Permissions  
- [ ] Tenant isolation  
- [ ] No secrets  

### 20.8 Testing Audit
- [ ] unit/security/integration suites  
- [ ] Static checks clean  

### 20.9 Documentation Audit
- [ ] Completion Report  
- [ ] Locked baselines unchanged  
- [ ] Traceability  

### 20.10 Performance Audit
- [ ] Pagination  
- [ ] Query/task risk review  

### 20.11 Governance Audit
- [ ] Phase authorization evidenced  
- [ ] STOP criteria clear  
- [ ] Parent governance respected  

---

## 21. Compliance Rules

All implementers shall:

1. Obtain PEARB phase authorization before coding each phase.  
2. Implement only Locked ERD inventory and Backend Planning scope.  
3. Follow Repository First and §9 package conventions.  
4. Preserve Architecture Lock and Clean Architecture/DDD rules.  
5. Enforce security, testing, and registration requirements.  
6. Produce Completion Reports and pass quality gates.  
7. Honor STOP criteria without exception for schedule pressure.  
8. Preserve Sprint 1–28 compatibility and stable documentation paths.  

Non-compliance → STOP, rejection of Phase Completion, and/or refusal of Validation/Release readiness.

---

## 22. Non-Goals

This document **does NOT**:

1. Replace Architecture Lock.  
2. Replace Repository Governance.  
3. Replace Documentation Governance.  
4. Replace the PEARB Charter.  
5. Replace Enterprise Master Governance.  
6. Implement code by publication.  
7. Authorize architecture redesign.  
8. Authorize Phase 0–4 by itself (PEARB phase authorization still required).  
9. Modify Locked FRD/ERD/Backend Planning content.  
10. Mark itself Locked or Final in this Review Candidate revision.

---

## 23. Appendices

### Appendix A — Frozen Sprint Lifecycle (implementation window)

```text
… → Backend Planning (Locked) → Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4
→ Validation → Validation Fix → Release → Sprint Completion
```

### Appendix B — Implementation Convention Precedence (normative)

1. Repository implementation conventions win.  
2. Planning documents must be editorially aligned.  
3. Architecture must NOT change.  
4. Implementation must NOT begin on the conflicting prescription.

### Appendix C — Layer Responsibility Matrix

| Layer | May | Must not |
|-------|-----|----------|
| `routers/` | HTTP map · status codes · deps | Business rules · ORM writes |
| `service/` | Use-cases · transactions · orchestration | Bypass engines for policy |
| `engines/` / `domain/` | Policy · invariants · lifecycle | ORM · HTTP · peer SDKs |
| `repository/` / `models/` | Persistence | Own product policy |
| `adapters/` | External/peer I/O | Become alternate SoR |

### Appendix D — Phase Entity Progress (pattern)

Phases deliver cumulative entity progress defined by Locked Backend Planning (example pattern: `0 → 7 → 10 → 16 → 17`). Exact numbers are sprint-specific and must match the Locked plan — never invented mid-phase.

---

## 24. Definitions & Glossary

| Term | Definition |
|------|------------|
| **Phase authorization** | Explicit PEARB approval to begin a numbered phase |
| **Phase Completion** | Accepted Completion Report after gates/audits pass |
| **Repository First** | Code conventions outrank conflicting planning layout text |
| **Peer ORM** | Writing another module’s SQLAlchemy models — forbidden |
| **Adapter** | Boundary component for Foundation/Hub/external I/O |
| **Engine** | ORM-free domain policy component under `service/engines/` |
| **STOP** | Mandatory halt until PEARB clears the violation |
| **Fail closed** | Errors do not fabricate successful external/health states |
| **Scaffold** | Phase 0 package/registration shell without business entity CRUD |
| **RC** | Review Candidate — this document’s current status |

---

## 25. Final Governance Statement

The Permanent Enterprise Architecture Review Board hereby publishes **Implementation Governance v1.0** as a **Review Candidate (RC)**.

By this document:

- Permanent implementation policy from Phase 0 through Release is defined.  
- Repository First, Implementation Convention Precedence, Documentation Lock, and Architecture Lock are binding on all coding work.  
- Phase entry/exit criteria, deliverables, reviews, gates, and completion conditions are established.  
- Clean Architecture, DDD, and canonical module package rules are mandatory.  
- STOP criteria, audits, and quality gates are fail-closed.  
- Parent authorities remain: Master Governance · PEARB Charter · Repository Governance · Documentation Governance · Architecture Lock v1.1.  

This Review Candidate is **not Locked**, does **not** implement code, and does **not** by itself authorize Phase 0–4 execution.

**Implementation Governance v1.0 — Review Candidate (RC).**

**Enterprise Master Governance — Respected.**

**PEARB Charter — Respected.**

**Repository Governance — Respected.**

**Documentation Governance — Respected.**

**Architecture Lock v1.1 — Preserved.**

**Sprint 1–28 — Official Baseline.**

**Permanent Enterprise Architecture Review Board — Implementation Governance Published for Review.**

---

*End of Implementation Governance v1.0 — Review Candidate (RC)*
