# Repository Governance

## Multi-Industry Enterprise ERP Platform

---

| Field | Value |
|-------|--------|
| **Document Title** | Repository Governance |
| **Document ID** | RG-01 |
| **Filename (canonical)** | `Repository_Governance_v1.0.md` |
| **Version** | **1.0** |
| **Status** | **Review Candidate (RC)** |
| **Document Status** | **Review Candidate (RC) — Not Locked** |
| **Classification** | Internal — Confidential |
| **Authority** | Permanent Enterprise Architecture Review Board (PEARB) |
| **Effective Date (proposed)** | 2026-07-29 |
| **Scope** | Structure, maintenance, review, evolution, audit, and quality gates for the ERP platform repository |
| **Parent Governance** | `Enterprise_Master_Governance_v1.0.md` |
| **Board Charter** | `Enterprise_Architecture_Review_Board_v1.0.md` |
| **Architecture Baseline** | Architecture Lock Report v1.1 |
| **Official Historical Baseline** | Sprint 1 through Sprint 28 (complete) |
| **Current Delivery Context** | Sprint 29 and all subsequent sprints |
| **Repository Location** | `docs/05_ARCHITECTURE_LOCK/Governance/` |
| **Supersedes** | None (first official Repository Governance) |
| **Does Not Replace** | Enterprise Master Governance · PEARB Charter · Architecture Lock v1.1 · BRD · FRD · SDD · DBS · ERD · Sprint artifacts |

> **Repository governance only.** This document defines **policy** for how the repository must be structured, maintained, reviewed, and evolved. It does **not** replace implementation design, Architecture Lock, Master Governance, or the PEARB Charter. It does **not** implement code, modify the repository by publication, authorize implementation phases, or reorganize folders.

---

### Document Control

| Role | Responsibility |
|------|----------------|
| **PEARB** | Author, custodian, and sole amendatory authority |
| **Platform Architect (PEARB seat)** | Primary specialty owner for repository convention enforcement |
| **Documentation & Governance Architect** | Documentation path stability and placement rules |
| **Database Architect** | Migration and schema repository rules |
| **Quality Assurance Architect** | Testing layout and repository quality gates |
| **Delivery Teams / Agents / Vendors** | Mandatory adherence |

### Version History

| Version | Date | Change | Authority |
|---------|------|--------|-----------|
| **1.0** | 2026-07-29 | Initial Repository Governance (Review Candidate). Codifies Repository First, Implementation Convention Precedence, directory/naming standards, module conventions, documentation and sprint-report placement, audits, quality gates, change management, approval, and escalation. Complies with Master Governance, PEARB Charter, Architecture Lock v1.1, Sprint 1–28 baseline, and current repository structure. Does not lock; does not authorize implementation. | PEARB — Review Candidate |

### Document Hierarchy

```text
1. Enterprise Master Governance v1.0
2. Architecture Lock v1.1 (+ locked ADRs)
3. Enterprise Architecture Review Board Charter v1.0
4. Repository Governance v1.0 (this document)
5. BRD · SDD · DBS
6. Sprint ARB Recommendation → FRD → ERD → Backend Planning
7. Phase / Validation / Release / Completion artifacts
8. Source code and migrations (must conform upward)
```

This document **shall not** contradict parent governance. Where ambiguity arises, Master Governance conflict resolution and Architecture Lock precedence apply. Repository implementation conventions govern package/file layout when planning text conflicts with established code (Master Governance Repository First / Implementation Convention Precedence).

---

## Table of Contents

