# Enterprise Architecture Review Board Charter

## Permanent Enterprise Architecture Review Board (PEARB)

### Multi-Industry Enterprise ERP Platform

---

| Field | Value |
|-------|--------|
| **Document Title** | Enterprise Architecture Review Board Charter |
| **Document ID** | EARB-01 |
| **Filename (canonical)** | `Enterprise_Architecture_Review_Board_v1.0.md` |
| **Version** | **1.0** |
| **Status** | **Review Candidate (RC)** |
| **Document Status** | **Review Candidate (RC) — Not Locked** |
| **Classification** | Internal — Confidential |
| **Authority** | Permanent Enterprise Architecture Review Board |
| **Effective Date (proposed)** | 2026-07-29 |
| **Scope** | Constitution, authority, responsibilities, decision framework, review and approval standards, meeting governance, voting, escalation, quality, and sprint-stage duties of the Permanent Enterprise Architecture Review Board |
| **Parent Governance** | `Enterprise_Master_Governance_v1.0.md` (Review Candidate / foundational charter) |
| **Architecture Baseline** | Architecture Lock Report v1.1 |
| **Official Historical Baseline** | Sprint 1 through Sprint 28 (complete) |
| **Current Delivery Context** | Sprint 29 and all subsequent sprints |
| **Repository Location** | `docs/05_ARCHITECTURE_LOCK/Governance/` |
| **Supersedes** | None (first official PEARB charter) |
| **Does Not Replace** | Enterprise Master Governance · Architecture Lock v1.1 · BRD · FRD · SDD · DBS · ERD · Sprint artifacts |

> **Board charter only.** This document does **not** implement code, modify the repository, redesign architecture, rename documentation, authorize implementation by itself, or override Enterprise Master Governance. It constitutes the Permanent Enterprise Architecture Review Board under Master Governance and Architecture Lock v1.1.

---

### Document Control

| Role | Responsibility |
|------|----------------|
| **Permanent Enterprise Architecture Review Board (PEARB / Permanent ARB)** | Author, custodian, and sole amendatory authority for this charter |
| **Composition** | Thirteen (13) standing architect seats · twenty (20) or more years of enterprise experience each |
| **Decision Rule** | **Unanimous approval** for adoption, amendment, material deviation, Architecture Lock change, and Master Governance amendment |
| **Hierarchy Position** | Below Enterprise Master Governance; equal in operational gatekeeping to Master Governance §10; subordinate to Architecture Lock for technical immutability |
| **CTO / Delivery Leadership** | Operational escalation and compliance enforcement |
| **Delivery Teams / Agents / Vendors** | Mandatory adherence to PEARB decisions and stage gates |

### Change History

| Version | Date | Change | Authority |
|---------|------|--------|-----------|
| **1.0** | 2026-07-29 | Initial Enterprise Architecture Review Board Charter (Review Candidate). Defines board constitution (13 seats), governance authority, responsibilities, decision framework, review and approval standards, meeting governance, voting rules, escalation, quality responsibilities, enterprise review workflow, and sprint-stage duties. Complies with Enterprise Master Governance v1.0, Architecture Lock v1.1, Sprint 1–28 baseline, and current repository structure. Does not lock; does not authorize implementation. | PEARB — Review Candidate |

### Document Hierarchy

```text
1. Enterprise Master Governance v1.0
2. Architecture Lock v1.1 (+ locked ADRs)
3. Enterprise Architecture Review Board Charter v1.0 (this document)
4. BRD · SDD · DBS
5. Sprint ARB Recommendation
6. FRD → ERD Entity Planning → Detailed ERD → Backend Planning
7. Phase / Validation / Release / Completion artifacts
8. Source code and migrations (must conform upward)
```

This charter **shall not** contradict Master Governance or Architecture Lock. Where ambiguity arises, Master Governance conflict-resolution and Architecture Lock precedence apply.

---

## Table of Contents

