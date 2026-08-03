# FRD-29 — Monitoring / Observability Domain

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document ID** | FRD-29 |
| **Document Title** | Monitoring / Observability Domain |
| **Domain** | Monitoring / Observability |
| **Version** | **1.1** |
| **Status** | **Locked — Ready for Future Reference** |
| **Classification** | Internal — Confidential |
| **Aligned To** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · FRD-01 Foundation · FRD-21 Integration Hub · FRD-22 Analytics · FRD-27 AI Platform · FRD-28 API Developer Portal · Sprint 29 ARB Recommendation Locked v1.1 · ERP Core v1.23-beta |
| **Sprint** | Sprint 29 (planning) |
| **Predecessor Release** | ERP Core v1.23-beta |
| **Planned Delivery** | ERP Core v1.24-beta (planned) |
| **Next Stage** | ERD-29 Entity Planning |
| **Planned Module (planning)** | `apps/api/src/modules/monitoring/` (or FRD-chosen name at ERD) |
| **Planned API Mount** | `/api/v1/monitoring` (planning) |
| **Schema / Prefix** | TBD under DBS naming standards at ERD-29 (planning hint: `monitoring` / `mon_*` or ERD-chosen) |
| **Business Tables (planning target)** | **~16–18** (ARB range **14–20**; exact count locked at ERD-29) |
| **RBAC Namespace (planning)** | **`monitoring.*`** — Final permission namespace will be confirmed during ERD-29 and permission seed design. |

### Cross References

- Platform: FRD-01 Foundation (Authentication · Authorization · RBAC · Audit · Notification · Workflow Engine) · FRD-02 Organization
- Recommended connectivity projections: FRD-21 Integration Hub (usage metering · transport — **unchanged SoR**)
- Optional reporting projections: FRD-22 Analytics (warehouse SoR unchanged)
- Non-SoR peers: FRD-25 Workflow & BPM Designer · FRD-26 Low-Code · FRD-27 Enterprise AI Platform · FRD-28 API Developer Portal
- External tooling guidance: SDD Observability Architecture (Prometheus · Grafana · Loki · OpenTelemetry · Alerting) — **external platforms remain external**
- Planning baseline: [Sprint 29 Architecture Review Board Recommendation](../08_SPRINT_REPORTS/Sprint_29/Sprint_29_Architecture_Review_Board_Recommendation.md) (Locked v1.1)
- Architecture: Architecture Lock v1.1
- Prior release: ERP Core v1.23-beta

### Related Documents

| Document | Location / Reference |
|----------|----------------------|
| Master-FRD | [Master-FRD.md](./Master-FRD.md) |
| Architecture Lock v1.1 | [ERP_Architecture_Lock_Report_v1.1.md](../05_ARCHITECTURE_LOCK/ERP_Architecture_Lock_Report_v1.1.md) |
| Sprint 29 ARB Recommendation | [Sprint_29_Architecture_Review_Board_Recommendation.md](../08_SPRINT_REPORTS/Sprint_29/Sprint_29_Architecture_Review_Board_Recommendation.md) |
| FRD-01 Foundation | [FRD-01-Foundation-Domain.md](./FRD-01-Foundation-Domain.md) |
| FRD-21 Integration Hub | [FRD-21-Integration-Hub-Enterprise-Platform-Services.md](./FRD-21-Integration-Hub-Enterprise-Platform-Services.md) |
| FRD-22 Analytics | FRD-22 Analytics (warehouse SoR unchanged) |
| FRD-27 AI Platform | [FRD-27-AI-Platform-Domain.md](./FRD-27-AI-Platform-Domain.md) |
| FRD-28 API Developer Portal | [FRD-28-API-Developer-Portal-Domain.md](./FRD-28-API-Developer-Portal-Domain.md) |

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-29 | Initial FRD-29 Monitoring / Observability Draft from Sprint 29 Architecture Review Board Recommendation Locked v1.1. Establishes Observability Metadata and Control Plane. No redesign of prior modules. External observability platforms remain external. No ERD, tables, SQL, migrations, APIs, or implementation. Architecture Lock v1.1 preserved. Next Stage: ERD-29 Entity Planning. |
| 1.1 | 2026-07-29 | Editorial Lock after Permanent Enterprise Architecture Review Board authorization. Normalized section order toward FRD-28 editorial spine; merged Assumptions and Risks; updated RBAC planning note, Phase Gate, Closing Statement, Related Documents (FRD-01 · FRD-22 Analytics), and Integration Contracts title. Metadata Version 1.1 · Status Locked — Ready for Future Reference. No functional, ownership, scope, FR, NFR, Business Rule, risk content, phase, or architecture changes. Ready for ERD-29 Entity Planning. |

---

## 2. Purpose

Provide an **enterprise Monitoring / Observability** domain that enables authenticated **SRE, platform operators, and security/compliance stakeholders** to govern observability **policies, catalogs, SLO/health definitions, alert routing metadata, dashboard definitions, and external platform bindings** — **without becoming** the System of Record for telemetry storage, APM products, log engines, metrics databases, distributed tracing backends, SIEM products, infrastructure monitoring platforms, Foundation Audit warehouse, Integration Hub usage metering, AI gateway telemetry, or Developer Portal DX reports.

This domain becomes the **Observability Metadata and Control Plane authority**. It **does not** become Prometheus, Grafana, Loki, OpenTelemetry collector clusters, cloud APM, SIEM, or a peer-module database writer.

---

## 3. Vision