1. [Cover Page and Metadata](#cover-page-and-metadata)  
2. [Repository Purpose](#2-repository-purpose)  
3. [Governance Scope](#3-governance-scope)  
4. [Mandatory Repository Principles](#4-mandatory-repository-principles)  
5. [Repository Hierarchy](#5-repository-hierarchy)  
6. [Directory Structure Governance](#6-directory-structure-governance)  
7. [Naming Convention Governance](#7-naming-convention-governance)  
8. [File Naming Standards](#8-file-naming-standards)  
9. [Folder Naming Standards](#9-folder-naming-standards)  
10. [Documentation Governance Rules](#10-documentation-governance-rules)  
11. [Documentation Placement Rules](#11-documentation-placement-rules)  
12. [Sprint Report Placement Rules](#12-sprint-report-placement-rules)  
13. [Source Code Governance Rules](#13-source-code-governance-rules)  
14. [Module Structure Governance](#14-module-structure-governance)  
15. [Shared Component Governance](#15-shared-component-governance)  
16. [Configuration Governance](#16-configuration-governance)  
17. [Database Governance](#17-database-governance)  
18. [Migration Governance](#18-migration-governance)  
19. [API Governance](#19-api-governance)  
20. [Security Governance](#20-security-governance)  
21. [Dependency Governance](#21-dependency-governance)  
22. [Testing Repository Governance](#22-testing-repository-governance)  
23. [CI/CD Repository Governance](#23-cicd-repository-governance)  
24. [Asset Governance](#24-asset-governance)  
25. [Logging & Monitoring Artifact Governance](#25-logging--monitoring-artifact-governance)  
26. [Version Control Governance](#26-version-control-governance)  
27. [Repository Review Workflow](#27-repository-review-workflow)  
28. [Repository Audit Checklist](#28-repository-audit-checklist)  
29. [Repository Quality Gates](#29-repository-quality-gates)  
30. [Repository Change Management](#30-repository-change-management)  
31. [Repository Approval Workflow](#31-repository-approval-workflow)  
32. [Repository Escalation Process](#32-repository-escalation-process)  
33. [Repository Compliance Rules](#33-repository-compliance-rules)  
34. [Non-Goals](#34-non-goals)  
35. [Appendices](#35-appendices)  
36. [Definitions & Glossary](#36-definitions--glossary)  
37. [Final Governance Statement](#37-final-governance-statement)  

---

<a id="cover-page-and-metadata"></a>

## 1. Cover Page and Metadata

This section is satisfied by the title block, Document Control, Version History, and Document Hierarchy above. Status remains **Review Candidate (RC)**. Version remains **1.0**. This document is **not Locked** and **not Final**.

---

## 2. Repository Purpose

The ERP repository is the **single authoritative workspace** for:

1. Platform source code (modular monolith under Architecture Lock v1.1).  
2. Enterprise documentation (BRD · FRD · SDD · DBS · Architecture Lock · Governance · ERD · Releases · Sprint Reports).  
3. Database migrations and schema evolution under DBS governance.  
4. Tests, workers, shared API registration, and operational configuration consistent with locked stack.  
5. Audit evidence for PEARB stage gates, Validation, Release, and Sprint Completion.

The repository exists to preserve **continuity, consistency, and trust** from Sprint 1–28 onward while enabling additive evolution under governance.

---

## 3. Governance Scope

### 3.1 In Scope

| Area | Scope |
|------|-------|
| Structure | Top-level and module directory layout |
| Naming | Files, folders, packages, modules, schemas, prefixes |
| Documentation | Placement, lock status honesty, path stability |
| Source code | Module conventions, imports, layering |
| Data | Schemas, models, Alembic lineage |
| API | Mount registration, router aggregation |
| Security | Secrets handling in repo, RBAC constants placement |
| Dependencies | Approved stack alignment |
| Tests | Global test tree |
| CI/CD artifacts | Pipeline definitions as repository citizens |
| Change control | Restructuring, duplicates, parallel implementations |
| Audits & gates | Mandatory repository audits and quality gates |

### 3.2 Out of Scope (handled by parent docs)

| Area | Governing document |
|------|--------------------|
| Board constitution / voting | PEARB Charter |
| Enterprise vision / hierarchy of authority | Master Governance |
| Technology stack immutability | Architecture Lock v1.1 |
| Domain entity inventory / relationships | Locked FRD / ERD |
| Phase implementation design details | Locked Backend Planning (subject to Repository First) |

### 3.3 Policy vs Design

**Governance documents define policy.** They do **not** replace implementation design. Backend Planning and phase design must still specify entity/services/engines within locked architecture — but package/file layout must follow this Repository Governance and living repository conventions.

---

## 4. Mandatory Repository Principles

The following principles are **permanent** unless amended by unanimous PEARB decision under Master Governance:

| ID | Principle | Mandate |
|----|-----------|---------|
| RP-01 | **Repository First** | Existing implementation conventions in the repository are authoritative for package/file layout, naming, DI, router registration, tests location, and related conventions. |
| RP-02 | **Implementation Convention Precedence** | When documentation conflicts with repository conventions: (1) repository wins; (2) planning docs are editorially aligned; (3) architecture does not change; (4) implementation must not begin on the conflicting prescription. |
| RP-03 | **Documentation Lock** | Locked documents are not redesigned during implementation; editorial alignment only when authorized; status honesty (RC ≠ Locked). |
| RP-04 | **Architecture Lock** | Architecture Lock v1.1 is preserved; repository changes may not invent alternate architecture. |
| RP-05 | **No duplicate folders** | Do not create parallel folder trees for the same concern. |
| RP-06 | **No duplicate modules** | One bounded-context module package per owned domain module. |
| RP-07 | **No parallel implementations** | Do not implement the same capability twice under different packages/stacks. |
| RP-08 | **No duplicate APIs** | Do not expose duplicate mounts/resources for the same SoR capability. |
| RP-09 | **No duplicate entities** | Do not create duplicate tables/models for the same locked entity. |
| RP-10 | **No duplicate migrations** | Do not fork Alembic histories or re-apply the same revision theme as a parallel chain. |
| RP-11 | **No repository restructuring without approval** | Renames, moves, and reorganizations require PEARB Class A/B approval. |
| RP-12 | **Backward compatibility** | Sprint 1–28 outcomes and paths remain valid. |
| RP-13 | **Sprint compatibility** | New work remains recognizable within the frozen Sprint Lifecycle and established repo patterns. |
| RP-14 | **Stable documentation paths** | Existing `docs/**` names and locations are stable. |
| RP-15 | **Stable report locations** | Sprint reports and releases remain under established `docs/08_SPRINT_REPORTS/` and `docs/07_RELEASES/` practice. |

---

## 5. Repository Hierarchy

### 5.1 Logical Hierarchy (governance view)

```text
Repository Root
├── docs/                          # Enterprise documentation (stable numbered roots)
├── apps/                          # Application code (modular monolith API and related apps)
├── (platform tooling / infra as already present) 
└── .git / VCS metadata
```

### 5.2 Documentation Root (`docs/`) — Current Stable Layout

| Path | Role |
|------|------|
| `docs/01_BRD/` | Business Requirements |
| `docs/02_FRD/` | Functional Requirements |
| `docs/03_SDD/` | System Design |
| `docs/04_DBS/` | Database Standards |
| `docs/05_ARCHITECTURE_LOCK/` | Architecture Lock + Governance |
| `docs/05_ARCHITECTURE_LOCK/Governance/` | Master Governance · PEARB Charter · Repository Governance (and future governed annexes only by PEARB) |
| `docs/06_ERD/` | Entity Planning and Detailed ERD |
| `docs/07_RELEASES/` | Platform release notes |
| `docs/08_SPRINT_REPORTS/` | Sprint ARB, Backend Planning, phase/validation/completion reports |

**Stability rule:** Do not invent alternate documentation roots (e.g. new top-level `docs/04_Backend_Planning/`) when established sprint practice places Backend Planning under `docs/08_SPRINT_REPORTS/Sprint_N/`.

### 5.3 Backend Application Hierarchy (authoritative convention)

```text
apps/api/
├── alembic/                       # Migration environment and revisions
├── pyproject.toml                 # Tooling · MyPy package paths
└── src/
    ├── modules/                   # Domain modules (SoR packages)
    ├── shared/                    # Shared API aggregation (e.g. router.py)
    ├── tests/                     # Global tests (unit · security · integration)
    ├── workers/                   # Celery app / workers
    └── (database/core/platform packages as already established)
```

Exact subordinate packages already present in the repository remain authoritative; this document does not invent new top-level trees.

---

## 6. Directory Structure Governance

| Rule | Mandate |
|------|---------|
| DS-01 | Preserve existing top-level `docs/` numbered directories. |
| DS-02 | Preserve `apps/api/src/modules/<module>/` as the home of domain modules. |
| DS-03 | Preserve global `apps/api/src/tests/{unit,security,integration}/`. |
| DS-04 | Do not create module-local `tests/` packages when global tests are the convention. |
| DS-05 | Do not create `schemas/` packages when flat `schemas.py` is the module convention. |
| DS-06 | Do not create `mappers/` packages when mapping is performed via `schemas.py` + services. |
| DS-07 | Do not create module-level `config.py` when modules do not use that convention. |
| DS-08 | Do not create `services/` (plural) when `service/` (singular) is the convention. |
| DS-09 | New directories require PEARB approval unless they are the standard empty package scaffolding inside an authorized new module following §14. |
| DS-10 | Empty / mistaken documentation roots must not be reintroduced after retirement. |

---

## 7. Naming Convention Governance

| Domain | Convention |
|--------|------------|
| Python packages | `snake_case` |
| Modules | Short domain names under `modules/` (e.g. `devportal`, `monitoring`) matching Backend Planning |
| PostgreSQL schemas | Domain schema names per locked ERD/DBS (e.g. `monitoring`) |
| Tables | Locked prefixes (e.g. `mon_`, `dp_`) — never invent competing prefixes for the same module |
| API mounts | `/api/v1/<module>` as locked in Backend Planning |
| RBAC | `<module>.*` namespace constants in `permissions.py` |
| Alembic themes | Phase-indicative names; IDs assigned at implementation time — no duplicate themes |
| Documentation files | Established sprint patterns (`FRD-NN-...`, `ERD-NN-...`, `Sprint_NN_...`, `ERP_Core_vX.Y-beta.md`) |
| Governance files | `Pascal_Snake` descriptive names with `_vMajor.Minor.md` under Governance |

---

## 8. File Naming Standards

| Artifact | Standard |
|----------|----------|
| Module Python files | `snake_case.py` |
| Aggregate router | `router.py` |
| Router handlers | under `routers/` with domain-oriented names |
| Pydantic DTOs | `schemas.py` (flat file) |
| DI | `dependencies.py` |
| RBAC constants | `permissions.py` |
| Celery tasks | `tasks.py` |
| SQLAlchemy models | one model file per entity (or established module pattern) under `models/` |
| Repositories | `*_repository.py` under `repository/` |
| Services | `*_service.py` under `service/` |
| Engines | under `service/engines/` |
| Adapters / ports | under `adapters/` |
| Tests | `test_*.py` under global tests tree |
| Docs | Match existing sprint/domain naming; do not invent colliding filenames |

---

## 9. Folder Naming Standards

| Folder | Standard |
|--------|----------|
| `modules/<name>/` | lowercase `snake_case` module name |
| `routers/` | plural handlers package |
| `service/` | singular application services |
| `service/engines/` | policy engines |
| `repository/` | persistence |
| `domain/` | ORM-free domain |
| `models/` | ORM models |
| `adapters/` | ports/adapters |
| `docs/0N_NAME/` | preserve existing numbered roots |
| `docs/08_SPRINT_REPORTS/Sprint_NN/` | sprint folder naming |
| `docs/05_ARCHITECTURE_LOCK/Governance/` | governance annexes only |

---

## 10. Documentation Governance Rules

| Rule | Mandate |
|------|---------|
| Doc-01 | Locked documents are frozen substantively. |
| Doc-02 | RC documents must not be treated as Locked. |
| Doc-03 | Version history required on governed documents. |
| Doc-04 | Editorial convention alignment must not change entities, phases, architecture, or ownership. |
| Doc-05 | Do not rename or move existing docs without PEARB approval. |
| Doc-06 | Do not create parallel documentation trees for the same artifact class. |
| Doc-07 | Governance docs live under `docs/05_ARCHITECTURE_LOCK/Governance/` unless PEARB relocates by Class A decision. |
| Doc-08 | Parent precedence: Master Governance > Architecture Lock > PEARB Charter > Repository Governance > sprint artifacts. |

---

## 11. Documentation Placement Rules

| Artifact class | Stable placement |
|----------------|------------------|
| BRD | `docs/01_BRD/` |
| FRD | `docs/02_FRD/` |
| SDD | `docs/03_SDD/` |
| DBS | `docs/04_DBS/` |
| Architecture Lock | `docs/05_ARCHITECTURE_LOCK/` |
| Governance | `docs/05_ARCHITECTURE_LOCK/Governance/` |
| ERD (Entity Planning + Detailed) | `docs/06_ERD/` |
| Releases | `docs/07_RELEASES/` |
| Sprint Reports (ARB, Backend Planning, Phase/Validation/Completion) | `docs/08_SPRINT_REPORTS/Sprint_NN/` |

**Prohibition:** Do not place Backend Planning under a newly invented `docs/04_Backend_Planning/` (or similar) when sprint practice is `docs/08_SPRINT_REPORTS/`.

---

## 12. Sprint Report Placement Rules

| Report | Placement |
|--------|-----------|
| Architecture Review Board Recommendation | `docs/08_SPRINT_REPORTS/Sprint_NN/` |
| Backend Planning | `docs/08_SPRINT_REPORTS/Sprint_NN/` |
| Phase 0–4 Completion Reports | `docs/08_SPRINT_REPORTS/Sprint_NN/` |
| Validation Report / Validation Fix Report | `docs/08_SPRINT_REPORTS/Sprint_NN/` |
| Sprint Completion Report | `docs/08_SPRINT_REPORTS/Sprint_NN/` |
| Release Notes | `docs/07_RELEASES/` |

Sprint folders are additive (`Sprint_29`, `Sprint_30`, …). Historical Sprint 1–28 report locations remain stable.

---

## 13. Source Code Governance Rules

| Rule | Mandate |
|------|---------|
| SC-01 | Modular monolith only (ADR-001). |
| SC-02 | Clean Architecture layering: Router → Service → Engine → Repository → Model. |
| SC-03 | Domain and engines remain ORM-free. |
| SC-04 | No peer-module ORM writes; UUID-only peer refs; adapters for cross-module I/O. |
| SC-05 | Absolute imports `modules.<pkg>...` per established practice. |
| SC-06 | Python/FastAPI/SQLAlchemy/Pydantic/Celery stack per Architecture Lock (ADR-002). |
| SC-07 | Do not introduce NestJS/Prisma or other superseded stacks. |
| SC-08 | New modules must mirror established peers (e.g. `devportal`, `ai`). |
| SC-09 | Register routers in `shared/router.py` (or current shared aggregation point). |
| SC-10 | Register Celery packages in `workers/celery_app.py` (or current discovery list). |
| SC-11 | Register models in `alembic/env.py` discovery imports. |
| SC-12 | Update MyPy package overrides in `pyproject.toml` when adding modules. |

---

## 14. Module Structure Governance

### 14.1 Canonical Module Layout (repository convention)

Planning and Phase 0 scaffolds for new modules **must** align to living repository conventions:

```text
modules/<module>/
├── __init__.py
├── router.py                 # aggregate include → /api/v1/<module>
├── routers/                  # thin handlers
├── dependencies.py           # tenant · RBAC · UoW helpers
├── permissions.py            # <module>.* constants
├── schemas.py                # Pydantic v2 DTOs (flat file)
├── domain/                   # enums · exceptions · entities/VOs (ORM-free)
├── models/                   # SQLAlchemy models
├── repository/               # repositories
├── service/                  # application services
│   └── engines/              # lifecycle · policy engines
├── adapters/                 # Foundation · Hub · peer · external ports
└── tasks.py                  # Celery tasks (idempotent)
```

### 14.2 Explicitly Not Used (absent across established modules)

| Anti-pattern | Governance |
|--------------|------------|
| `schemas/` package | Forbidden as default; use `schemas.py` |
| `mappers/` package | Forbidden as default; map via schemas + services |
| Module-level `config.py` | Forbidden as default |
| Module-local `tests/` | Forbidden as default; use global tests |
| `services/` (plural) | Forbidden as default; use `service/` |

### 14.3 Policy Clarification

This layout is a **repository convention governance** baseline. It does **not** replace Backend Planning design content (entities, engines, phase maps). It constrains **where** code lives.

---

## 15. Shared Component Governance

| Rule | Mandate |
|------|---------|
| SH-01 | Shared API aggregation remains in established shared packages (e.g. `shared/router.py`). |
| SH-02 | Foundation remains SoR for Auth · RBAC · Audit · Notification · Workflow patterns. |
| SH-03 | Do not duplicate Foundation capabilities inside business modules. |
| SH-04 | Shared utilities must not become a dumping ground that bypasses module ownership. |
| SH-05 | Cross-cutting changes to shared registration points require PEARB awareness at phase gates. |

---

## 16. Configuration Governance

| Rule | Mandate |
|------|---------|
| CFG-01 | Prefer platform/environment settings patterns already used by the repository. |
| CFG-02 | Do not invent per-module `config.py` when peers do not use it. |
| CFG-03 | Secrets never committed as plaintext; use secret references / vault patterns. |
| CFG-04 | Feature flags must not invent new entities or duplicate SoRs. |
| CFG-05 | Configuration changes that alter approved stack require Architecture Lock / ADR path. |

---

## 17. Database Governance

| Rule | Mandate |
|------|---------|
| DB-01 | Comply with DBS v1.1 and Architecture Lock. |
| DB-02 | One schema ownership per module as locked in ERD. |
| DB-03 | Table prefixes follow locked ERD. |
| DB-04 | Soft-delete · tenant · audit · version stamps per platform standards / ERD. |
| DB-05 | No peer-schema FK invention; UUID attributes for peer refs where locked. |
| DB-06 | Models live under `modules/<module>/models/`. |
| DB-07 | No duplicate entities/tables for the same locked business object. |

---

## 18. Migration Governance

| Rule | Mandate |
|------|---------|
| MIG-01 | Alembic is the sole schema migration tool (Architecture Lock). |
| MIG-02 | Single linear migration history — no parallel Alembic roots. |
| MIG-03 | No duplicate migrations for the same change. |
| MIG-04 | No destructive history rewrite without unanimous PEARB approval. |
| MIG-05 | Phase themes are indicative until implementation assigns revision IDs. |
| MIG-06 | Model discovery imports remain in `alembic/env.py`. |
| MIG-07 | Permission seeds follow established phase-4 patterns where applicable. |

---

## 19. API Governance

| Rule | Mandate |
|------|---------|
| API-01 | Versioned HTTP API under `/api/v1/...`. |
| API-02 | One aggregate module router registered once in shared API v1 router. |
| API-03 | No duplicate mounts for the same resources. |
| API-04 | Routers remain thin; business rules in services/engines. |
| API-05 | Pydantic v2 request/response DTOs in `schemas.py`. |
| API-06 | OpenAPI coherence required at Validation gates. |
| API-07 | RBAC enforced via Foundation dependencies / `permissions.py` constants. |

---

## 20. Security Governance (Repository Aspects)

| Rule | Mandate |
|------|---------|
| SEC-01 | No secrets, keys, or tokens in source or docs. |
| SEC-02 | `secret_ref` patterns only where ERD/FRD require bindings. |
| SEC-03 | Permission constants centralized in module `permissions.py`. |
| SEC-04 | Security tests under `apps/api/src/tests/security/<module>/`. |
| SEC-05 | Do not weaken tenant isolation for convenience. |
| SEC-06 | Security-affecting repository exceptions require PEARB Security Architect review. |

---

## 21. Dependency Governance

| Rule | Mandate |
|------|---------|
| DEP-01 | Dependencies must align with Architecture Lock approved stack. |
| DEP-02 | New major libraries that alter architecture require ADR + PEARB. |
| DEP-03 | Do not reintroduce superseded stacks (NestJS, Prisma, etc.). |
| DEP-04 | Pin/manage dependencies via existing project tooling (`pyproject.toml` / lockfiles as present). |
| DEP-05 | Avoid duplicate libraries for the same concern. |

---

## 22. Testing Repository Governance

| Rule | Mandate |
|------|---------|
| TST-01 | Tests live under `apps/api/src/tests/`. |
| TST-02 | Standard layers: `unit/`, `security/`, `integration/`. |
| TST-03 | Module suites under `tests/<layer>/<module>/` (e.g. `tests/unit/devportal/`). |
| TST-04 | Do not create module-local `modules/<module>/tests/` as the primary suite location. |
| TST-05 | Phase-scoped tests required for PEARB Validation gates. |
| TST-06 | Tooling: Pytest · httpx · Ruff · MyPy as established. |

---

## 23. CI/CD Repository Governance

| Rule | Mandate |
|------|---------|
| CI-01 | CI/CD definitions remain in their established repository locations. |
| CI-02 | Pipelines must not invent a second delivery architecture that bypasses PEARB gates. |
| CI-03 | Release promotion claims require Validation evidence (Master Governance). |
| CI-04 | Toolchain changes that alter Architecture Lock posture require ADR/PEARB. |
| CI-05 | Hotfixes must not silently skip frozen Sprint Lifecycle stages. |

---

## 24. Asset Governance

| Rule | Mandate |
|------|---------|
| AST-01 | Binary/large assets follow existing object-storage patterns (MinIO/S3) — not ad hoc repo dumps. |
| AST-02 | Do not commit large generated artifacts unless already established practice. |
| AST-03 | Document attachments and exports remain outside business SoR tables as binary blobs when standards forbid. |
| AST-04 | UI static assets follow existing frontend app conventions when frontend work is in scope. |

---

## 25. Logging & Monitoring Artifact Governance

| Rule | Mandate |
|------|---------|
| LM-01 | Platform observability tooling guidance in SDD/Architecture Lock remains external/platform concern unless a sprint domain explicitly owns **metadata/control-plane** only. |
| LM-02 | Do not convert the git repository into a telemetry warehouse. |
| LM-03 | Do not commit raw production log/metric/trace dumps. |
| LM-04 | Monitoring/Observability **business module** (when implemented) follows module conventions and locked ERD — metadata only; external APM/log/metrics platforms remain external. |
| LM-05 | Binding secrets never stored as plaintext in repo or tables. |

---

## 26. Version Control Governance

| Rule | Mandate |
|------|---------|
| VC-01 | Use the existing VCS workflow of the repository; do not invent parallel VCS roots. |
| VC-02 | Commits should be intentional and reviewable; do not mix unrelated governance restructures with feature work. |
| VC-03 | Do not force-push protected baselines without explicit organizational policy and PEARB awareness for history rewrite risk. |
| VC-04 | Do not commit secrets. |
| VC-05 | Branching strategies must not create long-lived parallel implementations of the same module. |
| VC-06 | Tags/releases should map to `docs/07_RELEASES/` notes. |

---

## 27. Repository Review Workflow

```text
Change proposal (docs and/or code structure)
        ↓
Repository impact classification
  - Editorial path alignment
  - Additive module scaffold (authorized phase)
  - Structural change (rename/move/reorg)
        ↓
If structural / duplicate / parallel risk → PEARB STOP + review
        ↓
Repository audits (§28) as applicable
        ↓
Quality gates (§29)
        ↓
Approval workflow (§31)
        ↓
Implement only if stage-authorized (phases require Backend Planning + PEARB)
        ↓
Validation evidence includes repository compliance
```

**Hard rule:** Publication of this RC document does **not** authorize Phase implementation.

---

## 28. Repository Audit Checklist

Mandatory audits (select by gate; full set required at Validation / Release readiness):

### 28.1 Repository Audit

- [ ] No unauthorized top-level trees  
- [ ] No parallel app/API stacks  
- [ ] Registrations updated consistently (router · Celery · Alembic · MyPy)

### 28.2 Structure Audit

- [ ] Module layout matches §14  
- [ ] No `schemas/`, `mappers/`, module `config.py`, module-local `tests/` anti-patterns introduced  

### 28.3 Naming Audit

- [ ] Module · schema · prefix · API · RBAC names match locks  
- [ ] File/folder naming standards observed  

### 28.4 Folder Audit

- [ ] Docs placement correct (§11–§12)  
- [ ] No duplicate folders for same concern  

### 28.5 Dependency Audit

- [ ] Stack aligns to Architecture Lock  
- [ ] No superseded frameworks reintroduced  

### 28.6 Security Audit

- [ ] No secrets in repo  
- [ ] Permissions/tests placement correct  

### 28.7 Documentation Audit

- [ ] Stable paths preserved  
- [ ] RC vs Locked status honest  
- [ ] No silent renames/moves  

### 28.8 Sprint Compatibility Audit

- [ ] Lifecycle artifacts in correct sprint folder  
- [ ] Sprint 1–28 paths undisturbed  

### 28.9 Architecture Audit

- [ ] Architecture Lock preserved  
- [ ] Clean Architecture / no peer ORM  

### 28.10 Governance Audit

- [ ] Master Governance / PEARB / Repository Governance not contradicted  
- [ ] PEARB decisions recorded for structural exceptions  

---

## 29. Repository Quality Gates

| Gate Area | Gate IDs | Requirement |
|-----------|----------|-------------|
| **Folder structure** | RQG-FS-01 | Matches §5–§6 and §14 |
| **File naming** | RQG-FN-01 | Matches §8 |
| **Package organization** | RQG-PK-01 | `service/`, `repository/`, `domain/`, `adapters/`, `models/`, `routers/` correct |
| **Imports** | RQG-IM-01 | Established import conventions; layer direction preserved |
| **Documentation** | RQG-DC-01 | Placement §11–§12; locks respected |
| **Testing** | RQG-TST-01 | Global tests layout; phase suites present |
| **Security** | RQG-SEC-01 | No secrets; RBAC artifacts correct |
| **Architecture** | RQG-AR-01 | Architecture Lock + ADR compliance |
| **Governance** | RQG-GV-01 | Parent governance compliance; no unauthorized restructure |
| **Release Readiness** | RQG-REL-01 | Audits complete; Validation accepted; release notes path correct |

**Fail-closed:** Failed repository gate blocks phase completion, Validation accept, or Release authorize as applicable.

---

## 30. Repository Change Management

| Change Type | Examples | Control |
|-------------|----------|---------|
| **Additive compliant** | New module files inside authorized phase scaffold following §14 | Phase authorization + normal review |
| **Editorial docs** | Align BP package refs to repository | PEARB-aware editorial; no architecture change |
| **Structural** | Rename/move docs or packages; new top-level trees | PEARB Class A/B approval **before** change |
| **Exception** | Temporary deviation | Unanimous PEARB · time-boxed · remediation plan |
| **Forbidden** | Duplicates, parallel implementations, Architecture Lock bypass | Reject · STOP |

---

## 31. Repository Approval Workflow

| Step | Action |
|------|--------|
| 1 | Author proposes repository-affecting change with impact notes |
| 2 | Platform Architect (or specialty seat) triage |
| 3 | Run applicable audits (§28) |
| 4 | Apply quality gates (§29) |
| 5 | PEARB vote if Class A/B (unanimous per PEARB Charter) |
| 6 | Record decision · constraints · STOP clearance |
| 7 | Only then execute structural change or authorize phase scaffold |

Approval of Repository Governance RC ≠ approval to implement product phases.

---

## 32. Repository Escalation Process

```text
Detect repository conflict / duplicate / restructure request
        ↓
STOP if Architecture Lock, security, or parallel-implementation risk
        ↓
Platform Architect intake
        ↓
Classify: Editorial · Additive · Structural · Forbidden
        ↓
Forbidden → Reject
Structural / Architecture impact → Full PEARB
Editorial convention conflict → Repository wins → align docs → certify
        ↓
If unresolved in 2 business days → Chief Enterprise Architect mediation
        ↓
If still unresolved → Full PEARB unanimous decision
        ↓
CTO escalation only with PEARB decision intact (no silent override)
```

Aligned to Master Governance conflict resolution:

1. Architecture Lock conflicts → Architecture Lock wins.  
2. Planning vs repository convention conflicts → repository wins; editorial alignment; no architecture change; no implementation on conflicting prescription.

---

## 33. Repository Compliance Rules

All contributors shall:

1. Comply with Master Governance, Architecture Lock, PEARB Charter, and this Repository Governance.  
2. Discover conventions from existing modules before inventing structure.  
3. Keep documentation and sprint report paths stable.  
4. Avoid all duplicate/parallel anti-patterns (RP-05–RP-10).  
5. Obtain PEARB approval before restructuring.  
6. Preserve Sprint 1–28 compatibility.  
7. Treat RC governance docs as non-locked until PEARB locks them.  
8. Produce audit evidence at Validation and Release gates.

Non-compliance is grounds for STOP, rejection, rework, or refusal of release readiness.

---

## 34. Non-Goals

This document **does NOT**:

1. Implement code, migrations, APIs, or tests.  
2. Modify the repository by its publication.  
3. Authorize Phase 0–4 implementation.  
4. Replace Architecture Lock v1.1.  
5. Replace Enterprise Master Governance.  
6. Replace the PEARB Charter.  
7. Reorganize folders or rename existing documents.  
8. Invalidate Sprint 1–28.  
9. Mark itself Locked or Final in this Review Candidate revision.  
10. Create any additional files beyond this single document.

---

## 35. Appendices

### Appendix A — Frozen Sprint Lifecycle (reference)

```text
Architecture Review Board → FRD → ERD Entity Planning → Detailed ERD → Backend Planning
→ Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Validation → Validation Fix → Release → Sprint Completion
```

Repository governance applies at every stage; lifecycle order is not modified by this document.

### Appendix B — Implementation Convention Precedence (normative)

When documentation conflicts with existing repository implementation:

1. Repository implementation conventions win.  
2. Planning documents must be editorially aligned.  
3. Architecture must NOT change.  
4. Implementation must NOT begin on the conflicting prescription.

### Appendix C — Reference Module Peers

Authoritative convention peers include completed modules such as `modules/devportal` and `modules/ai`, and other established `modules/*` packages. New modules must resemble these peers.

### Appendix D — Stable Path Quick Reference

| Concern | Path |
|---------|------|
| Governance | `docs/05_ARCHITECTURE_LOCK/Governance/` |
| Sprint reports | `docs/08_SPRINT_REPORTS/Sprint_NN/` |
| Releases | `docs/07_RELEASES/` |
| Modules | `apps/api/src/modules/<module>/` |
| Tests | `apps/api/src/tests/{unit,security,integration}/<module>/` |
| Shared router | `apps/api/src/shared/router.py` |
| Celery | `apps/api/src/workers/celery_app.py` |
| Alembic env | `apps/api/alembic/env.py` |

---

## 36. Definitions & Glossary

| Term | Definition |
|------|------------|
| **Repository First** | Living code conventions outrank conflicting planning package prescriptions |
| **Implementation Convention Precedence** | Normative four-step conflict rule in Appendix B |
| **PEARB** | Permanent Enterprise Architecture Review Board |
| **RC** | Review Candidate — not Locked |
| **Structural change** | Rename, move, reorganize, or new top-level/documentation root |
| **Additive compliant change** | New files inside authorized module scaffold following §14 |
| **Parallel implementation** | Second package/stack delivering the same capability |
| **Duplicate migration** | Overlapping or forked Alembic change for the same schema delta |
| **Stable path** | Established documentation or code location that must not move without PEARB approval |
| **Anti-pattern** | Structure forbidden because it contradicts repository-wide convention |

---

## 37. Final Governance Statement

The Permanent Enterprise Architecture Review Board hereby publishes **Repository Governance v1.0** as a **Review Candidate (RC)**.

By this document:

- Repository Purpose, Scope, Hierarchy, and Directory Governance are defined.  
- Naming, documentation placement, sprint report placement, and source/module conventions are binding policy.  
- Repository First and Implementation Convention Precedence are restated as permanent operating rules.  
- Duplicate folders/modules/APIs/entities/migrations and parallel implementations are forbidden.  
- Restructuring requires PEARB approval; Sprint 1–28 and stable paths are preserved.  
- Audits, quality gates, change management, approval, and escalation are established.  
- Enterprise Master Governance, PEARB Charter, and Architecture Lock v1.1 remain parent authorities.  

This Review Candidate is **not Locked** and does **not** authorize implementation.

**Repository Governance v1.0 — Review Candidate (RC).**

**Enterprise Master Governance — Respected.**

**PEARB Charter — Respected.**

**Architecture Lock v1.1 — Preserved.**

**Sprint 1–28 — Official Baseline.**

**Repository — Authoritative for Implementation Conventions.**

**Permanent Enterprise Architecture Review Board — Repository Governance Published for Review.**

---

*End of Repository Governance v1.0 — Review Candidate (RC)*
