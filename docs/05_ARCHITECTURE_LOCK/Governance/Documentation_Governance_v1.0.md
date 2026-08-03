# Documentation Governance

## Multi-Industry Enterprise ERP Platform

---

| Field | Value |
|-------|--------|
| **Document Title** | Documentation Governance |
| **Document ID** | DG-01 |
| **Filename (canonical)** | `Documentation_Governance_v1.0.md` |
| **Version** | **1.0** |
| **Status** | **Review Candidate (RC)** |
| **Document Status** | **Review Candidate (RC) — Not Locked** |
| **Classification** | Internal — Confidential |
| **Authority** | Permanent Enterprise Architecture Review Board (PEARB) |
| **Effective Date (proposed)** | 2026-07-29 |
| **Scope** | Creation, review, versioning, approval, locking, referencing, maintenance, amendment, deprecation, and retirement of all enterprise ERP program documents |
| **Parent Governance** | `Enterprise_Master_Governance_v1.0.md` |
| **Board Charter** | `Enterprise_Architecture_Review_Board_v1.0.md` |
| **Repository Governance** | `Repository_Governance_v1.0.md` |
| **Architecture Baseline** | Architecture Lock Report v1.1 |
| **Official Historical Baseline** | Sprint 1 through Sprint 28 (complete) |
| **Current Delivery Context** | Sprint 29 and all subsequent sprints |
| **Repository Location** | `docs/05_ARCHITECTURE_LOCK/Governance/` |
| **Supersedes** | None (first official Documentation Governance) |
| **Does Not Replace** | Enterprise Master Governance · PEARB Charter · Repository Governance · Architecture Lock v1.1 · BRD · FRD · SDD · DBS · ERD · Sprint artifacts |

> **Documentation governance only.** This document defines the permanent documentation standard for the ERP program. It does **not** implement code, modify the repository by publication, authorize implementation, replace Master Governance, replace Repository Governance, or replace Architecture Lock.

---

### Document Control

| Role | Responsibility |
|------|----------------|
| **PEARB** | Author, custodian, and sole amendatory authority for this standard |
| **Documentation & Governance Architect** | Primary specialty owner for documentation lifecycle, status honesty, and placement |
| **Chief Enterprise Architect** | Architecture Review certification for architecture-impacting documents |
| **Platform Architect** | Repository path / convention alignment of documentation references |
| **Delivery Teams / Agents / Vendors** | Mandatory adherence to lifecycle, naming, versioning, and lock rules |

### Version History

| Version | Date | Change | Authority |
|---------|------|--------|-----------|
| **1.0** | 2026-07-29 | Initial Documentation Governance (Review Candidate). Defines document classification, lifecycle (Draft → RC → Architecture Review → Editorial Review → Approval → LOCKED → Future Amendment), status model, versioning, naming, IDs, metadata, templates, editorial/review/approval/lock governance, change management, traceability, cross-references, placement rules, quality gates, audits, and compliance. Complies with Master Governance, PEARB Charter, Repository Governance, Architecture Lock v1.1, and Sprint 1–28 baseline. Does not lock; does not authorize implementation. | PEARB — Review Candidate |

### Document Hierarchy

```text
1. Enterprise Master Governance v1.0
2. Architecture Lock v1.1 (+ locked ADRs)
3. Enterprise Architecture Review Board Charter v1.0
4. Repository Governance v1.0
5. Documentation Governance v1.0 (this document)
6. BRD · SDD · DBS
7. Sprint ARB Recommendation → FRD → ERD → Backend Planning
8. Phase / Validation / Release / Completion artifacts
9. Source code and migrations (must conform upward)
```

This document **shall not** contradict parent governance. Where ambiguity arises, Master Governance conflict resolution, Architecture Lock precedence, and Repository Governance path rules apply.

---

## Table of Contents