Establish Monitoring / Observability as the **enterprise observability metadata and control-plane** bounded context for the Modular Monolith:

```text
Business Modules / Platform Modules
        ↓
Foundation (Auth · RBAC · Audit · Notification · Workflow)
        ↓
Monitoring / Observability (metadata · policy · control-plane)
        ↓
Adapters / Contracts
        ↓
External Observability Platforms
(Prometheus · Grafana · Loki · OpenTelemetry · Cloud APM · SIEM)
```

- One governed path for **observability configuration and policy** metadata
- One governed path for **monitored service / component registration** metadata
- One governed path for **metric definition** catalog (definitions only — not time-series storage)
- One governed path for **log and trace policy** metadata (sampling · retention · redaction policies — not stores)
- One governed path for **health-check registration** and **SLO / SLI** definition metadata
- One governed path for **alert rule and routing** metadata (Foundation Notification delivery)
- One governed path for **dashboard / view definition** metadata (not Grafana product ownership)
- One governed path for **external observability platform bindings** (UUID / adapters)
- One governed path for **operational observability reports** (projected via contracts)

Business modules remain **Systems of Record**. Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow authority. Integration Hub remains usage metering / transport SoR. Analytics remains warehouse SoR. AI Platform remains intelligence metadata SoR. Developer Portal remains DX metadata SoR. External observability platforms remain telemetry storage/execution systems.

Monitoring / Observability **consumes** those domains through **service contracts, adapters, and UUID references only**.

### Enterprise Observability Design Principles

| Principle | Statement |
|-----------|-----------|
| **Observability by Default** | Platform modules emit and govern observability signals under enterprise policy before ad-hoc tooling sprawl. |
| **Metadata First** | Monitoring delivers definitions, policies, bindings, SLOs, and alert routing metadata before owning telemetry storage engines. |
| **External Systems Remain External** | Prometheus, Grafana, Loki, OpenTelemetry collectors, cloud APM, and SIEM remain external platforms — never ERP SoR replacements. |
| **Contract First** | Cross-module integration uses published service contracts — never peer ORM. |
| **UUID-only Integration** | Peer references are UUID-only; no peer-schema foreign keys. |
| **Zero Duplicate Ownership** | Monitoring must not duplicate Foundation Audit, Integration Hub usage metering, AI gateway telemetry SoR, or cloud infra monitoring products. |
| **Security by Default** | RBAC, tenant isolation, secret refs, and audit paths apply before operational enablement. |
| **SRE-aligned Control Plane** | SLO/SLI/alert policy metadata supports reliability practice without becoming an incident-management product replacement. |
| **Service-first Communication** | Reads/writes to peer domains occur only through Application Services / adapters. |
| **Backward Compatibility** | Observability policies and dashboard definitions must support controlled versioning where published. |

### Observability Capability Classification

| Term | Meaning |
|------|---------|
| **Capability Classification** | Core / Extension / Future banding of capabilities in this FRD — **no new capabilities beyond ARB Locked v1.1**. |
| **Capability Groups** | Planning organization only for ERD sequencing — **no new capabilities**. |

| Classification | Capabilities |
|----------------|--------------|
| **Core** | Observability configuration / policy metadata · Monitored service / component registry metadata · Metric definition catalog (definitions only) · Log / trace policy metadata · Alert rule / severity / routing metadata · Health check / probe registration metadata · RBAC namespace + Foundation notification/audit integration |
| **Extension** | SLO / SLI definition metadata · Dashboard / view definition metadata · Signal correlation / incident-signal metadata (non-SIEM) · External observability platform bindings (UUID / adapter contracts) · Operational observability reports (projected via contracts) |
| **Future** | Deep APM product · Native metrics TSDB · Native log warehouse · Native distributed-trace backend · Full SIEM · Cloud infrastructure monitoring product · Production observability frontend product (may defer UI) |

---

## 4. Business Objectives

1. Provide a governed enterprise place for observability **policy and definition** metadata across ERP modules.
2. Enable SRE / platform operators to register monitored services, health checks, metric definitions, and alert policies without owning telemetry databases.
3. Bind external observability platforms via adapters/UUID refs while preserving Architecture Lock ownership.
4. Support SLO/SLI and operational report **metadata** for reliability governance.
5. Preserve Foundation Audit as the compliance audit warehouse; Monitoring does not replace audit SoR.
6. Preserve Integration Hub usage metering SoR; Monitoring does not become API usage warehouse.
7. Preserve Analytics warehouse SoR; Monitoring does not become BI/ETL/aggregation engine.
8. Enforce Foundation RBAC (`monitoring.*` planning placeholder) and Foundation workflows where approvals are required.
9. Preserve Architecture Lock v1.1: Clean Architecture, DDD, Modular Monolith, C-01–C-06, no peer ORM writes.
10. Elaborate SDD Observability / Monitoring tooling guidance as an ERP **control-plane metadata** domain without inventing a conflicting telemetry product or redesigning completed modules.

---

## Enterprise Observability Operator Journey

ASCII only. Reflects intended control-plane processes — no workflow redesign of Foundation.

```text
SRE / Platform Operator
        ↓
Observability Policy
        ↓
Service Registration
        ↓
Metric / Log / Trace Policy Definitions
        ↓
Health Check & SLO Definitions
        ↓
Alert Rules & Routing
        ↓
External Platform Binding
        ↓
Operational Reports
```

---

## 5. Scope

Sprint 29 Monitoring / Observability functional requirements for:

- Observability configuration and monitoring policies
- Monitored service / component registration
- Metric definition management (definitions only)
- Log and trace policy management (policies only — not stores)
- Health check management (registration metadata)
- Alert rule management and alert routing policies
- SLO / SLI management
- Dashboard definition management
- External observability platform binding requirements
- Operational reporting requirements
- Workflow, approval, notification, audit, security, compliance, validation, and error-handling requirements
- Integration and non-functional requirements
- Acceptance and ownership boundaries for all existing ERP domains and external platforms

**Correct architectural role (locked by ARB):**

> Monitoring / Observability = enterprise observability configuration · policy · catalog · SLO/alert control-plane metadata, integrating with Foundation, platform modules, and **external** observability systems **through contracts / adapters only**.

---

## 6. Out of Scope

- Redesign of Architecture Lock v1.1 or any locked FRD/ERD (FRD-01 … FRD-28 / ERD-01 … ERD-28)
- Becoming an **APM platform / vendor**
- Becoming a **log storage engine** (Loki / ELK replacement)
- Becoming a **metrics database** (Prometheus TSDB replacement)
- Becoming a **distributed tracing backend** (Jaeger / Tempo / OpenTelemetry collector cluster replacement)
- Becoming a **SIEM**
- Becoming an **infrastructure monitoring product** (cloud infra monitoring replacement)
- Owning Foundation Audit warehouse
- Owning Integration Hub usage metering / transport SoR
- Owning AI gateway / AI telemetry SoR (FRD-27)
- Owning Developer Portal DX operational report SoR (FRD-28)
- Owning Analytics warehouse / BI / ETL / aggregations
- Peer ORM writes or cross-module database access — **C-02**
- Duplicate masters — **C-01**
- High-cardinality raw telemetry ingest into ERP schema
- Production observability frontend product (may defer UI like Sprints 26–28 unless separately authorized)
- Schema, SQL, ERD Mermaid, migrations, routes, models, repositories, services, or implementation prescriptions in this FRD

---

## 7. Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| SRE / Platform Reliability | Governed SLO, health, alert, and dashboard metadata without owning telemetry stores |
| Platform / Module owners | Register monitored services without losing SoR |
| Security / Compliance | Redaction, retention policy metadata, RBAC, audit trails |
| Foundation owners | Preserve Auth / Audit / Notification / Workflow SoR |
| Integration Hub owners | Preserve usage metering / transport SoR |
| Analytics owners | Preserve warehouse SoR; optional projections only |
| AI / Developer Portal owners | Ensure no telemetry/DX report SoR takeover |
| Enterprise Architects | Architecture Lock compliance; zero duplicate ownership; external platforms remain external |
| QA / Validation | Acceptance against FRD gates prior to ERD/implementation |

---

## 8. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-29-001 | System shall provide a Monitoring / Observability control plane for observability policy, catalog, SLO/alert, dashboard definition, and external platform binding **metadata**. |
| FR-29-002 | System shall be the **System of Record for Observability Metadata and Control Plane only** (policies, registries, definitions, alert routing metadata, dashboard definitions, bindings, operational report definitions). |
| FR-29-003 | System shall never become the System of Record for telemetry storage, APM products, log engines, metrics databases, distributed tracing backends, SIEM products, infrastructure monitoring platforms, Foundation Audit warehouse, Integration Hub usage metering, AI gateway telemetry, Developer Portal DX reports, or Analytics warehouse. |
| FR-29-004 | System shall manage **observability / monitoring policies** (retention intent · redaction · sampling policy metadata — not storage engines). |
| FR-29-005 | System shall manage **monitored service / component registration** metadata for ERP modules and platform components. |
| FR-29-006 | System shall manage **metric definition** catalog metadata (names/types/labels definitions only — not time-series database). |
| FR-29-007 | System shall manage **log and trace policy** metadata (classification · sampling · PII redaction · retention intent — not log/trace backends). |
| FR-29-008 | System shall manage **health check / probe registration** metadata (registration only; deep probe-runner product depth remains out of scope unless later FRD authorization). |
| FR-29-009 | System shall manage **alert rule** metadata including severity classification. |
| FR-29-010 | System shall manage **alert routing policies** that route to Foundation Notification channels (Monitoring does not own notification delivery). |
| FR-29-011 | System shall manage **SLO / SLI definition** metadata for reliability governance. |
| FR-29-012 | System shall manage **dashboard / view definition** metadata (not Grafana product ownership). |
| FR-29-013 | System shall manage **external observability platform bindings** via UUID/adapter contracts to Prometheus/Grafana/Loki/OpenTelemetry/cloud APM (and similar) — platforms remain external. |
| FR-29-014 | System shall support **signal correlation / incident-signal metadata** as non-SIEM Extension capability only. |
| FR-29-015 | System shall produce **operational observability reports** with read/export permissions; projections via contracts — Monitoring is not telemetry or usage SoR. |
| FR-29-016 | System shall enforce Foundation Authentication and RBAC namespace **`monitoring.*`** (planning placeholder) for all control-plane actions. |
| FR-29-017 | System shall use Foundation Workflow for policy / binding / critical alert-route approvals where required (C-04). |
| FR-29-018 | System shall emit significant Monitoring mutations to Foundation Audit (C-06); Monitoring does not own the audit warehouse. |
| FR-29-019 | System shall use Foundation Notification for alert/operational notifications (C-05); Monitoring does not own delivery. |
| FR-29-020 | System may integrate with Integration Hub by UUID/contracts only for optional transport/health projections — **no peer ORM**; Hub remains usage SoR. |
| FR-29-021 | System shall never write peer ORM models; all peer mutations occur only via owning module services / adapters. |
| FR-29-022 | System shall enforce tenant isolation on all Monitoring / Observability artifacts. |
| FR-29-023 | System shall not store plaintext secrets/tokens for external platforms; refs/vault patterns only. |
| FR-29-024 | System shall not ingest or persist high-cardinality raw telemetry (metrics/logs/spans) as ERP SoR. |
| FR-29-025 | System shall not own AI gateway telemetry SoR (FRD-27) or Developer Portal DX report SoR (FRD-28). |
| FR-29-026 | System shall support Analytics read-only consumption of control-plane operational metrics where required; Analytics remains reporting SoR. |
| FR-29-027 | System shall support draft / published / retired (or equivalent) lifecycle for versioned policy, dashboard, alert-rule, and binding metadata where versioning applies. |
| FR-29-028 | System shall ensure published observability policy / dashboard / alert-rule / binding versions are not silently replaced (version-first / backward-compatibility principles). |