1. [Purpose and Applicability](#1-purpose-and-applicability)  
2. [Board Constitution](#2-board-constitution)  
3. [Standing Member Charters](#3-standing-member-charters)  
4. [Governance Authority](#4-governance-authority)  
5. [Review Authority](#5-review-authority)  
6. [Decision Framework](#6-decision-framework)  
7. [Decision Matrix](#7-decision-matrix)  
8. [Approval Standards](#8-approval-standards)  
9. [Rejection Standards](#9-rejection-standards)  
10. [Meeting Governance](#10-meeting-governance)  
11. [Voting Rules](#11-voting-rules)  
12. [Escalation Process](#12-escalation-process)  
13. [Enterprise Review Workflow](#13-enterprise-review-workflow)  
14. [Sprint Responsibilities](#14-sprint-responsibilities)  
15. [Quality Responsibilities](#15-quality-responsibilities)  
16. [Quality Gates](#16-quality-gates)  
17. [Governance Responsibilities](#17-governance-responsibilities)  
18. [Non-Goals and Explicit Prohibitions](#18-non-goals-and-explicit-prohibitions)  
19. [Compliance Statement](#19-compliance-statement)  
20. [Final Charter Statement](#20-final-charter-statement)  
21. [Appendix A — Locked Sprint Lifecycle](#appendix-a--locked-sprint-lifecycle)  
22. [Appendix B — Authority Levels](#appendix-b--authority-levels)  
23. [Appendix C — Decision Tree](#appendix-c--decision-tree)  
24. [Appendix D — Definitions and Glossary](#appendix-d--definitions-and-glossary)  

---

## 1. Purpose and Applicability

### 1.1 Purpose

This charter establishes the **Permanent Enterprise Architecture Review Board (PEARB)** — also referred to as the Permanent ARB / Enterprise Architecture Review Board (EARB) in Architecture Lock — as the standing body that:

1. Gates sprint initiation and stage progression under the frozen Sprint Lifecycle.  
2. Protects Architecture Lock v1.1 and Enterprise Master Governance.  
3. Enforces Repository First / Implementation Convention Precedence.  
4. Reviews and approves or rejects architecture, documentation, implementation planning, validation evidence, and release readiness.  
5. Resolves conflicts under Master Governance §13.  
6. Ensures Sprint 1–28 backward compatibility for all future work.

### 1.2 Applicability

This charter applies to all contributors, automated agents, vendors, and delivery leaders operating on the Multi-Industry Enterprise ERP Platform repository and documentation set.

### 1.3 Relationship to Parent Documents

| Document | Relationship |
|----------|--------------|
| Enterprise Master Governance v1.0 | **Parent** — this charter implements Master Governance §10 (Review Board Authority) and related policies; it does **not** override Master Governance |
| Architecture Lock v1.1 | **Binding technical baseline** — PEARB enforces; PEARB may amend only via unanimous decision + ADR |
| Sprint 1–28 | **Official historical baseline** — PEARB preserves compatibility |
| Current `docs/` structure | **Stable** — PEARB does not rename, move, or reorganize existing documents by this charter |

---

## 2. Board Constitution

### 2.1 Legal Standing within the Enterprise Program

The PEARB is a **permanent** board. It is not dissolved between sprints. Seats are standing roles; individuals may rotate, but the thirteen-seat constitution remains unless Master Governance and this charter are amended by unanimous PEARB decision.

### 2.2 Minimum Membership

The board consists of **exactly thirteen (13)** standing architect seats:

| # | Seat |
|---|------|
| 1 | Chief Enterprise Architect |
| 2 | Principal Solution Architect |
| 3 | Enterprise Domain Architect |
| 4 | Platform Architect |
| 5 | Cloud Architect |
| 6 | Infrastructure Architect |
| 7 | Security Architect |
| 8 | Integration Architect |
| 9 | Database Architect |
| 10 | Performance Architect |
| 11 | DevOps Architect |
| 12 | Quality Assurance Architect |
| 13 | Documentation & Governance Architect |

### 2.3 Eligibility

| Requirement | Statement |
|-------------|-----------|
| Experience | Each seat holder shall have **twenty (20) or more years** of relevant enterprise architecture or equivalent senior enterprise delivery experience |
| Independence | Seat holders shall not approve their own unchecked delivery without board quorum rules |
| Continuity | Vacancies must be filled before material unanimous votes that affect Architecture Lock or Master Governance |
| Neutrality | Schedule pressure does not reduce experience or independence requirements |

### 2.4 Quorum

| Vote class | Quorum |
|------------|--------|
| Ordinary stage gate (non-architecture-amendment) | All thirteen seats present or formally delegated with recorded proxy |
| Architecture Lock amendment / ADR / Master Governance amendment / charter amendment | All thirteen seats; **no proxy for dissenting seat** — full personal vote required |
| Emergency Review | Minimum nine (9) seats including Chief Enterprise Architect **or** Principal Solution Architect, with ratification by full board within five (5) business days |

### 2.5 Chair

| Role | Duty |
|------|------|
| **Chair** | Chief Enterprise Architect |
| **Vice-Chair** | Principal Solution Architect |
| **Secretariat** | Documentation & Governance Architect |

The Chair convenes meetings, publishes agendas, and certifies unanimous outcomes. The Vice-Chair acts in the Chair’s absence. The Secretariat maintains decision logs, version history, and artifact traceability.

---

## 3. Standing Member Charters

For each seat, the following dimensions are defined: Mission · Responsibilities · Authority · Decision Rights · Review Scope · Approval Scope · Escalation Responsibility.

### 3.1 Chief Enterprise Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Own enterprise architectural coherence across all domains and sprints; protect Architecture Lock and Master Governance. |
| **Responsibilities** | Chair PEARB; certify stage outcomes; ensure ownership boundaries; prevent parallel architectures; escalate systemic risk. |
| **Authority** | Convene/stop reviews; declare STOP on Architecture Lock conflict; sponsor ADRs. |
| **Decision Rights** | Lead unanimous votes; cast Chair certification; initiate Architecture Lock amendment proposals. |
| **Review Scope** | Cross-domain architecture, modular monolith integrity, Clean Architecture / DDD conformance, sprint fitness. |
| **Approval Scope** | Sprint ARB Recommendations; architecture deviations; release architectural readiness co-sign. |
| **Escalation Responsibility** | Escalate to CTO when delivery pressure threatens Architecture Lock; escalate ownership conflicts to full PEARB. |

### 3.2 Principal Solution Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Ensure end-to-end solution integrity from FRD through release without inventing new platform patterns. |
| **Responsibilities** | Validate solution boundaries; confirm adapter/contract usage; assess phased delivery realism against locked plans. |
| **Authority** | Vice-Chair; halt solution designs that violate SoR ownership or peer-ORM prohibitions. |
| **Decision Rights** | Vote on all gates; co-sponsor solution-level constraints in Sprint ARB Recommendations. |
| **Review Scope** | Solution composition, module interactions, API mount strategy, phased entity progression. |
| **Approval Scope** | Backend Planning coherence; Phase authorization readiness; Validation architectural fitness. |
| **Escalation Responsibility** | Escalate cross-module redesign proposals; escalate “temporary” bypasses of Clean Architecture. |

### 3.3 Enterprise Domain Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Protect domain models, bounded contexts, and FRD/ERD fidelity. |
| **Responsibilities** | Review FRD scope; Entity Planning inventory; Detailed ERD relationships; detect entity drift. |
| **Authority** | Reject domain inventiveness outside locked FRD/ERD; require entity-count integrity. |
| **Decision Rights** | Vote on FRD/ERD locks; require ERD errata via PEARB before implementation proceeds. |
| **Review Scope** | Domain language, aggregates, ownership, UUID-only peer refs, lifecycle semantics. |
| **Approval Scope** | FRD · Entity Planning · Detailed ERD stage approvals (board-level). |
| **Escalation Responsibility** | Escalate SoR disputes; escalate silent entity add/remove/rename attempts. |

### 3.4 Platform Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Preserve modular monolith platform shape, shared kernel patterns, and module packaging conventions. |
| **Responsibilities** | Enforce Repository First; verify `modules/*` convention alignment; prevent duplicate structures. |
| **Authority** | STOP on invented folders/packages; require editorial Backend Planning alignment to repository. |
| **Decision Rights** | Vote on platform deviations; approve convention-alignment editorial actions. |
| **Review Scope** | Package layout, router registration, Celery discovery, Alembic model discovery, DI patterns. |
| **Approval Scope** | Phase 0 scaffold authorization; repository convention compliance at each phase. |
| **Escalation Responsibility** | Escalate proposals for microservices split, second API stack, or shadow packages. |

### 3.5 Cloud Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Ensure cloud deployment posture remains consistent with Architecture Lock (Kubernetes-ready, Terraform-ready) without premature redesign. |
| **Responsibilities** | Review cloud assumptions in SDD/Architecture Lock alignment; reject unapproved cloud product sprawl. |
| **Authority** | Block cloud stack substitutions outside ADR process. |
| **Decision Rights** | Vote on infrastructure-affecting ADRs; advise on multi-environment metadata (not inventing infra SoR in business modules). |
| **Review Scope** | Environment classes, deployment constraints, external platform binding patterns. |
| **Approval Scope** | Cloud-related exceptions; release notes cloud claims accuracy. |
| **Escalation Responsibility** | Escalate unapproved cloud vendor lock-in or architecture fork. |

### 3.6 Infrastructure Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Guard runtime, messaging, cache, storage, and operational infrastructure against Architecture Lock drift. |
| **Responsibilities** | Validate RabbitMQ/Redis/MinIO/S3/PostgreSQL usage remains within approved roles. |
| **Authority** | Reject replacement of locked infrastructure components without ADR. |
| **Decision Rights** | Vote on infra ADRs; constrain module-level infra invention. |
| **Review Scope** | Broker/cache/storage usage, Celery Beat schedules, operational coupling. |
| **Approval Scope** | Infra-affecting Backend Planning claims; release infra readiness. |
| **Escalation Responsibility** | Escalate dual-broker or dual-database proposals. |

### 3.7 Security Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Enforce security, tenancy, RBAC, secret handling, and fail-closed integration behavior. |
| **Responsibilities** | Review permission namespaces; secret_ref patterns; audit expectations; tenant isolation. |
| **Authority** | Reject plaintext secrets in business tables; reject missing RBAC on sensitive routes. |
| **Decision Rights** | Vote on security exceptions; require security gates for Validation/Release. |
| **Review Scope** | AuthN/Z, RBAC, secrets, audit, threat-relevant adapter behavior. |
| **Approval Scope** | Phase 4 permission seed readiness; security test evidence; release security sign-off input. |
| **Escalation Responsibility** | Escalate security debt deferred past Validation without PEARB waiver. |

### 3.8 Integration Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Protect Integration Hub ownership and adapter-only cross-module / external integration patterns. |
| **Responsibilities** | Review ports/adapters; UUID peer refs; external platform bindings; prevent peer ORM. |
| **Authority** | STOP on cross-schema FK invention and peer-module ORM writes. |
| **Decision Rights** | Vote on integration exceptions; constrain Hub vs business SoR boundaries. |
| **Review Scope** | Adapters, contracts, event/notification/workflow initiation patterns. |
| **Approval Scope** | Integration sections of FRD/ERD/Backend Planning; Phase adapter skeletons. |
| **Escalation Responsibility** | Escalate Hub bypass or duplicate transport layers. |

### 3.9 Database Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Enforce DBS v1.1, schema ownership, Alembic governance, and ERD physical fidelity. |
| **Responsibilities** | Review schemas, prefixes, FKs, soft-delete/tenant/audit stamps, migration lineage. |
| **Authority** | Reject migrations that contradict Detailed ERD or DBS; reject destructive history rewrite. |
| **Decision Rights** | Vote on schema exceptions; require ERD lock before business table creation. |
| **Review Scope** | PostgreSQL schemas, ORM models, Alembic revisions, indexes/constraints per ERD. |
| **Approval Scope** | ERD Detailed stage; Phase migration themes; Alembic head integrity at Validation. |
| **Escalation Responsibility** | Escalate schema redesign mid-sprint; escalate peer-schema FK proposals. |

### 3.10 Performance Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Ensure scalability and performance characteristics remain compatible with modular monolith constraints. |
| **Responsibilities** | Review N+1 risks, unbounded list APIs, cache misuse, background job load, false SoR for telemetry. |
| **Authority** | Reject designs that convert control-plane modules into high-volume telemetry warehouses without ARB scope. |
| **Decision Rights** | Vote on performance exceptions; require performance evidence where phase claims demand it. |
| **Review Scope** | Query patterns, pagination, async job design, caching strategy alignment with Master Governance. |
| **Approval Scope** | Performance-related Backend Planning; Validation performance hygiene findings. |
| **Escalation Responsibility** | Escalate uncontrolled fan-out jobs or synchronous remote calls in hot paths. |

### 3.11 DevOps Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Preserve CI/CD, containerization, and operational release discipline without inventing alternate delivery pipelines that bypass gates. |
| **Responsibilities** | Ensure release artifacts, environment promotion claims, and operational checklists align with Validation evidence. |
| **Authority** | Reject “ship without Validation Report”; constrain toolchain changes requiring ADR. |
| **Decision Rights** | Vote on DevOps/toolchain ADRs; co-sign Release operational readiness. |
| **Review Scope** | Docker/K8s-ready posture, migration apply discipline, Celery worker registration. |
| **Approval Scope** | Release stage operational readiness; Validation Fix pipeline hygiene. |
| **Escalation Responsibility** | Escalate hotfixes that skip Sprint Lifecycle stages. |

### 3.12 Quality Assurance Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Own quality gate integrity across unit, security, integration, static analysis, and completion evidence. |
| **Responsibilities** | Verify global test layout compliance; Ruff/MyPy/Pytest expectations; Validation Report sufficiency. |
| **Authority** | Fail Validation gate on missing evidence; limit Validation Fix to hygiene unless PEARB expands scope. |
| **Decision Rights** | Vote on quality waivers; define phase-scoped quality bar with board. |
| **Review Scope** | Tests location/conventions, coverage of RBAC/tenant rules, OpenAPI coherence checks. |
| **Approval Scope** | Validation · Validation Fix · quality portions of Phase Completion Reports. |
| **Escalation Responsibility** | Escalate chronic quality debt; escalate false-green Validation claims. |

### 3.13 Documentation & Governance Architect

| Dimension | Definition |
|-----------|------------|
| **Mission** | Protect documentation lock integrity, naming stability, version history, and governance auditability. |
| **Responsibilities** | Secretariat duties; ensure locked docs are not redesigned; ensure RC vs Locked status is explicit; preserve Sprint 1–28 docs. |
| **Authority** | Reject unauthorized renames/moves; require editorial-only scope for convention alignment. |
| **Decision Rights** | Vote on governance document status transitions; certify document control metadata. |
| **Review Scope** | FRD/ERD/BP/ARB/Completion/Release document control; Master Governance / PEARB charter consistency. |
| **Approval Scope** | Documentation Lock observance; governance document RC → Locked transitions (board-level). |
| **Escalation Responsibility** | Escalate documentation drift, missing version history, or silent status elevation to Locked. |

---

## 4. Governance Authority

PEARB authority covers the following domains. Authority is **gatekeeping and decisioning**, not day-to-day coding.

| Domain | PEARB Authority |
|--------|-----------------|
| **Architecture** | Enforce Modular Monolith · Clean Architecture · DDD; approve ADRs; STOP redesign |
| **Architecture Lock** | Preserve v1.1; amend only by unanimous vote + ADR |
| **Enterprise Governance** | Operate under Master Governance; propose Master Governance amendments |
| **Repository Governance** | Enforce Repository First; forbid duplicate/parallel structures |
| **Documentation Governance** | Enforce Documentation Lock; control RC/Locked transitions for governance docs |
| **Implementation Governance** | Authorize phases; forbid implementation before required locks |
| **Validation Governance** | Accept/reject Validation and Validation Fix scope |
| **Release Governance** | Accept/reject release readiness |
| **Sprint Governance** | Own frozen lifecycle stage gates |
| **FRD** | Approve lock / reject scope drift |
| **ERD** | Approve Entity Planning and Detailed ERD locks |
| **Backend Planning** | Approve lock; require convention alignment to repository |
| **Implementation Phases** | Authorize Phase 0–4 entry/exit |
| **Validation** | Gate evidence sufficiency |
| **Release** | Gate platform release claims |
| **Sprint Completion** | Gate formal sprint close |

PEARB **does not** override Enterprise Master Governance. PEARB **executes** it.

---

## 5. Review Authority

Mandatory review responsibilities (board collectively; seats lead within specialty):

| Review Area | Mandatory PEARB Duty |
|-------------|----------------------|
| **Architecture** | Confirm Architecture Lock preservation; ADR necessity |
| **Repository** | Confirm no invented conventions; modules follow established peers |
| **Folder Structure** | Confirm no unauthorized docs/apps reorganization |
| **Documentation** | Confirm locks, version history, naming stability |
| **Naming** | Confirm schema/prefix/module/API/RBAC naming consistency with locks |
| **Implementation** | Confirm phase scope matches Backend Planning / ERD |
| **Dependencies** | Confirm approved stack; reject unapproved libraries that alter architecture |
| **Imports** | Confirm absolute `modules.*` patterns and layer direction (no domain→ORM pollution) |
| **Security** | Confirm RBAC, tenancy, secrets, audit |
| **Performance** | Confirm pagination, async boundaries, non-SoR telemetry constraints |
| **Scalability** | Confirm modular monolith scalability assumptions hold |
| **Maintainability** | Confirm Clean Architecture layering and engine purity |
| **Coding Standards** | Confirm PY/DG rules from Architecture Lock; Ruff/MyPy expectations |
| **Validation** | Confirm evidence artifacts and fail-closed remediation |
| **Completion Reports** | Confirm honesty of remaining work, entity counts, and gate results |

---

## 6. Decision Framework

### 6.1 Decision Making Principles (binding)

Aligned to Master Governance DM-01–DM-10:

| ID | Principle |
|----|-----------|
| DF-01 | Prefer existing patterns over new patterns. |
| DF-02 | Prefer additive modules over platform redesign. |
| DF-03 | Prefer UUID-only peer references and adapters over peer ORM. |
| DF-04 | Prefer clear SoR ownership over shared mutable tables. |
| DF-05 | Prefer fail-closed integration over invented success states. |
| DF-06 | Prefer explicit locks and reports over informal decisions. |
| DF-07 | Prefer **unanimous** PEARB decisions for material risk. |
| DF-08 | Prefer repository evidence over assumed conventions. |
| DF-09 | Prefer smallest sufficient change preserving Sprint 1–28 compatibility. |
| DF-10 | Prefer validation evidence before release claims. |

### 6.2 Decision Classes

| Class | Examples | Rule |
|-------|----------|------|
| **A — Charter / Lock** | Master Governance amendment; Architecture Lock; this charter; ADRs | Unanimous · full board · recorded |
| **B — Sprint Gate** | ARB Recommendation; FRD/ERD/BP lock; Phase authorize; Validation; Release; Completion | Unanimous · quorum per §2.4 |
| **C — Editorial** | Convention alignment of planning text; path notes; non-substantive errata | Unanimous or Chair+Secretariat certification with board notice if pre-authorized |
| **D — Operational** | Agenda, meeting minutes, evidence checklist formatting | Chair/Secretariat within policy |

---

## 7. Decision Matrix

### 7.1 Approval Matrix

| Outcome | When used |
|---------|-----------|
| **APPROVED** | All gates satisfied; Architecture Lock preserved; no ownership breach |
| **APPROVED WITH CONSTRAINTS** | Approved subject to explicit binding constraints recorded in the decision |
| **CONDITIONALLY APPROVED** | Approved only after enumerated conditions are met and re-verified |
| **DEFERRED** | Insufficient evidence; return to authors without rejection stigma |
| **NOT AUTHORIZED FOR IMPLEMENTATION** | Planning incomplete or convention conflict unresolved |

### 7.2 Rejection Matrix

| Outcome | When used |
|---------|-----------|
| **REJECTED — Architecture** | Violates Architecture Lock / ADR / Clean Architecture |
| **REJECTED — Ownership** | Violates SoR / Foundation / Hub / peer boundaries |
| **REJECTED — Scope** | Entity/API/table drift from locked FRD/ERD |
| **REJECTED — Repository** | Invents conventions, duplicates structures, parallel implementations |
| **REJECTED — Security** | Secrets, RBAC, tenancy, or audit failures |
| **REJECTED — Evidence** | Validation/Completion claims without artifacts |
| **REJECTED — Process** | Lifecycle stage skipped or reordered |

### 7.3 Risk Matrix

| Risk Level | Examples | PEARB Response |
|------------|----------|----------------|
| **Critical** | Architecture Lock breach; peer ORM; secret materialization | Immediate STOP · Class A/B unanimous remediation |
| **High** | SoR boundary blur; lifecycle skip; release without Validation | STOP stage · Rejection or Conditional Approval only |
| **Medium** | Convention drift in planning text; incomplete checklists | Editorial alignment · Deferred until fixed |
| **Low** | Typographical / formatting issues | Secretariat correction · no stage unlock change |

### 7.4 Escalation Matrix

| Trigger | Escalate To | Timebox |
|---------|-------------|---------|
| Architecture Lock conflict | Full PEARB (Class A) | Immediate STOP |
| Planning vs repository convention conflict | Platform Architect → Full PEARB | Before Phase 0 |
| Security finding post-Validation | Security Architect → Full PEARB | Before Release |
| Delivery pressure to skip stage | Chief Enterprise Architect → CTO + Full PEARB | No skip without unanimous waiver |
| Seat disagreement blocking gate | Chair mediation → re-vote | Within 2 business days |
| Emergency production defect | Emergency Review (§10.4) → Full ratification | 5 business days |

### 7.5 RACI Matrix

| Activity | CEA | PSA | EDA | Plat | Cloud | Infra | Sec | Int | DB | Perf | DevOps | QA | DocGov |
|----------|:---:|:---:|:---:|:----:|:-----:|:-----:|:---:|:---:|:--:|:----:|:------:|:--:|:-----:|
| Sprint ARB Recommendation | A | C | C | C | C | C | C | C | C | C | C | C | R |
| FRD Lock | A | C | R | C | I | I | C | C | C | I | I | C | R |
| Entity Planning Lock | A | C | R | C | I | I | C | C | C | I | I | C | R |
| Detailed ERD Lock | A | C | R | C | I | I | C | C | R | C | I | C | R |
| Backend Planning Lock | A | R | C | R | C | C | C | C | C | C | C | C | R |
| Phase 0–4 Authorize | A | R | C | R | C | C | C | C | C | C | C | C | C |
| Validation Accept | A | C | C | C | C | C | C | C | C | C | C | R | R |
| Release Accept | A | C | I | C | C | C | R | C | C | C | R | R | R |
| Architecture Lock Amend | A | R | C | R | R | R | R | R | R | R | R | C | R |
| Master Governance Amend | A | C | C | C | C | C | C | C | C | C | C | C | R |

**Legend:** R = Responsible · A = Accountable · C = Consulted · I = Informed  
**Seat codes:** CEA=Chief Enterprise Architect · PSA=Principal Solution Architect · EDA=Enterprise Domain Architect · Plat=Platform · Sec=Security · Int=Integration · DB=Database · Perf=Performance · DocGov=Documentation & Governance

All **A** rows still require **board unanimity** for Class A/B decisions; RACI does not replace voting rules.

### 7.6 Authority Levels

See [Appendix B — Authority Levels](#appendix-b--authority-levels).

### 7.7 Decision Tree

See [Appendix C — Decision Tree](#appendix-c--decision-tree).

---

## 8. Approval Standards

A stage or artifact may be **Approved** only when all applicable standards hold:

| # | Standard |
|---|----------|
| AS-01 | Architecture Lock v1.1 preserved |
| AS-02 | Enterprise Master Governance principles observed |
| AS-03 | Frozen Sprint Lifecycle stage order respected |
| AS-04 | Prior stage artifacts Locked (where required) and traceable |
| AS-05 | Ownership / SoR boundaries intact |
| AS-06 | No unauthorized entities, tables, peer ORM, or parallel implementations |
| AS-07 | Repository conventions followed or planning editorially aligned |
| AS-08 | Security / tenancy / RBAC expectations addressed for the stage |
| AS-09 | Evidence sufficient for the stage (reports, checklists, counts) |
| AS-10 | Unanimous PEARB decision recorded (Class A/B) |
| AS-11 | Sprint 1–28 compatibility not broken |
| AS-12 | Document control metadata accurate (version, status, history) |

**Approved with Constraints** requires constraints to be written, numbered, and testable at the next gate.

---

## 9. Rejection Standards

Rejection is mandatory when any of the following are true:

| # | Standard |
|---|----------|
| RS-01 | Architecture Lock or ADR violation |
| RS-02 | Master Governance override attempt |
| RS-03 | Lifecycle skip / reorder |
| RS-04 | Entity or relationship drift from locked ERD |
| RS-05 | Invented repository conventions or duplicate structures |
| RS-06 | Implementation begun without required authorization |
| RS-07 | Security-critical defect unmitigated |
| RS-08 | Validation/Release claims without evidence |
| RS-09 | Documentation rename/move/reorganization without PEARB Class A approval |
| RS-10 | Attempt to mark governance docs Locked without unanimous PEARB |

Rejected work returns to the responsible authors with a written rejection matrix code and remediation conditions.

---

## 10. Meeting Governance

### 10.1 Weekly Governance Meeting

| Attribute | Definition |
|-----------|------------|
| **Cadence** | Weekly while any sprint is in active gated stages |
| **Purpose** | Conflict scan, STOP items, convention alignment, upcoming gates |
| **Chair** | Chief Enterprise Architect |
| **Outputs** | Decision log · action list · STOP register |

### 10.2 Sprint Planning Review

| Attribute | Definition |
|-----------|------------|
| **Trigger** | Proposed new sprint / domain |
| **Purpose** | Fitness for lifecycle; ownership; Architecture Lock impact |
| **Outputs** | Sprint ARB Recommendation (approve / approve with constraints / reject) |

### 10.3 Architecture Review

| Attribute | Definition |
|-----------|------------|
| **Trigger** | ADR proposal; Architecture Lock tension; cross-domain redesign risk |
| **Purpose** | Class A decision readiness |
| **Outputs** | ADR accept/reject; STOP or proceed |

### 10.4 Emergency Review

| Attribute | Definition |
|-----------|------------|
| **Trigger** | Production-critical defect or security incident requiring governed exception |
| **Purpose** | Time-boxed exception without silent lifecycle bypass |
| **Rule** | Reduced quorum allowed (§2.4); full-board ratification within five business days |
| **Outputs** | Emergency Decision Record · remediation plan · expiry |

### 10.5 Validation Review

| Attribute | Definition |
|-----------|------------|
| **Trigger** | Validation Report submitted |
| **Purpose** | Evidence sufficiency; scope creep detection; Validation Fix authorization |
| **Outputs** | Accept / Reject / Conditional · Validation Fix scope statement |

### 10.6 Release Review

| Attribute | Definition |
|-----------|------------|
| **Trigger** | Release candidate proposed |
| **Purpose** | Map Validation evidence to release notes; refuse silent ship |
| **Outputs** | Release authorize / reject |

### 10.7 Annual Governance Review

| Attribute | Definition |
|-----------|------------|
| **Cadence** | At least annually |
| **Purpose** | Assess Master Governance, this charter, Quality Gates, and continuous improvement proposals |
| **Constraint** | Improvements must preserve Sprint 1–28 compatibility and frozen lifecycle |
| **Outputs** | Governance Improvement Proposal (if any) · version plan |

---

## 11. Voting Rules

| Rule | Statement |
|------|-----------|
| VR-01 | Class A and Class B decisions require **unanimous** affirmative votes of the sitting board under quorum rules. |
| VR-02 | Abstention on Class A is equivalent to non-approval (blocks unanimity). |
| VR-03 | Dissent must be recorded with rationale; Chair may call one reconsideration after mediation. |
| VR-04 | Proxies are allowed only as defined in §2.4; not for Architecture Lock / Master Governance amendments. |
| VR-05 | Silence is not consent; affirmative recorded vote is required. |
| VR-06 | Emergency decisions require ratification vote; failure to ratify voids the emergency exception prospectively. |
| VR-07 | Editorial Class C actions pre-authorized by prior unanimous decision do not require a new full vote if scope is unchanged. |
| VR-08 | Vote outcomes are published in the sprint decision log / ARB recommendation / completion artifacts as applicable. |

---

## 12. Escalation Process

```text
1. Detect conflict or risk
        ↓
2. Seat-level assessment (specialty architect)
        ↓
3. STOP if Architecture Lock / security / ownership critical
        ↓
4. Chair intake · classify Risk Level (§7.3)
        ↓
5. Mediation (max 2 business days) if non-critical disagreement
        ↓
6. Full PEARB vote (Class A/B as applicable)
        ↓
7. Record decision · constraints · remediation
        ↓
8. If delivery pressure remains → escalate to CTO with PEARB decision intact
        ↓
9. No CTO override of Architecture Lock without new unanimous PEARB + ADR
```

**Hard rule:** Escalation never authorizes skipping the frozen Sprint Lifecycle without unanimous PEARB waiver recorded as Class A/B.

---

## 13. Enterprise Review Workflow

Aligned to Master Governance Approval Workflow and frozen lifecycle:

```text
Proposal / Sprint Intent
        ↓
PEARB Sprint Planning Review → Sprint ARB Recommendation
        ↓
FRD (lock gate)
        ↓
ERD Entity Planning (lock gate)
        ↓
Detailed ERD (lock gate)
        ↓
Backend Planning (lock gate; Repository First alignment)
        ↓
Phase 0 authorize → execute → Phase Completion + gates
        ↓
Phase 1 authorize → execute → Phase Completion + gates
        ↓
Phase 2 authorize → execute → Phase Completion + gates
        ↓
Phase 3 authorize → execute → Phase Completion + gates
        ↓
Phase 4 authorize → execute → Phase Completion + gates
        ↓
Validation Review
        ↓
Validation Fix (if authorized; hygiene-only by default)
        ↓
Release Review
        ↓
Sprint Completion Review
```

Each arrow is a **hard gate**. PEARB may issue STOP at any gate.

---

## 14. Sprint Responsibilities

PEARB responsibilities by frozen lifecycle stage:

| Stage | PEARB Responsibilities |
|-------|------------------------|
| **Architecture Review Board** | Domain fitness; ownership; Architecture Lock impact; constraints; unanimous recommendation |
| **FRD** | Scope lock; SoR clarity; non-goals; reject overreach |
| **Entity Planning** | Inventory lock; aggregate map; entity count integrity |
| **Detailed ERD** | Relationship lock; FK/UUID rules; DBS compliance; no silent redesign |
| **Backend Planning** | Implementation plan lock; Repository First package alignment; phase map; no code delivery in BP |
| **Phase 0** | Authorize scaffold only; verify registrations via existing platform mechanisms; 0 business entities if so planned |
| **Phase 1** | Authorize planned entities only; enforce conventions; phase completion evidence |
| **Phase 2** | Same as Phase 1 for incremental scope |
| **Phase 3** | Same; review adapters/external bindings for ownership safety |
| **Phase 4** | Permissions seed; hardening; final entity count; completion readiness |
| **Validation** | Independent evidence review; fail-closed on missing gates |
| **Validation Fix** | Authorize hygiene-only fixes; forbid feature expansion unless Class B expansion granted |
| **Release** | Authorize release notes accuracy; refuse undocumented claims |
| **Sprint Completion** | Formal close; remaining work honesty; baseline update for next sprint |

---

## 15. Quality Responsibilities

| Area | PEARB Quality Duty |
|------|--------------------|
| **Planning quality** | Locks are complete, consistent, and non-contradictory before implementation |
| **Implementation quality** | Phases match plan; Clean Architecture preserved; no peer ORM |
| **Repository quality** | Conventions stable; no duplicate trees |
| **Security quality** | RBAC/tenant/secret/audit gates enforced |
| **Test quality** | Global test layout; phase-scoped suites meaningful |
| **Documentation quality** | Status honesty (RC vs Locked); version history; no silent renames |
| **Release quality** | Evidence-linked release notes |
| **Governance quality** | Decisions unanimous where required; STOP register maintained |

---

## 16. Quality Gates

Enterprise quality gates administered by PEARB (aligned to Master Governance QG-01–QG-11 and extended for board charter clarity):

### 16.1 Repository Gates

| ID | Gate |
|----|------|
| RG-01 | No unauthorized folder reorganization |
| RG-02 | New modules follow existing `modules/*` conventions |
| RG-03 | Registration via existing router / Celery / Alembic / MyPy mechanisms |
| RG-04 | Tests under global `apps/api/src/tests/` layout |

### 16.2 Architecture Gates

| ID | Gate |
|----|------|
| AG-01 | Architecture Lock v1.1 preserved |
| AG-02 | ADR-001 / ADR-002 respected |
| AG-03 | No parallel architecture or second API stack |
| AG-04 | Ownership / SoR boundaries intact |

### 16.3 Documentation Gates

| ID | Gate |
|----|------|
| DG-01 | Required stage artifact exists and is versioned |
| DG-02 | Locked docs not redesigned during implementation |
| DG-03 | Editorial changes do not alter entities/phases/architecture |
| DG-04 | Governance docs not marked Locked without PEARB unanimity |

### 16.4 Implementation Gates

| ID | Gate |
|----|------|
| IG-01 | Phase scope ⊆ Backend Planning / ERD |
| IG-02 | No peer ORM / unauthorized FKs |
| IG-03 | Engines ORM-free; routers thin |
| IG-04 | Permissions and tenancy enforced on sensitive routes |

### 16.5 Testing Gates

| ID | Gate |
|----|------|
| TG-01 | Pytest suites present for phase scope |
| TG-02 | Security tests for RBAC/tenant as applicable |
| TG-03 | Ruff / MyPy clean for phase scope |

### 16.6 Validation Gates

| ID | Gate |
|----|------|
| VG-01 | Validation Report produced |
| VG-02 | Entity count / schema / ownership scan complete |
| VG-03 | Failures routed to Validation Fix or phase rework correctly |

### 16.7 Release Gates

| ID | Gate |
|----|------|
| RelG-01 | Validation accepted |
| RelG-02 | Release notes under `docs/07_RELEASES/` practice |
| RelG-03 | No silent ship |

### 16.8 Governance Gates

| ID | Gate |
|----|------|
| GG-01 | Unanimous decision recorded for Class A/B |
| GG-02 | Constraints tracked to closure |
| GG-03 | STOP items cleared or explicitly waived |
| GG-04 | Master Governance and this charter not contradicted |

**Fail-closed:** Any failed gate blocks stage passage.

---

## 17. Governance Responsibilities

Collective PEARB governance responsibilities:

1. Maintain the STOP register and decision log.  
2. Protect Sprint 1–28 historical baseline.  
3. Enforce frozen Sprint Lifecycle without modification.  
4. Enforce Repository First and Implementation Convention Precedence.  
5. Preserve Architecture Lock v1.1 until formally amended.  
6. Keep documentation names and folder structure stable.  
7. Ensure RC documents are not treated as Locked.  
8. Authorize only additive, compatible evolution.  
9. Refuse urgency-based governance bypass.  
10. Continuously improve quality **without** breaking compatibility (Master Governance Continuous Improvement Policy).

---

## 18. Non-Goals and Explicit Prohibitions

This document **does NOT**:

1. Implement code, migrations, APIs, or tests.  
2. Modify any existing repository files.  
3. Rename or move existing documentation or folders.  
4. Redesign architecture or amend Architecture Lock by publication alone.  
5. Authorize Phase 0–4 implementation by itself.  
6. Override or supersede Enterprise Master Governance.  
7. Invalidate Sprint 1–28 outcomes.  
8. Reorganize `docs/` or `apps/` structures.  
9. Mark itself Locked or Final in this Review Candidate revision.  
10. Create additional governance documents beyond this single charter file.

**Explicit prohibitions for PEARB members and delivery teams:**

- Never invent architecture.  
- Never invent repository conventions.  
- Never create duplicate structures or parallel implementations.  
- Never skip lifecycle stages.  
- Never treat Review Candidate documents as Locked.  
- Never use schedule pressure to override unanimity.

---

## 19. Compliance Statement

All PEARB actions shall comply with:

1. **Enterprise Master Governance v1.0**  
2. **Architecture Lock Report v1.1** (+ locked ADRs)  
3. **This Enterprise Architecture Review Board Charter v1.0** (when adopted; currently Review Candidate)  
4. Applicable locked BRD · SDD · DBS · FRD · ERD · Backend Planning  
5. Repository First / Implementation Convention Precedence  
6. Frozen Sprint Lifecycle  
7. Sprint 1–28 backward compatibility  

Non-compliance is grounds for STOP, rejection, rework, or refusal of release readiness.

---

## 20. Final Charter Statement

The Permanent Enterprise Architecture Review Board hereby publishes **Enterprise Architecture Review Board Charter v1.0** as a **Review Candidate (RC)**.

By this charter:

- The thirteen-seat board constitution is defined.  
- Governance, review, and approval authorities are specified.  
- Decision, risk, escalation, and RACI matrices are established.  
- Meeting types, voting rules, and enterprise review workflow are declared.  
- Sprint-stage and quality-gate responsibilities are binding for PEARB operations.  
- Enterprise Master Governance remains parent authority.  
- Architecture Lock v1.1 remains preserved.  
- Sprint Lifecycle remains frozen.  
- Sprint 1–28 remains the official historical baseline.  
- Repository structure and existing documentation names remain unmodified by this act.  

This Review Candidate is **not Locked** and **does not** by itself authorize implementation.

**Enterprise Architecture Review Board Charter v1.0 — Review Candidate (RC).**

**Enterprise Master Governance — Respected.**

**Architecture Lock v1.1 — Preserved.**

**Sprint Lifecycle — Frozen.**

**Sprint 1–28 — Official Baseline.**

**Permanent Enterprise Architecture Review Board — Charter Published for Review.**

---

## Appendix A — Locked Sprint Lifecycle

The official lifecycle is frozen and shall not be modified by this charter:

```text
Architecture Review Board
        ↓
       FRD
        ↓
ERD Entity Planning
        ↓
   Detailed ERD
        ↓
 Backend Planning
        ↓
     Phase 0
        ↓
     Phase 1
        ↓
     Phase 2
        ↓
     Phase 3
        ↓
     Phase 4
        ↓
    Validation
        ↓
  Validation Fix
        ↓
      Release
        ↓
 Sprint Completion
```

---

## Appendix B — Authority Levels

| Level | Name | May Decide | May Not Decide Alone |
|-------|------|------------|----------------------|
| L0 | Secretariat | Minutes, formatting, checklist templates | Gates, locks, ADRs |
| L1 | Specialty Seat | STOP recommendation in specialty; draft constraints | Unanimous Class A/B outcomes |
| L2 | Chair / Vice-Chair | Convene, mediate, certify recorded unanimous outcomes | Override dissent; amend Architecture Lock alone |
| L3 | Full PEARB (Unanimous) | All Class A/B decisions; waivers; lock transitions | Contradict physical law of repository evidence without alignment |
| L4 | PEARB + ADR | Architecture Lock / stack amendments | Silent undocumented redesign |

---

## Appendix C — Decision Tree

```text
Is Architecture Lock impacted?
  YES → Class A path → unanimous full board + ADR if amending → Approve / Reject
  NO  ↓
Is a lifecycle stage gate required?
  YES → Class B path → evidence check → unanimous → Approve / Approve with Constraints / Reject / Deferred
  NO  ↓
Is it editorial convention alignment only (no entity/architecture/phase change)?
  YES → Class C path → align planning to repository → record → proceed to next gate when ready
  NO  ↓
Is it operational admin?
  YES → Class D path → Chair/Secretariat
  NO  → Escalate to Chair for classification
```

**Repository conflict branch (mandatory):**

```text
Planning text conflicts with repository conventions?
  → Repository wins
  → Editorial alignment required
  → Architecture unchanged
  → Implementation must NOT begin on conflicting prescription
  → PEARB Platform Architect leads; full board certifies if gate-blocking
```

---

## Appendix D — Definitions and Glossary

| Term | Definition |
|------|------------|
| **PEARB** | Permanent Enterprise Architecture Review Board |
| **Permanent ARB** | Synonym for PEARB used in Master Governance and sprint artifacts |
| **EARB** | Enterprise Architecture Review Board (Architecture Lock synonym) |
| **RC** | Review Candidate — not Locked; not Final |
| **Locked** | Substantive content frozen pending PEARB amendment |
| **Architecture Lock** | ERP Architecture Lock Report v1.1 and locked ADRs |
| **Master Governance** | `Enterprise_Master_Governance_v1.0.md` |
| **Repository First** | Implementation conventions in code outrank conflicting planning prescriptions |
| **SoR** | System of Record |
| **STOP** | Mandatory halt of the gated stage until PEARB resolves the conflict |
| **Class A/B/C/D** | Decision classes defined in §6.2 |
| **Frozen Sprint Lifecycle** | Appendix A stage sequence |
| **Historical baseline** | Sprint 1 through Sprint 28 completed platform state |
| **Unanimous** | All required voting seats affirmatively approve; abstention blocks Class A |

---

*End of Enterprise Architecture Review Board Charter v1.0 — Review Candidate (RC)*