1. [Cover Page and Metadata](#1-cover-page-and-metadata)  
2. [Documentation Purpose](#2-documentation-purpose)  
3. [Documentation Scope](#3-documentation-scope)  
4. [Documentation Hierarchy](#4-documentation-hierarchy)  
5. [Document Classification](#5-document-classification)  
6. [Document Lifecycle](#6-document-lifecycle)  
7. [Document Status Model](#7-document-status-model)  
8. [Versioning Standards](#8-versioning-standards)  
9. [Document Naming Standards](#9-document-naming-standards)  
10. [Document ID Standards](#10-document-id-standards)  
11. [Metadata Standards](#11-metadata-standards)  
12. [Document Template Standards](#12-document-template-standards)  
13. [Editorial Governance](#13-editorial-governance)  
14. [Review Governance](#14-review-governance)  
15. [Approval Governance](#15-approval-governance)  
16. [Lock Governance](#16-lock-governance)  
17. [Change Management](#17-change-management)  
18. [Traceability Rules](#18-traceability-rules)  
19. [Cross Reference Rules](#19-cross-reference-rules)  
20. [Repository Documentation Rules](#20-repository-documentation-rules)  
21. [Sprint Documentation Rules](#21-sprint-documentation-rules)  
22. [Governance Documentation Rules](#22-governance-documentation-rules)  
23. [Quality Gates](#23-quality-gates)  
24. [Audit Checklist](#24-audit-checklist)  
25. [Compliance Rules](#25-compliance-rules)  
26. [Non-Goals](#26-non-goals)  
27. [Appendices](#27-appendices)  
28. [Definitions & Glossary](#28-definitions--glossary)  
29. [Final Governance Statement](#29-final-governance-statement)  

---

## 1. Cover Page and Metadata

This section is satisfied by the title block, Document Control, Version History, and Document Hierarchy above. Status remains **Review Candidate (RC)**. Version remains **1.0**. This document is **not Locked** and **not Final**.

---

## 2. Documentation Purpose

Enterprise documentation exists to:

1. Preserve architectural and business intent across sprints.  
2. Provide auditable baselines for PEARB gates, Validation, Release, and Sprint Completion.  
3. Enforce Documentation Lock and Architecture Lock through explicit status and version discipline.  
4. Enable Repository First / Implementation Convention Precedence via accurate path and package references.  
5. Protect Sprint 1–28 historical baselines while enabling controlled future amendment.  
6. Ensure every reader can determine: what the document is, which version is current, whether it is Locked, and what it depends on.

---

## 3. Documentation Scope

### 3.1 In Scope

| Class | Examples |
|-------|----------|
| Governance | Master Governance · PEARB Charter · Repository Governance · Documentation Governance |
| Architecture baselines | Architecture Lock · ADRs · SDD · DBS |
| Business / functional | BRD · FRD |
| Data design | ERD Entity Planning · Detailed ERD |
| Implementation planning | Backend Planning · Sprint ARB Recommendations |
| Delivery evidence | Phase Completion · Validation · Validation Fix · Release · Sprint Completion |
| Cross-cutting metadata | Status · version · IDs · change history · traceability links |

### 3.2 Out of Scope

| Item | Note |
|------|------|
| Source code structure | Repository Governance + Architecture Lock |
| PEARB voting constitution | PEARB Charter |
| Enterprise vision / authority hierarchy | Master Governance |
| Runtime product behavior | FRD / implementation (not this standard) |

### 3.3 Policy Clarification

Documentation Governance defines **how documents are governed**. It does **not** replace the substantive content of Architecture Lock, FRD, ERD, or Backend Planning.

---

## 4. Documentation Hierarchy

### 4.1 Authority Hierarchy (normative)

```text
Master Governance
        ↓
PEARB Charter
        ↓
Repository Governance
        ↓
Documentation Governance (this document)
        ↓
Architecture Lock (+ ADRs)
        ↓
BRD
        ↓
FRD
        ↓
ERD (Entity Planning → Detailed ERD)
        ↓
Backend Planning
        ↓
Implementation (code / migrations)
        ↓
Validation
        ↓
Release
        ↓
Sprint Completion
```

Lower documents must not contradict higher documents. Sprint artifacts must cite their locked baselines.

### 4.2 Placement Hierarchy (stable paths)

Aligned to Repository Governance:

| Root | Content |
|------|---------|
| `docs/01_BRD/` | BRD |
| `docs/02_FRD/` | FRD |
| `docs/03_SDD/` | SDD |
| `docs/04_DBS/` | DBS |
| `docs/05_ARCHITECTURE_LOCK/` | Architecture Lock |
| `docs/05_ARCHITECTURE_LOCK/Governance/` | Governance standards |
| `docs/06_ERD/` | ERD artifacts |
| `docs/07_RELEASES/` | Release notes |
| `docs/08_SPRINT_REPORTS/Sprint_NN/` | Sprint ARB · Backend Planning · Phase/Validation/Completion |

---

## 5. Document Classification

| Class Code | Classification | Sensitivity | Examples |
|------------|----------------|-------------|----------|
| **G** | Governance | Internal — Confidential | EMG · EARB · RG · DG |
| **A** | Architecture Baseline | Internal — Confidential | Architecture Lock · ADR · SDD · DBS |
| **B** | Business | Internal — Confidential | BRD |
| **F** | Functional | Internal — Confidential | FRD |
| **E** | Entity / Data Design | Internal — Confidential | Entity Planning · Detailed ERD |
| **P** | Implementation Planning | Internal — Confidential | Backend Planning · Sprint ARB Recommendation |
| **D** | Delivery Evidence | Internal — Confidential | Phase / Validation / Completion reports |
| **R** | Release | Internal — Confidential | ERP Core release notes |

Documents may carry additional labels (e.g. domain name, sprint number) but must retain a primary class.

---

## 6. Document Lifecycle

### 6.1 Mandatory Lifecycle (frozen for documentation governance)

```text
Draft
  ↓
Review Candidate (RC)
  ↓
Architecture Review
  ↓
Editorial Review
  ↓
Approval
  ↓
LOCKED
  ↓
Future Amendment
```

Stages may not be skipped for Class G, A, F, E, or P documents that become delivery baselines. Delivery Evidence (Class D) and Releases (Class R) follow the same status honesty rules with stage mapping defined in §6.3.

### 6.2 Entry and Exit Criteria

#### Stage 1 — Draft

| | Criteria |
|--|----------|
| **Entry** | Author creates a new document or opens a substantive amendment working copy |
| **Required** | Working title; intended Document ID; intended placement path; dependency list |
| **Exit** | Metadata skeleton complete; scope stated; ready for RC promotion |
| **Forbidden on exit** | Claiming Locked or Final; authorizing implementation |

#### Stage 2 — Review Candidate (RC)

| | Criteria |
|--|----------|
| **Entry** | Draft meets template/metadata minimum; published to stable path (or amendment branch destined for that path) |
| **Required** | Status explicitly **Review Candidate (RC)**; Version set; Change History entry; Non-contradiction claim vs parents |
| **Exit** | Submitted to Architecture Review with complete body |
| **Forbidden** | Treating RC as Locked; silent implementation authorization |

#### Stage 3 — Architecture Review

| | Criteria |
|--|----------|
| **Entry** | RC submitted to PEARB / specialty seats for architecture, ownership, and parent-governance fitness |
| **Required** | Architecture Lock preservation check; SoR/ownership check; hierarchy compliance; Repository First path check where applicable |
| **Exit** | Architecture Review outcome: Pass · Pass with Constraints · Fail (return to Draft/RC) |
| **Fail conditions** | Architecture Lock conflict; ownership breach; parent contradiction; invented paths/conventions |

#### Stage 4 — Editorial Review

| | Criteria |
|--|----------|
| **Entry** | Architecture Review passed (or passed with editorial-only constraints) |
| **Required** | Naming · IDs · metadata · version history · cross-references · spelling/structure · path stability · status honesty |
| **Exit** | Editorial Review outcome: Pass · Pass with minor errata · Fail (return for correction) |
| **Note** | Editorial Review does not redesign architecture or entities |

#### Stage 5 — Approval

| | Criteria |
|--|----------|
| **Entry** | Architecture Review and Editorial Review both Pass (constraints recorded if any) |
| **Required** | PEARB unanimous approval for Class G/A and for sprint baseline locks (FRD/ERD/BP) per PEARB Charter; recorded decision |
| **Exit** | Approval recorded; document eligible for LOCKED transition |
| **Forbidden** | Approval without recorded vote/decision for Class A/B PEARB gates |

#### Stage 6 — LOCKED

| | Criteria |
|--|----------|
| **Entry** | Approval complete; status updated to **Locked** (or sprint-equivalent locked wording); version history records lock event |
| **Required** | Substantive freeze; implementation may rely on this baseline only after required lifecycle stage authorization |
| **Exit** | Remains Locked until Future Amendment process opens a governed change |
| **Forbidden** | Silent redesign during phases; elevating RC to Locked without Approval |

#### Stage 7 — Future Amendment

| | Criteria |
|--|----------|
| **Entry** | PEARB authorizes amendment (Class A/B as applicable) or pre-authorized editorial convention alignment |
| **Required** | Amendment type declared: Editorial · Technical · Substantive; impact on dependents assessed |
| **Exit** | Amended document re-enters lifecycle at Draft or RC as appropriate; prior Locked version retained in history/supersession notes |
| **Rule** | Substantive amendments to locked FRD/ERD/Architecture require PEARB unanimity; editorial convention alignment must not change entities/phases/architecture |

### 6.3 Mapping for Delivery Evidence and Releases

| Artifact | Typical lifecycle expression |
|----------|------------------------------|
| Phase Completion Report | Draft → RC → Editorial Review → Approval (phase gate) → Accepted (phase-closed; not an architecture lock) |
| Validation Report | Draft → RC → PEARB Validation Review → Accepted / Rejected |
| Release Notes | Draft → RC → Release Review → Published |
| Sprint Completion | Draft → RC → PEARB Completion Review → Closed |

These artifacts are **evidence**, not Architecture Lock substitutes. They must still obey naming, metadata, versioning, and placement rules.

---

## 7. Document Status Model

### 7.1 Allowed Status Values

| Status | Meaning | May be cited as delivery baseline? |
|--------|---------|-------------------------------------|
| **Draft** | Work in progress | No |
| **Review Candidate (RC)** | Complete candidate pending reviews/approval | No (planning reference only with caution) |
| **In Architecture Review** | Optional explicit mid-state | No |
| **In Editorial Review** | Optional explicit mid-state | No |
| **Approved** | Approved but not yet Locked (short transitional) | Only if PEARB decision explicitly allows |
| **Locked** | Substantive freeze | Yes |
| **Locked — Ready for Future Reference** | Locked baseline retained for subsequent stages | Yes |
| **Published** | Release notes / public-internal publication | Yes for release claims |
| **Superseded** | Replaced by a newer locked version | Historical only |
| **Deprecated** | Withdrawal path started | No for new work |
| **Archived** | Retained for audit; not active | No for new work |

### 7.2 Status Honesty Rules

| Rule | Mandate |
|------|---------|
| ST-01 | RC ≠ Locked ≠ Final. |
| ST-02 | Do not mark governance docs Locked without PEARB Approval stage completion. |
| ST-03 | Do not remove Locked status without Future Amendment authorization. |
| ST-04 | Document Status field and narrative Closing Statement must agree. |
| ST-05 | “Final” as marketing language is forbidden for RC documents; use Locked/Published as applicable after Approval. |

---

## 8. Versioning Standards

### 8.1 Version Format

`MAJOR.MINOR` (e.g. `1.0`, `1.1`, `2.0`)

| Change type | Version impact | Examples |
|-------------|----------------|----------|
| **Major** | Increment MAJOR; reset MINOR to 0 | Architecture redesign authorization; entity inventory rewrite; governance charter replacement |
| **Minor** | Increment MINOR | Editorial lock additions; convention alignment; non-substantive errata; additive checklists without entity/phase change |
| **Patch** | Not used in filenames by default; record in Change History if needed | Typo-only if PEARB allows without version bump — prefer minor bump for locked docs |

### 8.2 Filename Versioning

Governance and many baselines embed version in filename: `Name_v1.0.md`.  
Sprint artifacts may use document-internal version tables with stable sprint filenames (established practice). Both patterns are allowed; **internal Version field is mandatory** in either case.

### 8.3 Version History Obligation

Every governed document shall include a Change History stating:

- Version  
- Date  
- What changed  
- What did **not** change (for locks/amendments)  
- Authority  

### 8.4 Final Publication

“Final publication” means: Approved + Locked (baselines) or Published (releases), with version history entry and PEARB/stage decision reference. RC documents are never “finally published” as locked baselines.

---

## 9. Document Naming Standards

| Class | Pattern (stable) | Example |
|-------|------------------|---------|
| Governance | `Title_vMAJOR.MINOR.md` | `Documentation_Governance_v1.0.md` |
| Architecture Lock | Established existing names | `ERP_Architecture_Lock_Report_v1.1.md` |
| FRD | `FRD-NN-Domain-Name.md` | `FRD-29-Monitoring-Observability-Domain.md` |
| ERD | `ERD-NN-...` / established variants | `ERD-29-Monitoring-Observability-Detailed-ERD.md` |
| Sprint reports | `Sprint_NN_<Artifact>.md` | `Sprint_29_Backend_Planning.md` |
| Releases | `ERP_Core_vX.Y-beta.md` (or established) | `ERP_Core_v1.23-beta.md` |

**Rules:**

- Do not invent colliding names for the same artifact.  
- Do not rename historical Sprint 1–28 documents without PEARB Class A approval.  
- Prefer consistency with existing sprint naming over novelty.

---

## 10. Document ID Standards

| Class | ID Pattern | Example |
|-------|------------|---------|
| Master Governance | `EMG-NN` | `EMG-01` |
| PEARB Charter | `EARB-NN` | `EARB-01` |
| Repository Governance | `RG-NN` | `RG-01` |
| Documentation Governance | `DG-NN` | `DG-01` |
| Backend Planning | `BP-NN` | `BP-29` |
| FRD | `FRD-NN` | `FRD-29` |
| ERD | `ERD-NN` | `ERD-29` |
| ADR | `ADR-NNN` | `ADR-001` |

IDs are stable identifiers independent of filename tweaks. New ID series require Documentation & Governance Architect + PEARB awareness.

---

## 11. Metadata Standards

Every governed document shall include, at minimum:

| Metadata field | Required |
|----------------|----------|
| Document Title | Yes |
| Document ID | Yes (where ID series applies) |
| Filename (canonical) | Yes for governance; recommended otherwise |
| Version | Yes |
| Status / Document Status | Yes |
| Classification | Yes |
| Authority | Yes |
| Sprint / Domain (if applicable) | Yes when sprint-scoped |
| Architecture Lock baseline reference | Yes for delivery baselines |
| Parent / Aligned To references | Yes |
| Change History | Yes |
| Non-replacement / Non-goals (governance docs) | Yes for Class G |

Optional but recommended: Effective Date, Repository Location, Prior Release, Entity counts (ERD/BP).

---

## 12. Document Template Standards

### 12.1 Minimum Template Skeleton

1. Title  
2. Metadata table  
3. Governance disclaimer (what the doc is / is not)  
4. Document Control  
5. Version History  
6. Hierarchy / Aligned To  
7. Table of Contents (for long documents)  
8. Body sections  
9. Non-Goals (governance and planning docs)  
10. Closing / Final Statement  
11. Appendices as needed  

### 12.2 Sprint Baseline Template Expectations

| Document | Must include |
|----------|--------------|
| Sprint ARB Recommendation | Decision · constraints · Architecture Lock preservation · next stage |
| FRD | Scope · non-goals · ownership · acceptance themes |
| ERD Entity Planning | Exact inventory · aggregates |
| Detailed ERD | Relationships · constraints matching planning |
| Backend Planning | Module path · phases · conventions aligned to repository |
| Phase Completion | Entity progress · remaining work · gate results |
| Validation | Evidence · pass/fail · findings |
| Release | Version · mapped sprint evidence |
| Sprint Completion | Close statement · baselines preserved |

Templates define **structure**, not domain content.

---

## 13. Editorial Governance

| Rule | Mandate |
|------|---------|
| ED-01 | Editorial updates fix clarity, metadata, path notes, and convention alignment. |
| ED-02 | Editorial updates must not change architecture, entities, relationships, phases, roadmaps, or ownership. |
| ED-03 | Editorial convention alignment follows Repository First: repository wins; docs align; architecture unchanged; implementation not begun on conflicting prescription. |
| ED-04 | Editorial changes to Locked docs require PEARB-authorized editorial path and a version history entry (typically minor bump). |
| ED-05 | Spelling/formatting fixes still require status honesty; do not use them to smuggle substantive change. |

---

## 14. Review Governance

| Review type | Owner focus | Required for |
|-------------|-------------|--------------|
| **Architecture Review** | PEARB architecture seats | Class G/A; FRD/ERD/BP locks; ADRs |
| **Editorial Review** | Documentation & Governance Architect (+ Platform Architect for paths) | All baselines before Approval |
| **Security Review** (as applicable) | Security Architect | Docs claiming security controls / permission models |
| **Validation Review** | QA + PEARB | Validation Reports |
| **Release Review** | PEARB Release gate | Release Notes |

Reviews produce Pass / Pass with Constraints / Fail. Constraints must be numbered and testable.

---

## 15. Approval Governance

| Rule | Mandate |
|------|---------|
| AP-01 | Approval follows PEARB Charter voting rules (unanimous for Class A/B material decisions). |
| AP-02 | Approval is recorded (decision log / document history / sprint recommendation). |
| AP-03 | Approval ≠ implementation authorization by itself; stage gates still apply. |
| AP-04 | Conditional Approval requires explicit conditions and re-verification. |
| AP-05 | Rejected documents return to Draft/RC with rejection rationale codes when applicable. |

---

## 16. Lock Governance

| Rule | Mandate |
|------|---------|
| LK-01 | Only Approved documents may become Locked. |
| LK-02 | Locked means substantive freeze. |
| LK-03 | Implementation phases must not redesign Locked FRD/ERD/Architecture. |
| LK-04 | Allowed post-lock changes: PEARB-authorized amendments; authorized editorial convention alignment; authorized errata. |
| LK-05 | Lock event must appear in Version History. |
| LK-06 | RC governance documents (including this one) remain unlockable until Approval → LOCKED completes. |
| LK-07 | “Ready for Future Reference” is a Locked subtype, not an RC synonym. |

---

## 17. Change Management

### 17.1 Change Types

| Type | Description | Control |
|------|-------------|---------|
| **Editorial** | Wording, metadata, path/convention alignment | Authorized editorial path; minor version |
| **Technical** | Corrections that improve accuracy without scope expansion (e.g. wrong path note) | Review + minor version; PEARB if locked |
| **Substantive** | Entities, phases, architecture, ownership, requirements | Future Amendment + PEARB unanimity + major/minor per impact |
| **Deprecation** | Document withdrawn from active use | PEARB approval; status Deprecated → Archived |
| **Archive** | Retained for audit only | Status Archived; path stability preferred over deletion |

### 17.2 Amendment Process

1. Declare amendment type and impacted dependents.  
2. Obtain PEARB authorization when required.  
3. Open Draft/RC working revision.  
4. Complete Architecture + Editorial reviews as applicable.  
5. Approve and Lock (or Publish).  
6. Update cross-references in dependents or record deferred alignment.  

### 17.3 Deprecation Process

1. PEARB decision to deprecate.  
2. Status → Deprecated; successor Document ID/path cited.  
3. No new sprint may use deprecated baseline.  
4. After retention window, Status → Archived (do not delete Sprint 1–28 history).  

### 17.4 Archive Policy

- Prefer status change over file deletion.  
- Do not reorganize archives into new roots without PEARB approval.  
- Sprint 1–28 documents remain discoverable at stable paths.

---

## 18. Traceability Rules

### 18.1 Mandatory Traceability Chain

```text
Master Governance
        ↓
PEARB Charter
        ↓
Repository Governance
        ↓
Documentation Governance
        ↓
Architecture Lock
        ↓
BRD
        ↓
FRD
        ↓
ERD
        ↓
Backend Planning
        ↓
Implementation
        ↓
Validation
        ↓
Release
        ↓
Sprint Completion
```

### 18.2 Traceability Obligations

| Rule | Mandate |
|------|---------|
| TR-01 | Each sprint baseline document lists **Aligned To** / authoritative parents. |
| TR-02 | Backend Planning cites FRD · ERD · Architecture Lock · ARB Recommendation. |
| TR-03 | Phase Completion cites Backend Planning entity targets and actual counts. |
| TR-04 | Validation cites phase evidence and Architecture Lock preservation. |
| TR-05 | Release cites Validation and sprint identity. |
| TR-06 | Sprint Completion cites Release and remaining work honesty. |
| TR-07 | Broken traceability is a documentation quality gate failure. |

---

## 19. Cross Reference Rules

| Rule | Mandate |
|------|---------|
| XR-01 | Prefer stable paths and Document IDs over ambiguous titles only. |
| XR-02 | When citing Locked docs, include version. |
| XR-03 | Do not cite Drafts as authoritative baselines. |
| XR-04 | Cross-references must not invent alternate folder locations. |
| XR-05 | If a reference conflicts with repository reality, apply Repository First and editorially correct the reference. |
| XR-06 | Circular contradictions (A cites B Locked; B contradicts A) require PEARB STOP. |

---

## 20. Repository Documentation Rules

Aligned to Repository Governance:

| Rule | Mandate |
|------|---------|
| RD-01 | Stable documentation paths only. |
| RD-02 | No duplicate documentation trees for the same artifact. |
| RD-03 | No rename/move without PEARB approval. |
| RD-04 | Governance docs live under `docs/05_ARCHITECTURE_LOCK/Governance/`. |
| RD-05 | Package/layout references in docs must match repository conventions (`schemas.py`, `service/`, global tests, etc.). |
| RD-06 | Documentation must not prescribe anti-patterns forbidden by Repository Governance. |

---

## 21. Sprint Documentation Rules

| Rule | Mandate |
|------|---------|
| SD-01 | Sprint artifacts reside under `docs/08_SPRINT_REPORTS/Sprint_NN/`. |
| SD-02 | Frozen Sprint Lifecycle order governs which document is produced next. |
| SD-03 | Each stage document must declare Next Stage. |
| SD-04 | Entity counts and phase maps must remain consistent across FRD → ERD → BP → Completion. |
| SD-05 | Sprint 1–28 reports remain the historical baseline; do not rewrite history. |
| SD-06 | Backend Planning is implementation planning only — not code. |

---

## 22. Governance Documentation Rules

| Rule | Mandate |
|------|---------|
| GD-01 | Class G documents require full lifecycle including Architecture and Editorial Review before Lock. |
| GD-02 | Governance docs must include Non-Goals and parent non-replacement statements. |
| GD-03 | Governance RC documents are not operational locks until Locked. |
| GD-04 | New governance annexes require PEARB authorization and Documentation Governance compliance. |
| GD-05 | Governance docs shall not reorganize `docs/` or authorize implementation by publication. |

---

## 23. Quality Gates

| Gate Area | Gate ID | Requirement |
|-----------|---------|-------------|
| **Metadata** | DQG-MD-01 | Required metadata fields present and consistent |
| **Naming** | DQG-NM-01 | Filename and title match naming standards |
| **Versioning** | DQG-VR-01 | Version + Change History accurate for the change type |
| **Status** | DQG-ST-01 | Status honest; RC not claimed Locked |
| **References** | DQG-XR-01 | Parents/baselines cited with versions; paths stable |
| **Consistency** | DQG-CS-01 | No contradiction with parent governance or sibling sprint artifacts |
| **Completeness** | DQG-CP-01 | Template minimum sections present for document class |
| **Editorial Quality** | DQG-ED-01 | Structure clarity; TOC for long docs; no broken internal logic |
| **Technical Accuracy** | DQG-TA-01 | Architecture/repo references accurate; Repository First observed |
| **Governance Compliance** | DQG-GV-01 | Lifecycle stage appropriate; PEARB rules observed |

**Fail-closed:** Failed documentation gate blocks Approval/Lock and may block dependent sprint stages.

---

## 24. Audit Checklist

### 24.1 Documentation Audit (mandatory at Lock and Validation)

- [ ] Metadata complete  
- [ ] Version/history coherent  
- [ ] Status honest  
- [ ] Placement correct  
- [ ] Traceability chain intact  
- [ ] Cross-references valid  
- [ ] No parent contradictions  
- [ ] Naming/ID standards met  

### 24.2 Editorial Audit

- [ ] No substantive smuggling in “editorial” diffs  
- [ ] Convention alignment only where claimed  
- [ ] Closing statement matches status  

### 24.3 Governance Audit

- [ ] Lifecycle stages evidenced  
- [ ] Approval/lock authority recorded  
- [ ] Non-Goals present for Class G  
- [ ] Sprint 1–28 compatibility preserved  

### 24.4 Sprint Compatibility Audit

- [ ] Correct `Sprint_NN` folder  
- [ ] Lifecycle order respected  
- [ ] Entity/phase consistency across artifacts  

---

## 25. Compliance Rules

All authors and reviewers shall:

1. Obey Master Governance, PEARB Charter, Repository Governance, Documentation Governance, and Architecture Lock.  
2. Use the mandatory document lifecycle and status model.  
3. Maintain traceability and stable paths.  
4. Never treat RC as Locked.  
5. Never redesign Locked baselines during implementation.  
6. Apply Repository First when doc package references conflict with code.  
7. Record versions and authorities for every governed change.  
8. Preserve Sprint 1–28 documentation integrity.  

Non-compliance is grounds for PEARB STOP, rejection, or refusal to Lock/Release.

---

## 26. Non-Goals

This document **does NOT**:

1. Implement code.  
2. Modify the repository by publication.  
3. Authorize implementation phases.  
4. Replace Enterprise Master Governance.  
5. Replace Repository Governance.  
6. Replace Architecture Lock.  
7. Replace the PEARB Charter.  
8. Rename or move existing documentation.  
9. Invalidate Sprint 1–28.  
10. Mark itself Locked or Final in this Review Candidate revision.

---

## 27. Appendices

### Appendix A — Lifecycle Quick Reference

| Stage | Status label | Baseline usable for implementation dependency? |
|-------|--------------|------------------------------------------------|
| Draft | Draft | No |
| RC | Review Candidate (RC) | No |
| Architecture Review | RC / In Architecture Review | No |
| Editorial Review | RC / In Editorial Review | No |
| Approval | Approved (transitional) | Only if PEARB explicitly allows |
| LOCKED | Locked | Yes |
| Future Amendment | Draft/RC working copy + prior Locked retained | Prior Locked remains until replaced |

### Appendix B — Editorial vs Substantive Test

| Question | If Yes |
|----------|--------|
| Does it change entities, relationships, phases, ownership, or architecture? | **Substantive** |
| Does it only align package/path references to repository? | **Editorial** (Repository First) |
| Does it only fix metadata/status honesty/typos? | **Editorial / Technical errata** |

### Appendix C — Parent Conflict Resolution (documentation lens)

1. Conflict with Architecture Lock → Architecture Lock wins; amend doc.  
2. Conflict with repository conventions in planning text → repository wins; editorial alignment; no architecture change; no implementation on conflict.  
3. Conflict among FRD/ERD siblings → PEARB STOP until reconciled.  

### Appendix D — Stable Governance Filenames (current)

| Document | Filename |
|----------|----------|
| Master Governance | `Enterprise_Master_Governance_v1.0.md` |
| PEARB Charter | `Enterprise_Architecture_Review_Board_v1.0.md` |
| Repository Governance | `Repository_Governance_v1.0.md` |
| Documentation Governance | `Documentation_Governance_v1.0.md` |

---

## 28. Definitions & Glossary

| Term | Definition |
|------|------------|
| **RC** | Review Candidate — complete candidate, not Locked |
| **Locked** | Substantive content frozen pending authorized amendment |
| **Editorial update** | Non-substantive change; no entity/architecture/phase change |
| **Technical update** | Accuracy correction without scope expansion |
| **Substantive amendment** | Change to requirements, entities, architecture, ownership, or phases |
| **Final publication** | Approved Locked baseline or Published release — not an RC state |
| **Traceability** | Explicit upward/downward references across the mandatory chain |
| **Status honesty** | Document status fields match actual lifecycle position |
| **Deprecation** | Active withdrawal from use for new work |
| **Archive** | Retained for audit; inactive |
| **Document ID** | Stable identifier (e.g. DG-01) independent of narrative title |

---

## 29. Final Governance Statement

The Permanent Enterprise Architecture Review Board hereby publishes **Documentation Governance v1.0** as a **Review Candidate (RC)**.

By this document:

- Documentation Purpose, Scope, Hierarchy, and Classification are defined.  
- The mandatory document lifecycle and status model are established with entry/exit criteria.  
- Versioning, naming, IDs, metadata, and template standards are binding policy.  
- Editorial, Review, Approval, and Lock governance are specified.  
- Traceability from Master Governance through Sprint Completion is mandatory.  
- Repository and sprint documentation placement rules remain stable and respected.  
- Quality gates and audits protect consistency, completeness, and governance compliance.  
- Parent authorities remain: Master Governance · PEARB Charter · Repository Governance · Architecture Lock v1.1.  

This Review Candidate is **not Locked** and does **not** authorize implementation.

**Documentation Governance v1.0 — Review Candidate (RC).**

**Enterprise Master Governance — Respected.**

**PEARB Charter — Respected.**

**Repository Governance — Respected.**

**Architecture Lock v1.1 — Preserved.**

**Sprint 1–28 — Official Baseline.**

**Permanent Enterprise Architecture Review Board — Documentation Governance Published for Review.**

---

*End of Documentation Governance v1.0 — Review Candidate (RC)*