---

## 9. Capability Requirements (Detailed)

Documentation requirements only. No schema or API prescriptions.

### 9.1 Monitoring Policies

| Concern | Requirement |
|---------|-------------|
| Purpose | Govern tenant/platform observability policy metadata |
| Includes | Retention intent · sampling intent · redaction / PII policy metadata |
| Excludes | Actual log/metric/trace storage engines |
| Lifecycle | Draft → review/approve (where required) → publish → retire |

### 9.2 Service Registration

| Concern | Requirement |
|---------|-------------|
| Purpose | Register which modules/services/components are monitored |
| Includes | Service identity metadata · ownership · environment classification metadata |
| Excludes | Owning the business module SoR or runtime process inventory products |

### 9.3 Metric Definition Management

| Concern | Requirement |
|---------|-------------|
| Purpose | Catalog metric **definitions** (names, types, labels metadata) |
| Excludes | Prometheus TSDB / metrics database ownership |

### 9.4 Log & Trace Policy Management

| Concern | Requirement |
|---------|-------------|
| Purpose | Govern log/trace classification, sampling, redaction, retention **policy metadata** |
| Excludes | Loki/ELK log store · OTel/Jaeger/Tempo tracing backends |

### 9.5 Health Check Management

| Concern | Requirement |
|---------|-------------|
| Purpose | Register health-check / probe metadata for monitored services |
| Excludes | Full infrastructure probe-runner product depth (unless later authorized) |

### 9.6 Alert Rule Management

| Concern | Requirement |
|---------|-------------|
| Purpose | Define alert rules and severity metadata |
| Excludes | SIEM correlation product · security monitoring warehouse |

### 9.7 Alert Routing Policies

| Concern | Requirement |
|---------|-------------|
| Purpose | Route alert notifications through Foundation Notification channels |
| Owner of delivery | Foundation Notification (C-05) |

### 9.8 SLO / SLI Management

| Concern | Requirement |
|---------|-------------|
| Purpose | Define SLO/SLI metadata for reliability governance |
| Excludes | Native SLO evaluation engine as telemetry SoR replacement |

### 9.9 Dashboard Definition Management

| Concern | Requirement |
|---------|-------------|
| Purpose | Store dashboard/view **definition** metadata |
| Excludes | Grafana (or equivalent) product ownership |

### 9.10 External Platform Binding Requirements

| Concern | Requirement |
|---------|-------------|
| Purpose | Bind external observability platforms via adapter/UUID contracts |
| Platforms (examples) | Prometheus · Grafana · Loki · OpenTelemetry · Cloud APM · SIEM |
| Rule | Platforms remain external Systems of Record for telemetry storage/execution |
| Secrets | Refs only — no plaintext tokens in Monitoring tables |

### 9.11 Operational Reporting Requirements

| Concern | Requirement |
|---------|-------------|
| Purpose | Control-plane operational reports (policy coverage, binding status, alert-rule inventory, SLO definition inventory) |
| Projections | Via contracts only — not Analytics warehouse; not Hub usage SoR; not raw telemetry warehouse |
| Permissions | `monitoring.report:read` / `monitoring.report:export` (final codes at seed time) |

---

## 10. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-29-001 | Multi-tenant isolation on all Monitoring / Observability artifacts and reports. |
| NFR-29-002 | Company / branch scoping where enterprise tenancy patterns require it. |
| NFR-29-003 | Soft-delete / retire patterns for mutable control-plane metadata; preserve audit-relevant history. |
| NFR-29-004 | Optimistic concurrency / version stamps on editable drafts. |
| NFR-29-005 | Availability and recoverability aligned with platform ERP SLAs for control-plane services. |
| NFR-29-006 | Observability of the control plane itself: structured logs/metrics for policy publishes, binding failures, and projection failures (without becoming telemetry SoR). |
| NFR-29-007 | Scalability: metadata CRUD only in Sprint 29 backend intent; no high-cardinality telemetry ingest SoR. |
| NFR-29-008 | Security: least privilege; secrets never stored in Monitoring tables. |
| NFR-29-009 | Privacy: PII minimization via redaction **policy metadata**; enforcement may remain external. |
| NFR-29-010 | Resilience: adapter/projection failures must fail safely without inventing telemetry. |
| NFR-29-011 | Compliance: significant actions auditable via Foundation Audit. |
| NFR-29-012 | Performance: interactive control-plane latency suitable for enterprise operations under normal load. |
| NFR-29-013 | Clean Architecture: Router → Service → Engine → Repository → Database; domain independent of transport; Adapter pattern for external platforms. |
| NFR-29-014 | DDD: bounded context for Monitoring / Observability; aggregates aligned at ERD-29. |
| NFR-29-015 | Modular Monolith: new `modules/monitoring` package (or FRD-chosen name); no service-boundary redesign. |
| NFR-29-016 | Extensibility: adapters allow additional external platforms without redesigning completed modules. |

---

## 11. User Roles

| Role | Responsibilities |
|------|------------------|
| **Monitoring Admin** | Full `monitoring.*` including approve / retire / bind; policy and catalog governance |
| **SRE Operator** | SLO/SLI, health checks, alert rules, dashboard definitions, service registration (mid-level) |
| **Service Owner** | Register/update monitored services for owned modules (no approve / admin) |
| **Monitoring Auditor** | Read-only access to policies, bindings, alert history metadata, operational reports |
| **Security / Compliance Officer** | Oversight of redaction/retention policy metadata, RBAC, and external binding secret-ref hygiene |

Roles are realized through Foundation RBAC permission codes; Monitoring does not invent a parallel identity store.

Namespace (planned): **`monitoring.*`**

**RBAC note:** Final permission namespace will be confirmed during ERD-29 and permission seed design.

---

## 12. Actors

| Actor | Description |
|-------|-------------|
| **SRE / Platform Reliability Operator** | Defines policies, SLOs, health checks, alert rules, dashboard definitions |
| **Observability Administrator** | Full control-plane governance and approvals |
| **Module / Service Owner** | Registers monitored services/components for owned modules |
| **Security / Compliance Officer** | Oversight of redaction policies, RBAC, secret-ref hygiene, auditability |
| **Auditor** | Read-only access to policy/publish/alert history and operational reports |
| **External Observability Platform** | Prometheus / Grafana / Loki / OpenTelemetry / cloud APM / SIEM — external systems bound by adapters |
| **Foundation Platform Services** | Auth · RBAC · Audit · Notification · Workflow |
| **Integration Hub** | Optional transport/health projection peer (usage SoR unchanged) |
| **Analytics** | Optional read-only consumer (warehouse SoR unchanged) |

---

## 13. Business Processes

### 13.1 Policy governance
Draft observability policy → submit/approve (where required) → publish → bind to services → retire.

### 13.2 Service registration
Register monitored service/component → associate policies → activate/retire registration metadata.

### 13.3 Definition catalogs
Maintain metric definitions and log/trace policies as versioned metadata; publish without creating telemetry stores.

### 13.4 Reliability definitions
Define health-check registration and SLO/SLI metadata; align to alert rules.

### 13.5 Alerting control-plane
Draft alert rule → severity → routing policy → approve (where required) → publish → route notifications via Foundation Notification.

### 13.6 External binding
Create/update external platform binding (UUID/adapter) → validate ref → activate/retire; secrets remain vault/Hub patterns.

### 13.7 Operational reporting
Generate/export control-plane operational reports under RBAC; projections fail safely without inventing telemetry.

---

## 14. Business Rules

1. **Monitoring is Observability Metadata / Control Plane SoR only.**
2. **External observability platforms remain external** for telemetry storage and execution.
3. **Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow SoR.**
4. **Integration Hub remains usage metering / transport SoR.**
5. **Analytics remains warehouse / BI SoR.**
6. **AI Platform remains intelligence metadata SoR** (including AI-scoped telemetry metadata).
7. **Developer Portal remains DX metadata SoR.**
8. **C-01** — no duplicate masters.
9. **C-02** — no cross-module database access; no peer ORM writes.
10. **C-03** — external connectivity patterns align with Integration Hub / adapters; Monitoring does not own transport.
11. **C-04 / DG-03** — approvals remain Workflow Engine / BPM / Foundation.
12. **C-05** — notifications via Foundation Notification.
13. **C-06** — enterprise audit via Foundation Audit.
14. **No APM / log-store / metrics-DB / trace-backend / SIEM / infra-monitoring product scope.**
15. **No high-cardinality raw telemetry warehouse in ERP schema.**
16. **Secrets never belong in Monitoring tables** — UUID refs / vault keys only.
17. **Published versions are not silently replaced.**
18. **Architecture Lock v1.1 is immutable** for this FRD.
19. **Entity inventory exact count is locked at ERD-29** within ARB target ~16–18 (range 14–20).

---

## 15. Ownership Boundaries

| Concern | Owner |
|---------|--------|
| Observability configuration · policy · catalog · SLO/alert control-plane metadata · dashboard definitions · external platform bindings · operational report definitions | **Monitoring / Observability (this FRD)** |
| Identity · JWT · RBAC · users · Audit warehouse · Notification delivery · Workflow Engine | **Foundation** |
| Connectivity / transport / connectors / webhooks / queues · API usage metering · rate-limit enforcement metadata | **Integration Hub** |
| Enterprise BI / reporting warehouse | **Analytics** |
| Intelligence metadata / AI-scoped telemetry metadata | **AI Platform** |
| Developer Portal DX metadata / DX operational reports | **API Developer Portal** |
| Document file storage | **Document Management** |
| Business transactions / masters | **Business modules / Master Data** |
| Prometheus / Grafana / Loki / OpenTelemetry / cloud APM / SIEM products | **External systems** |

**Forbidden ownership transfers:** none of the completed modules may be redesigned or stripped of SoR to “fit” Monitoring.

### Critical Distinction

| Existing capability | Owner today | Monitoring must **not** become |
|---------------------|-------------|--------------------------------|
| Application / security / DB audit warehouse | Foundation Audit | Second audit SoR / SIEM replacement |
| API usage metering / rate-limit enforcement metadata | Integration Hub | Usage warehouse / gateway metrics SoR |
| AI gateway / cost / guardrail telemetry metadata | AI Platform (scoped) | AI traffic SoR takeover |
| Developer Portal DX operational reports | API Developer Portal | DX report SoR takeover |
| Prometheus / Grafana / Loki / OpenTelemetry | External platforms (SDD tooling) | Native metrics DB · log store · trace backend · APM vendor |
| Notification delivery channels | Foundation Notification (+ Hub transport where defined) | PagerDuty/email product replacement |
| Cloud infrastructure monitoring | Cloud / SRE tooling | Infra monitoring platform product |

---

## 16. Integration Contracts

| System | Integration Pattern |
|--------|---------------------|
| Foundation Security / RBAC | Authentication, authorization, tenant context (`monitoring.*`) |
| Foundation Audit | Policy publish / approve / binding / alert-rule change audit events (C-06) |
| Foundation Notification | Alert and operational notifications (C-05); Monitoring does not own delivery |
| Foundation Workflow / BPM | Policy / binding / critical alert-route approvals (C-04) |
| Organization | Organizational scope without duplicating org masters |
| Integration Hub | Optional UUID/contracts for transport/health projections; usage SoR unchanged; **no peer ORM** |
| Analytics | Optional read-only control-plane report consumption; warehouse SoR unchanged |
| External Observability Platforms | Adapter/UUID bindings only — platforms remain external |
| Business / Platform modules | Contract-only monitored-service registration; never own their data |
| AI Platform / Developer Portal / Low-Code / BPM | None as SoR; optional future UUID hooks only |

**Forbidden:** peer ORM writes; Monitoring-local secret vaults; Monitoring-owned telemetry stores; SIEM/APM/infra-monitoring product replacement.

---

## 17. Security Requirements

| Concern | Requirement |
|---------|-------------|
| Identity | Foundation authentication / session only |
| Authorization | Foundation RBAC `monitoring.*` for all control-plane actions |
| Tenant isolation | Mandatory on policies, registries, definitions, bindings, reports |
| Secret management | Secrets in vault/Hub patterns only; Monitoring stores refs |
| Least privilege | Service Owners receive minimum registration/definition scope |
| Cross-module | No peer DB access; C-02 compliant |
| Abuse prevention | No raw telemetry ingest SoR; fail closed on projection failures |
| External platforms | Adapter contracts only; no impersonation of SIEM/APM products |

---

## 18. Audit Requirements

| Concern | Requirement |
|---------|-------------|
| Audit owner | Foundation Audit (C-06) |
| Audited actions (minimum) | Policy publish/retire · service registration changes · alert rule publish · routing changes · external binding activate/retire · report export |
| Monitoring role | Emit audit events; never become enterprise audit warehouse |
| Retention | Follow Foundation / enterprise retention policy |

---

## 19. Workflow Requirements

| Concern | Requirement |
|---------|-------------|
| Workflow owner | Foundation Workflow Engine (C-04); BPM alignment where required |
| Planned approval classes | Observability policy publish · External platform binding activate · Critical alert routing policy |
| Monitoring role | Initiate / participate in workflows; does not replace Workflow Engine |
| Example workflow codes (planning names) | `MON_POLICY_APPROVAL` · `MON_BINDING_APPROVAL` · `MON_ALERT_ROUTE_APPROVAL` (final codes at ERD/implementation seed time) |

---

## 20. Approval Requirements

| Concern | Requirement |
|---------|-------------|
| Policy publish | Requires authorization; workflow approval where enterprise policy demands |
| External binding activate | Requires authorization; secret-ref hygiene checks |
| Alert routing changes | Requires authorization for production-impacting routes |
| Least privilege | Service Owners cannot approve Admin-class changes |

---

## 21. Notification Requirements

| Concern | Requirement |
|---------|-------------|
| Notification owner | Foundation Notification (C-05) |
| Trigger examples | Alert rule fired metadata events · policy publish · binding failure · report export completion |
| Monitoring role | Emit notification requests; never own SMS/email/PagerDuty delivery |

---

## 22. Compliance Requirements

| Concern | Requirement |
|---------|-------------|
| PII / redaction | Redaction and retention **policy metadata** governed in Monitoring; enforcement may remain external or future-scoped |
| Auditability | Significant actions auditable via Foundation Audit |
| Evidence | Operational reports and publish history support compliance evidence without SIEM ownership |
| Regulatory mapping | Follow enterprise compliance program; Monitoring does not invent a parallel compliance warehouse |

---

## 23. Validation Rules

| Rule | Statement |
|------|-----------|
| V-29-001 | Policy/dashboard/alert-rule/binding identifiers must be unique within tenant/company scope (exact uniqueness model at ERD). |
| V-29-002 | Published artifacts cannot be silently overwritten; new versions required. |
| V-29-003 | Alert routing must reference valid Foundation Notification channel contracts where routing is enabled. |
| V-29-004 | External platform bindings require non-null platform type and authorized reference; secrets not accepted as plaintext. |
| V-29-005 | Metric definitions are metadata-only; system must reject attempts to store raw time-series payloads as SoR. |
| V-29-006 | Log/trace policy artifacts must not accept raw log/span payload warehouses. |
| V-29-007 | Tenant isolation must be enforced on all create/read/update/retire operations. |
| V-29-008 | Soft-delete / retire patterns apply to mutable metadata; preserve audit-relevant history. |

---

## 24. Error Handling

| Condition | Expected behavior |
|-----------|-------------------|
| Unauthorized access | Deny via Foundation RBAC; no data leakage |
| Invalid policy transition | Reject with clear domain error; no partial publish |
| External adapter failure | Fail safely; do not invent telemetry or binding “healthy” state |
| Hub projection failure | Fail safely; do not invent usage/health numbers |
| Secret materialization attempt | Reject; require refs only |
| Concurrent edit conflict | Optimistic concurrency / version stamp failure (NFR) |
| Missing required fields | Validation error; no silent defaults that cross ownership boundaries |

---

## 25. Version Compatibility Policy

Documentation-level compatibility only. No implementation.

| Artifact | Compatibility concern |
|----------|----------------------|
| **Observability Policy Version** | Published observability policy metadata must map to a stable policy identity for tenant/company scope |
| **Dashboard Definition Version** | Dashboard / view definition version must align to the referenced policy and monitored-service set |
| **Alert Rule Version** | Alert rule / severity / routing metadata must reference a compatible policy and notification channel binding |
| **External Platform Binding Version** | Adapter/UUID binding version must track the external observability platform contract without owning telemetry storage |
| **SLO / SLI Definition Version** | Reliability objective definitions must remain compatible with health-check and alert-rule metadata versions |
| **Metric Definition Version** | Metric catalog definition version (names/types/labels metadata only — not time-series storage) |

- Published versions are never silently replaced.
- Version upgrades must be explicit and auditable.
- Existing bindings/routes continue on their resolved versions unless explicitly migrated under policy.

---

## 26. Implementation Phases (Approved — Unchanged)

Per Sprint 29 ARB Recommendation Locked v1.1 — **do not change**:

| Phase | Focus | Intent |
|-------|--------|--------|
| **Phase 0** | Schema shell · module scaffold · Alembic bootstrap · adapters skeleton | Foundation only |
| **Phase 1** | Observability policy · monitored service registry · metric definition catalog · health-check registration | Core control-plane spine |
| **Phase 2** | Log/trace policy metadata · alert rules · severity/routing · Foundation Notification bindings | Alerting control-plane |
| **Phase 3** | SLO/SLI definitions · dashboard/view definitions · external platform bindings (adapters) | Reliability & external integration metadata |
| **Phase 4** | Observability reports · hardening · permissions seed · validation gate | Operational close |

Then: Validation → Validation Fix (if needed) → Release Notes (v1.24-beta planned) → Completion Report — same governance path as Sprints 26–28.

**Entity planning target:** ~16–18 business tables (ARB range 14–20). Exact inventory locked at ERD-29.

---

## Observability Control-Plane Lifecycle

ASCII lifecycle only. Documentation only — no redesign of Foundation workflows.

```text
Draft
        ↓
Review
        ↓
Approve
        ↓
Publish
        ↓
Bind / Route
        ↓
Monitor (external platforms)
        ↓
Retire
```

---

## 27. Risks & Assumptions

### Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-29-01 | Becoming metrics/log/trace **storage SoR** | **Critical** | Hard ownership matrix in this FRD; external platforms remain stores |
| R-29-02 | SIEM / security monitoring product creep | **Critical** | Foundation Audit remains audit warehouse; no SIEM scope |
| R-29-03 | Overlap with Integration Hub usage metering | **High** | Hub remains usage SoR; Monitoring may project via contract only |
| R-29-04 | Overlap with Foundation Audit | **High** | Audit SoR unchanged; Monitoring emits audit events only |
| R-29-05 | Accidental APM / infra monitoring product scope | **High** | Keep SDD tooling external; adapters only |
| R-29-06 | High-cardinality telemetry ingest into ERP DB | **High** | Metadata-only tables; forbid raw telemetry warehouse in ERP schema |
| R-29-07 | Secret/token storage for external platforms in clear text | **High** | Secrets via approved vault/Hub patterns; Monitoring stores refs only |
| R-29-08 | Confusion with AI / Devportal operational reports | **Medium** | Distinct audiences and ownership; UUID/contracts only |

### Assumptions

1. Foundation AuthN/AuthZ/RBAC/Audit/Notification/Workflow remain available platform services.
2. External observability platforms remain the telemetry execution/storage systems (SDD tooling guidance).
3. Architecture Lock v1.1 remains final and unmodified.
4. Sprint 29 follows the established **metadata-first backend** delivery pattern (Sprints 26–28).
5. Frontend may be deferred unless separately authorized.
6. Integration Hub remains usage metering / transport SoR and may expose optional health projection contracts.
7. Analytics remains warehouse SoR and may consume control-plane reports read-only.
8. Exact entity inventory is finalized at ERD-29 within the approved ARB range.
9. SDD Observability / Monitoring sections are tooling guidance elaborated by this FRD as ERP control-plane metadata — not a conflicting product.

---

## 28. Constraints

1. Architecture Lock v1.1 preserved — no modification.
2. No redesign of completed modules (Foundation through API Developer Portal).
3. Monitoring owns observability metadata / policy / control-plane only.
4. Must not become APM vendor, log storage engine, metrics database, distributed tracing backend, SIEM, or infrastructure monitoring platform.
5. External observability platforms remain external.
6. Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow SoR.
7. Integration Hub remains usage / transport SoR.
8. Contracts / UUID / services / adapters only — no peer ORM.
9. No ERD / tables / APIs / migrations in this FRD.
10. Entity inventory target ~16–18 (range 14–20) pending ERD-29 lock.
11. BRD / SDD / DBS — no mandatory redesign.
12. Unanimous Permanent ARB approval required before implementation.

---

## 29. Future Considerations

- Production observability UI over existing control-plane APIs (separately authorized)
- Native telemetry runtimes (explicitly future — not Sprint 29)
- Deeper SRE automation extending alert/SLO metadata without ownership redesign
- Additional external platforms via adapters — do not fork completed modules
- Master FRD consolidation to include FRD-23 … FRD-29 (documentation debt only)

### Documentation-Level Roadmap References

Roadmap references only. No implementation.

| Roadmap Item | Notes |
|--------------|-------|
| **Deeper SLO evaluation automation** | Future automation over locked SLO/SLI metadata without becoming metrics SoR |
| **Expanded adapter catalog** | Additional external platform adapters under the same binding model |
| **Observability UI** | Future operator UI over control-plane APIs |
| **Cross-module signal catalog federation** | Future discovery improvements without peer ORM |
| **Incident workflow hooks** | Future UUID hooks to ITSM/BPM without SIEM ownership |

*(Enhancements must not violate Architecture Lock, C-01–C-06, or ownership boundaries of Foundation, Integration Hub, Analytics, AI, Developer Portal, Document, or business modules, and must not absorb external observability platforms as ERP SoR.)*

---

## 30. Acceptance Criteria

| # | Criterion |
|---|-----------|
| 1 | FRD defines Monitoring / Observability as Observability Metadata and Control Plane SoR without owning telemetry stores |
| 2 | FRD affirms Foundation ownership of AuthN/AuthZ/RBAC/Audit/Notification/Workflow Engine |
| 3 | FRD affirms Integration Hub ownership of usage metering / transport |
| 4 | FRD affirms Analytics / AI / Developer Portal ownership boundaries unchanged |
| 5 | FRD affirms external observability platforms remain external |
| 6 | FRD prohibits APM / log-store / metrics-DB / trace-backend / SIEM / infra-monitoring product scope |
| 7 | FRD prohibits peer ORM writes and duplicate masters (C-01 / C-02) |
| 8 | FRD affirms C-03 / C-04 / C-05 / C-06 boundaries |
| 9 | Core / Extension / Future capability classification matches ARB Recommendation Locked v1.1 |
| 10 | Approved implementation phases match ARB Recommendation without change |
| 11 | Entity planning target ~16–18 (range 14–20) stated; exact inventory deferred to ERD-29 |
| 12 | Risks R-29-01 … R-29-08 preserved with severities |
| 13 | No schema, API, ERD Mermaid, SQL, migrations, or implementation prescriptions included |
| 14 | Architecture Lock v1.1 preserved |
| 15 | Ready for ERD-29 Entity Planning |

---

## 31. Phase Gate

| # | Gate Criterion | Status |
|---|----------------|--------|
| 1 | Documents Monitoring purpose, vision, and SoR boundary (control-plane metadata vs external platforms / Foundation / Hub) | ✅ |
| 2 | Covers required functional, NFR, ownership, integration, security, audit, workflow, notification, compliance, validation, error-handling, and reporting sections without implementation artifacts | ✅ |
| 3 | Affirms Foundation / Integration Hub / Analytics / AI / Developer Portal / external platform ownership splits | ✅ |
| 4 | Affirms C-01–C-06 and no peer ORM writes / UUID-only references / service contracts / adapters | ✅ |
| 5 | Design principles, capability classification, version compatibility, phases, risks preserved from ARB Locked v1.1 | ✅ |
| 6 | No redesign of prior FRDs / Architecture Lock / Sprint 26–28 / ARB Recommendation | ✅ |
| 7 | Ready for ERD-29 Entity Planning | ✅ |

**Documentation status progression (editorial):**

| Status | Meaning |
|--------|---------|
| **Draft** | Documentation complete (FRD content authored; no architectural changes) |
| **Editorial Lock** | Next step after Draft — Permanent ARB editorial authorization applied |
| **Locked — Ready for Future Reference** | After Editorial Lock — document is ready for ERD-29 Entity Planning |

**Phase Gate: PASS — Ready for ERD-29 Entity Planning**

---

### FRD Dependency Summary

| Dependency | Purpose |
|------------|---------|
| Foundation | Identity, RBAC, tenant context, Audit (C-06), Notification delivery (C-05), Workflow Engine (C-04) |
| Organization | Organizational scope without duplicating org masters |
| Integration Hub | Optional transport/health projections; usage SoR unchanged (C-03) |
| Analytics | Optional read-only control-plane report consumption |
| External Observability Platforms | Adapter/UUID bindings; remain telemetry storage/execution SoR |
| Business / Platform Modules | Contract-only monitored-service registration; remain Systems of Record |
| AI / Developer Portal / Low-Code / BPM | No SoR transfer; optional future UUID hooks only |

---

### Document Status

| Field | Value |
|-------|--------|
| **Version** | 1.1 |
| **FRD Status** | Locked |
| **Status** | Locked — Ready for Future Reference |
| **Next Stage** | ERD-29 Entity Planning |
| **Next Artifact** | ERD-29 Entity Planning (not created in this step) |
| **Authoritative Planning Baseline** | Sprint 29 ARB Recommendation Locked v1.1 |

---

## 32. Closing Statement

FRD-29 is now Locked and becomes the baseline for all future ERD, backend implementation, validation, and release activities.

No architectural or ownership changes were introduced.

Architecture Lock v1.1 preserved.

Ready for ERD-29 Entity Planning.
