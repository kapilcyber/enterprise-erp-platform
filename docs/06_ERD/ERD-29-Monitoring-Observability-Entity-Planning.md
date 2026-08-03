# ERD-29 — Entity Planning  
## Monitoring / Observability

| Field | Value |
|-------|--------|
| **Document** | ERD-29 Monitoring / Observability Entity Planning |
| **Version** | **1.1** |
| **Status** | **Locked — Ready for Future Reference** |
| **Document Status** | **Locked** |
| **Next Stage** | **ERD-29 Detailed ERD** |
| **Schema / Prefix (proposed)** | `monitoring` / `mon_` (TBD under DBS naming standards at Detailed ERD) |
| **Business Entities (recommended)** | Exactly **17** (ARB range **14–20**; FRD target **~16–18**) |
| **Aligned To** | FRD-29 (Locked v1.1) · Architecture Lock v1.1 (C-01–C-06) · BRD v1.0 · SDD v1.1 · DBS v1.1 · Sprint 29 ARB Recommendation Locked v1.1 · FRD-01 Foundation · FRD-21 Integration Hub · FRD-22 Analytics · FRD-27 AI Platform · FRD-28 API Developer Portal |
| **Prior Release** | ERP Core v1.23-beta |
| **Planned Delivery** | ERP Core v1.24-beta (planned) |
| **Planned Module (planning)** | `apps/api/src/modules/monitoring/` (or FRD-chosen name at Detailed ERD) |
| **RBAC Namespace (planning)** | **`monitoring.*`** — Final permission namespace confirmed during ERD-29 Detailed ERD and permission seed design |

> **Planning only.** No Mermaid, SQL, columns, indexes, PK/FK diagrams, migrations, APIs, repository design, service layer, Backend Planning, or implementation in this document.

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-29 | Initial Entity Planning for Monitoring / Observability. Recommended inventory of exactly **17** business entities within ARB range 14–20 / FRD target ~16–18. Draft — Ready for Architect Review. No Detailed ERD, Mermaid, SQL, APIs, or implementation. Architecture Lock v1.1 preserved. Next Stage: ERD-29 Detailed ERD. |
| 1.1 | 2026-07-29 | Editorial Lock after Permanent Enterprise Architecture Review Board unanimous approval. Added ASCII Dependency Overview; Recommended Implementation Order; Entity Classification Operational clarification; Versioning Strategy clarification; numbered Entity Dependency Summary; Document Control path note. Metadata Version 1.1 / Locked — Ready for Future Reference. No entity added, removed, or renamed. Still exactly **17** entities. No ownership, aggregate, or architecture changes. Ready for ERD-29 Detailed ERD. |

---

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document ID** | ERD-29-EP |
| **Document Title** | Monitoring / Observability — Entity Planning |
| **Domain** | Monitoring / Observability |
| **Classification** | Internal — Confidential |
| **Authoritative Baselines** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · FRD-29 Locked v1.1 · Sprint 29 ARB Recommendation Locked v1.1 · FRD-01…FRD-28 (locked peers) · ERD-01…ERD-28 |
| **Permanent ARB** | 13 architects · 20+ years enterprise experience each · unanimous approval required |
| **Product Role** | Enterprise Observability Metadata and Control Plane |
| **Repository Path Note** | Sprint 29 Entity Planning is stored under `docs/03_ERD/`. Historical Sprint 26–28 Entity Planning documents may use `docs/06_ERD/`. Documentation organization only — no repository restructuring. |

---

## 2. Entity Planning Objectives

Entity Planning freezes the **complete business-entity inventory** for the Monitoring / Observability domain before Detailed ERD and backend implementation.

Later ERD design and implementation **must use only these entities**. No new Monitoring / Observability entities may appear during implementation without formal Permanent Enterprise Architecture Review Board approval.

This document exists to:

- Translate FRD-29 Locked v1.1 capabilities into a governed entity set of exactly **17** entities
- Preserve Architecture Lock v1.1 and cross-module ownership boundaries
- Prevent over-normalization and SoR duplication with Foundation Audit, Integration Hub usage metering, Analytics warehouse, AI Platform telemetry metadata, Developer Portal DX reports, and external observability platforms
- Provide a planning baseline for ERD-29 Detailed ERD

**Monitoring / Observability owns observability metadata / policy / control-plane only.**  
**External observability platforms remain external. Foundation remains security / audit / notification / workflow SoR. Integration Hub remains usage / transport SoR.**

---

## 3. Planning Principles

| Principle | Application |
|-----------|-------------|
| **Observability Metadata / Control Plane only** | Policies, registries, definitions, alert routing metadata, dashboard definitions, bindings, operational report definitions — not telemetry storage engines |
| **External systems remain external** | Prometheus · Grafana · Loki · OpenTelemetry · cloud APM · SIEM remain external platforms — never ERP SoR replacements |
| **Zero duplicate ownership** | Never duplicate Foundation Audit, Integration Hub usage metering, AI gateway telemetry SoR, Developer Portal DX reports, or Analytics warehouse |
| **UUID references only** | Peer domains referenced by UUID / contracts — never peer-schema FKs |
| **No peer ORM** | Monitoring never writes peer-module ORM models |
| **Secret refs only** | External platform secret materialization forbidden; vault/Hub pattern refs as attributes — no Monitoring secret-store entity |
| **Version-first control plane** | Publishable policy / alert / dashboard / binding / SLO metadata follow Draft → Publish → Retire; published versions are never silently replaced |
| **Avoid over-normalization** | Justified merges only (see coverage mapping) |
| **Foundation ownership preserved** | AuthN · AuthZ · RBAC · Audit · Notification · Workflow Engine unchanged |
| **Integration Hub ownership preserved** | Usage metering · transport · connectors unchanged |
| **Clean Architecture · DDD · Modular Monolith** | Required at implementation time; not prescribed here as schema |
| **Repository · Service · Engine · Adapter · DI** | Preserved architecture patterns at implementation — not designed in this document |

---

## 4. Architecture Principles (Preserved)

| Principle | Status |
|-----------|--------|
| Modular Monolith | Preserved |
| Clean Architecture | Preserved |
| DDD | Preserved |
| UUID-only references | Preserved |
| Repository Pattern | Preserved (implementation later) |
| Service Layer | Preserved (implementation later) |
| Engine Layer | Preserved (implementation later) |
| Adapter Pattern | Preserved (external platforms) |
| Dependency Injection | Preserved (implementation later) |
| Foundation ownership | Preserved |
| Integration Hub ownership | Preserved |
| No Peer ORM | Preserved |

---

## 5. Estimated Entity Count

| Estimate | Count | Rationale |
|----------|------:|-----------|
| **ARB planning range** | **14–20** | Focused control-plane envelope — not a telemetry warehouse |
| **FRD target** | **~16–18** | Policy · registry · definitions · alerts · SLO · dashboards · bindings · reports |
| **This Entity Planning recommendation** | **Exactly 17** | Mid-target; justified merges applied; no storage/APM/SIEM entities |
| **Final lock** | Detailed ERD | Exact count locked during ERD-29 Detailed ERD within range 14–20 |

**Not a metrics warehouse. Not a 34-class AI-scale inventory.**

---

## 6. Entity Classification

Documentation categories only. No implementation. Recommended count remains exactly **17**.

**Editorial clarification:** **Operational** is an Entity Planning classification only. It does **not** redefine FRD-29 capability classification (Core / Extension / Future). FRD capability banding remains unchanged — including operational observability reports under FRD Extension capability banding where stated.

| Classification | Entities |
|----------------|----------|
| **Core** | `mon_observability_policy` · `mon_observability_policy_version` · `mon_monitored_service` · `mon_monitored_component` · `mon_metric_definition` · `mon_log_trace_policy` · `mon_health_check` · `mon_alert_rule` · `mon_alert_routing_policy` · `mon_service_policy_assignment` |
| **Extension** | `mon_slo_definition` · `mon_sli_definition` · `mon_dashboard_definition` · `mon_signal_correlation` · `mon_external_platform_binding` · `mon_service_platform_assignment` |
| **Operational** | `mon_observability_report` |
| **Future Ready** | *(none as Sprint 29 entities — see Future Entity Considerations)* |

---

## 7. Candidate Business Entities — Coverage → Entity Mapping

| FRD / Planning Concern | Entity Decision |
|------------------------|-----------------|
| Observability / monitoring policy identity | `mon_observability_policy` |
| Observability policy version (Draft → Publish → Retire) | `mon_observability_policy_version` |
| Monitored service / module registration | `mon_monitored_service` |
| Monitored component registration | `mon_monitored_component` (kept separate — first-class component registry) |
| Metric definition catalog | `mon_metric_definition` |
| Log policy · Trace policy | **Merged** into `mon_log_trace_policy` (policy kind / signal class) |
| Health check / probe registration | `mon_health_check` |
| Alert rule · severity | `mon_alert_rule` |
| Alert routing to Foundation Notification | `mon_alert_routing_policy` (Notification channel UUID refs as attributes — no delivery entity) |
| SLO definition | `mon_slo_definition` |
| SLI definition | `mon_sli_definition` (kept separate for reliability governance clarity) |
| Dashboard / view definition | `mon_dashboard_definition` |
| Signal correlation / incident-signal metadata (non-SIEM) | `mon_signal_correlation` |
| External observability platform bindings · secret refs | `mon_external_platform_binding` (**secret refs merged as attributes** — no Monitoring vault entity) |
| Service ↔ policy assignment | `mon_service_policy_assignment` |
| Service ↔ external platform assignment | `mon_service_platform_assignment` |
| Operational observability reports | `mon_observability_report` |
| AuthN/AuthZ/RBAC/JWT · Audit warehouse · Notification delivery · Workflow Engine | **Not Monitoring entities** — Foundation |
| API usage metering · transport · connectors | **Not Monitoring entities** — Integration Hub |
| Analytics warehouse / BI / ETL | **Not Monitoring entities** — Analytics |
| AI gateway / AI telemetry SoR | **Not Monitoring entities** — AI Platform |
| Developer Portal DX operational reports | **Not Monitoring entities** — API Developer Portal |
| Prometheus / Grafana / Loki / OTel / cloud APM / SIEM products | **Not Monitoring entities** — External platforms |
| Raw metrics / logs / spans warehouse · APM · SIEM · infra monitoring | **Out of scope** — forbidden |

---

## 8. Entity Inventory

Exactly **17** entities. Recommended inventory only — final lock at Detailed ERD within ARB range.

### 1. `mon_observability_policy`

| Field | Value |
|-------|--------|
| **Entity Name** | Observability Policy |
| **Purpose** | Stable identity for tenant/platform observability policy metadata (retention intent · sampling · redaction / PII policy governance). |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Policy Governance |
| **Merge rationale** | — |
| **Notes** | Does not own log/metric/trace storage engines. |

### 2. `mon_observability_policy_version`

| Field | Value |
|-------|--------|
| **Entity Name** | Observability Policy Version |
| **Purpose** | Versioned publishable unit of an observability policy (Draft / Published / Retired); published versions are immutable. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Policy Governance |
| **Merge rationale** | Kept separate from Policy identity for version-first / Version Compatibility Policy alignment. |
| **Notes** | Approvals via Foundation Workflow where required (C-04). |

### 3. `mon_monitored_service`

| Field | Value |
|-------|--------|
| **Entity Name** | Monitored Service |
| **Purpose** | Registration metadata for ERP modules / platform services subject to observability governance. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Service Registry |
| **Merge rationale** | — |
| **Notes** | Does not own business module SoR or runtime process inventory products. Peer modules referenced by UUID / module code only. |

### 4. `mon_monitored_component`

| Field | Value |
|-------|--------|
| **Entity Name** | Monitored Component |
| **Purpose** | Component-level registration metadata under a monitored service. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Service Registry |
| **Merge rationale** | Kept separate from Service per FRD service/component registry requirement. |
| **Notes** | Metadata only — not an infrastructure CMDB product. |

### 5. `mon_metric_definition`

| Field | Value |
|-------|--------|
| **Entity Name** | Metric Definition |
| **Purpose** | Catalog of metric **definitions** (names, types, labels metadata). |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Signal Catalog |
| **Merge rationale** | Label metadata kept as attributes — no separate label-dictionary entity. |
| **Notes** | Not a Prometheus TSDB / metrics database. Must reject raw time-series SoR intent. |

### 6. `mon_log_trace_policy`

| Field | Value |
|-------|--------|
| **Entity Name** | Log / Trace Policy |
| **Purpose** | Log and trace classification, sampling, PII redaction, and retention **policy metadata**. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Signal Catalog |
| **Merge rationale** | **Log policy + Trace policy merged** via signal/policy kind (avoid over-normalization). |
| **Notes** | Not Loki/ELK log store · not OTel/Jaeger/Tempo tracing backends. |

### 7. `mon_health_check`

| Field | Value |
|-------|--------|
| **Entity Name** | Health Check |
| **Purpose** | Health-check / probe **registration** metadata for monitored services/components. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Reliability |
| **Merge rationale** | Probe registration merged into Health Check — no separate probe-runner product entity. |
| **Notes** | Registration only; deep probe-runner product depth remains out of scope. |

### 8. `mon_alert_rule`

| Field | Value |
|-------|--------|
| **Entity Name** | Alert Rule |
| **Purpose** | Alert rule and severity classification **metadata**. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Alerting Control Plane |
| **Merge rationale** | Severity catalog merged as attributes on Alert Rule. |
| **Notes** | Not a SIEM correlation product or security monitoring warehouse. |

### 9. `mon_alert_routing_policy`

| Field | Value |
|-------|--------|
| **Entity Name** | Alert Routing Policy |
| **Purpose** | Alert routing metadata that directs notifications to Foundation Notification channels. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Alerting Control Plane |
| **Merge rationale** | Kept separate from Alert Rule per FRD alert-rule vs routing split. |
| **Notes** | Foundation Notification remains delivery SoR (C-05). Channel refs are UUID-only attributes. |

### 10. `mon_slo_definition`

| Field | Value |
|-------|--------|
| **Entity Name** | SLO Definition |
| **Purpose** | Service Level Objective definition metadata for reliability governance. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Reliability |
| **Merge rationale** | — |
| **Notes** | Not a native SLO evaluation engine as telemetry SoR replacement. |

### 11. `mon_sli_definition`

| Field | Value |
|-------|--------|
| **Entity Name** | SLI Definition |
| **Purpose** | Service Level Indicator definition metadata aligned to SLO definitions. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Reliability |
| **Merge rationale** | Kept separate from SLO for Version Compatibility / reliability clarity. |
| **Notes** | Metadata only — evaluation engines may remain external or future-scoped. |

### 12. `mon_dashboard_definition`

| Field | Value |
|-------|--------|
| **Entity Name** | Dashboard Definition |
| **Purpose** | Dashboard / view **definition** metadata (layout/definition intent). |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Dashboard Catalog |
| **Merge rationale** | Panel/view fragments merged as definition payload/attributes — no separate panel entity. |
| **Notes** | Not Grafana (or equivalent) product ownership. |

### 13. `mon_signal_correlation`

| Field | Value |
|-------|--------|
| **Entity Name** | Signal Correlation |
| **Purpose** | Non-SIEM signal correlation / incident-signal **metadata** (Extension). |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Correlation |
| **Merge rationale** | — |
| **Notes** | Explicitly not a SIEM; Foundation Audit remains audit warehouse. |

### 14. `mon_external_platform_binding`

| Field | Value |
|-------|--------|
| **Entity Name** | External Platform Binding |
| **Purpose** | Adapter/UUID binding metadata to external observability platforms (Prometheus · Grafana · Loki · OpenTelemetry · cloud APM · SIEM refs). |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | External Bindings |
| **Merge rationale** | **Secret refs merged as attributes** — no Monitoring secret-store or credential-binding entity. |
| **Notes** | Platforms remain external SoR for telemetry storage/execution. Secrets via vault/Hub patterns only. |

### 15. `mon_service_policy_assignment`

| Field | Value |
|-------|--------|
| **Entity Name** | Service Policy Assignment |
| **Purpose** | Assignment metadata linking monitored services/components to observability policy versions. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Policy Governance |
| **Merge rationale** | Kept separate from Policy Version for clear service-binding lifecycle. |
| **Notes** | Business association only — no peer FK to foreign schemas. |

### 16. `mon_service_platform_assignment`

| Field | Value |
|-------|--------|
| **Entity Name** | Service Platform Assignment |
| **Purpose** | Assignment metadata linking monitored services/components to external platform bindings. |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | External Bindings |
| **Merge rationale** | Kept separate from Platform Binding and from Policy Assignment (distinct binding concerns). |
| **Notes** | UUID/adapter association only — does not materialize telemetry. |

### 17. `mon_observability_report`

| Field | Value |
|-------|--------|
| **Entity Name** | Observability Report |
| **Purpose** | Control-plane operational report metadata (policy coverage, binding status, alert-rule inventory, SLO definition inventory). |
| **Ownership** | Monitoring / Observability |
| **Aggregate** | Operations |
| **Merge rationale** | Export lifecycle merged into report entity attributes — no separate export entity. |
| **Notes** | Projections via contracts only. Not Analytics warehouse · not Hub usage SoR · not raw telemetry warehouse. |

**Business Entities: 17** · **Schema (proposed): `monitoring`** · **Prefix (proposed): `mon_`**

---

## 9. Aggregate Candidates

| Aggregate | Conceptual Root | Members |
|-----------|-----------------|---------|
| **Policy Governance** | Observability Policy | `mon_observability_policy` · `mon_observability_policy_version` · `mon_service_policy_assignment` |
| **Service Registry** | Monitored Service | `mon_monitored_service` · `mon_monitored_component` |
| **Signal Catalog** | Metric Definition / Log-Trace Policy | `mon_metric_definition` · `mon_log_trace_policy` |
| **Reliability** | SLO / Health | `mon_health_check` · `mon_slo_definition` · `mon_sli_definition` |
| **Alerting Control Plane** | Alert Rule | `mon_alert_rule` · `mon_alert_routing_policy` |
| **Dashboard Catalog** | Dashboard Definition | `mon_dashboard_definition` |
| **Correlation** | Signal Correlation | `mon_signal_correlation` |
| **External Bindings** | External Platform Binding | `mon_external_platform_binding` · `mon_service_platform_assignment` |
| **Operations** | Observability Report | `mon_observability_report` |

DDD aggregate boundaries are planning guidance for Detailed ERD. No relationship cardinality or schema is prescribed here.

---

## 10. Aggregate Ownership

| Aggregate | Owner |
|-----------|--------|
| Policy Governance | Monitoring / Observability |
| Service Registry | Monitoring / Observability |
| Signal Catalog | Monitoring / Observability |
| Reliability | Monitoring / Observability |
| Alerting Control Plane | Monitoring / Observability |
| Dashboard Catalog | Monitoring / Observability |
| Correlation | Monitoring / Observability |
| External Bindings | Monitoring / Observability |
| Operations | Monitoring / Observability |
| Auth · RBAC · Audit warehouse · Notification delivery · Workflow | **Foundation** (not Monitoring aggregates) |
| Usage metering · transport | **Integration Hub** (not Monitoring aggregates) |
| Telemetry storage / APM / SIEM products | **External platforms** (not Monitoring aggregates) |

---

## 11. Entity Responsibilities

| Entity | Responsibility (business level) |
|--------|----------------------------------|
| `mon_observability_policy` | Identify and govern observability policy masters |
| `mon_observability_policy_version` | Version, publish, and retire policy content |
| `mon_monitored_service` | Register what services/modules are monitored |
| `mon_monitored_component` | Register components under monitored services |
| `mon_metric_definition` | Catalog metric definitions (not time-series) |
| `mon_log_trace_policy` | Govern log/trace policy metadata (not stores) |
| `mon_health_check` | Register health/probe metadata |
| `mon_alert_rule` | Define alert rules and severity metadata |
| `mon_alert_routing_policy` | Route alert notifications via Foundation Notification refs |
| `mon_slo_definition` | Define SLO metadata |
| `mon_sli_definition` | Define SLI metadata |
| `mon_dashboard_definition` | Store dashboard/view definition metadata |
| `mon_signal_correlation` | Hold non-SIEM correlation / incident-signal metadata |
| `mon_external_platform_binding` | Bind external platforms via adapter/UUID + secret refs |
| `mon_service_policy_assignment` | Assign policies to monitored targets |
| `mon_service_platform_assignment` | Assign external bindings to monitored targets |
| `mon_observability_report` | Define/export control-plane operational reports |

---

## 12. Entity Relationships (Business Level Only)

Documentation relationships only. **No foreign keys. No cardinality schema. No Mermaid.**

| From | To | Business relationship |
|------|----|------------------------|
| Observability Policy Version | Observability Policy | Version of policy identity |
| Monitored Component | Monitored Service | Component belongs to service registration |
| Service Policy Assignment | Monitored Service / Component | Assigns policy to target |
| Service Policy Assignment | Observability Policy Version | Uses published (or draft) policy version |
| Health Check | Monitored Service / Component | Health registration for target |
| SLI Definition | SLO Definition | Indicator supports objective |
| Alert Routing Policy | Alert Rule | Routes a rule’s notifications |
| Alert Routing Policy | Foundation Notification (UUID) | Channel reference only |
| Service Platform Assignment | Monitored Service / Component | Assigns external binding to target |
| Service Platform Assignment | External Platform Binding | Uses platform binding |
| Dashboard Definition | Observability Policy / Monitored Service set | Definition may reference policy/service set (UUID/metadata) |
| Signal Correlation | Alert Rule / Metric Definition (optional UUID refs) | Non-SIEM correlation metadata |
| Observability Report | Control-plane entities (projected) | Report over Monitoring metadata via contracts |

---

## 13. UUID Reference Strategy

| Rule | Statement |
|------|-----------|
| **Internal Monitoring refs** | Monitoring entities may reference other Monitoring entities by UUID within the Monitoring bounded context (Detailed ERD decides persistence form). |
| **Peer module refs** | All peer-domain references are **UUID-only** (or stable module codes where Architecture Lock permits) — **never** peer-schema foreign keys. |
| **External platform refs** | External platform identities/contracts stored as adapter refs / UUIDs — platforms remain external. |
| **Secret refs** | Vault/Hub secret references only — plaintext tokens forbidden. |
| **No peer ORM** | Monitoring never loads or writes peer-module ORM models. |

---

## 14. Cross-Module References

| Peer | Reference mode | What Monitoring may store |
|------|----------------|---------------------------|
| Foundation Auth / RBAC | Service contracts | Actor/tenant context; permission checks via Foundation |
| Foundation Audit | Emit events (C-06) | No audit warehouse entity |
| Foundation Notification | UUID / channel contract refs | Routing metadata only |
| Foundation Workflow | Workflow initiation (C-04) | No Workflow Engine entity |
| Organization | UUID / tenant filters | Org scope without duplicating org masters |
| Integration Hub | Optional UUID/contracts | Transport/health projection refs — usage SoR unchanged |
| Analytics | Optional read-only consumption | No Analytics warehouse entity |
| Business / Platform modules | UUID / module code | Monitored target identity — never own their data |
| AI Platform | Optional future UUID hooks only | No AI telemetry SoR takeover |
| API Developer Portal | Optional future UUID hooks only | No DX report SoR takeover |
| External Observability Platforms | Adapter / UUID bindings | Binding metadata + secret refs only |

---

## 15. Ownership Matrix

| Concern | Owner |
|---------|--------|
| Observability policy · policy versions · service/component registry · metric definitions · log/trace policies · health-check registration · alert rules · alert routing metadata · SLO/SLI definitions · dashboard definitions · signal correlation metadata · external platform bindings · service assignments · operational report definitions | **Monitoring / Observability (this ERD)** |
| Authentication · Authorization · RBAC · JWT · users · Audit warehouse · Notification delivery · Workflow Engine | **Foundation** |
| Connectivity / transport / connectors / webhooks / queues · API usage metering · rate-limit enforcement metadata | **Integration Hub** |
| Enterprise BI / reporting warehouse | **Analytics** |
| Intelligence metadata / AI-scoped telemetry metadata | **AI Platform** |
| Developer Portal DX metadata / DX operational reports | **API Developer Portal** |
| Document file storage | **Document Management** |
| Business transactions / masters | **Business modules / Master Data** |
| Prometheus / Grafana / Loki / OpenTelemetry / cloud APM / SIEM products | **External systems** |

**Forbidden ownership transfers:** none of the completed modules may be redesigned or stripped of SoR to “fit” Monitoring.

---

## 16. Dependency Overview

ASCII only. Planning visualization — **not an ERD**. Documentation only. No architecture changes.

```text
Business Modules
        ↓
Foundation
        ↓
Monitoring / Observability
        ↓
Integration Hub
        ↓
Analytics
        ↓
External Observability Platforms
```

---

## 17. Foundation Dependencies

| Dependency | Required | Mode |
|------------|----------|------|
| Authentication / session | **Mandatory** | Services only |
| RBAC (`monitoring.*` planning) | **Mandatory** | Services only |
| Audit (C-06) | **Mandatory** | Emit audit events; Foundation remains warehouse |
| Notification (C-05) | **Mandatory** | Alert/operational notification requests; Foundation remains delivery |
| Workflow Engine (C-04) | **Mandatory where approvals required** | Policy publish · binding activate · critical alert-route approvals |
| Tenant / company context | **Mandatory** | Context filters + UUID |

---

## 18. Integration Hub Dependencies

| Dependency | Required | Mode |
|------------|----------|------|
| Transport / connector health projections | **Recommended (optional)** | UUID / contracts only |
| Usage metering | **None as SoR** | Hub remains usage SoR; Monitoring must not become usage warehouse |
| Peer ORM | **Forbidden** | No Hub model writes |

---

## 19. Analytics Dependencies

| Dependency | Required | Mode |
|------------|----------|------|
| Warehouse / BI / ETL | **None as SoR** | Analytics remains warehouse SoR |
| Control-plane operational metrics consumption | **Optional** | Read-only / projected — Analytics may consume; Monitoring does not become BI engine |

---

## 20. AI Platform Dependencies

| Dependency | Required | Mode |
|------------|----------|------|
| AI gateway / AI telemetry SoR | **None** | AI Platform ownership unchanged |
| Future UUID hooks | **Optional** | No SoR transfer; no redesign |

---

## 21. API Developer Portal Dependencies

| Dependency | Required | Mode |
|------------|----------|------|
| DX operational report SoR | **None** | Developer Portal ownership unchanged |
| Future UUID hooks | **Optional** | Distinct audiences; UUID/contracts only |

---

## 22. External Platform Dependencies

| Dependency | Required | Mode |
|------------|----------|------|
| Prometheus / Grafana / Loki / OpenTelemetry / cloud APM / SIEM | **Mandatory (adapters)** | Adapter / UUID bindings only |
| Telemetry storage / execution | **External SoR** | Must not enter ERP schema as Monitoring SoR |
| Secrets | **Vault / Hub patterns** | Refs on `mon_external_platform_binding` only |

---

## 23. Entity Lifecycle Planning

| Entity class | Planned lifecycle |
|--------------|-------------------|
| Policy / Policy Version / Alert Rule / Alert Routing / Dashboard / External Binding / SLO / SLI | Draft → Review → Approve (where required) → Publish → Bind/Route → Retire |
| Monitored Service / Component | Register → Activate → Update → Retire |
| Metric Definition / Log-Trace Policy / Health Check | Create → Publish/Activate → Update → Retire |
| Service Policy / Platform Assignments | Create → Activate → Update → Retire |
| Signal Correlation | Create → Activate → Update → Retire |
| Observability Report | Define → Generate/Export → Archive/Retire |

Published versions are **never silently replaced**.

---

## 24. Soft Delete Strategy

| Rule | Statement |
|------|-----------|
| **Soft-delete / retire** | Mutable control-plane metadata uses soft-delete or retire patterns aligned to DBS standards |
| **Audit-relevant history** | Retire/soft-delete must preserve history needed for Foundation Audit correlation |
| **Published immutability** | Published versions are not overwritten; new versions are created |
| **Detailed ERD** | Exact soft-delete columns/patterns deferred to Detailed ERD (not defined here) |

---

## 25. Versioning Strategy

| Artifact | Versioning concern |
|----------|--------------------|
| Observability Policy Version | Stable policy identity + explicit versions |
| Alert Rule / Alert Routing | Version-aware publish; no silent replace |
| Dashboard Definition | Version-aware definition metadata |
| External Platform Binding | Binding version tracks external contract without owning telemetry |
| SLO / SLI Definition | Remain compatible with health-check and alert-rule metadata versions |
| Metric Definition | Definition version (names/types/labels metadata only) |

**Editorial clarification:** Only `mon_observability_policy_version` is a **separate version entity**. Other publishable entities remain **version-aware within the same entity** (Draft → Publish → Retire lifecycle on the entity itself). Do **not** introduce additional version entities in Detailed ERD without Permanent ARB approval.

- Version upgrades must be explicit and auditable.
- Existing bindings/routes continue on resolved versions unless explicitly migrated under policy.

---

## 26. Audit Strategy

| Rule | Statement |
|------|-----------|
| **Audit owner** | Foundation Audit (C-06) |
| **Monitoring role** | Emit audit events for significant mutations |
| **Minimum audited actions (planning)** | Policy publish/retire · service/component registration changes · alert rule publish · routing changes · external binding activate/retire · report export |
| **Forbidden** | Monitoring-owned enterprise audit warehouse / SIEM replacement |

---

## 27. Multi-Tenant Strategy

| Rule | Statement |
|------|-----------|
| **Tenant isolation** | Mandatory on all Monitoring / Observability artifacts and reports |
| **RBAC** | Foundation RBAC `monitoring.*` (planning placeholder) |
| **Fail closed** | Unauthorized access denied via Foundation; no data leakage |
| **Detailed ERD** | Exact tenant key patterns deferred to Detailed ERD under DBS standards |

---

## 28. Company / Branch Scope

| Rule | Statement |
|------|-----------|
| **Company / branch scoping** | Applied where enterprise tenancy patterns require it (NFR-29-002) |
| **Organization masters** | Not duplicated — Organization domain remains SoR |
| **Scope filters** | UUID / context filters only |

---

## 29. Business Constraints

1. Architecture Lock v1.1 preserved — no modification.  
2. Exactly **17** recommended entities — add/remove/rename requires Permanent ARB approval; final count locked at Detailed ERD within **14–20**.  
3. Monitoring owns observability metadata / policy / control-plane only.  
4. Must not become APM vendor, log storage engine, metrics database, distributed tracing backend, SIEM, or infrastructure monitoring platform.  
5. External observability platforms remain external.  
6. Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow SoR.  
7. Integration Hub remains usage / transport SoR.  
8. Analytics / AI / Developer Portal ownership unchanged.  
9. Contracts / UUID / services / adapters only — **no peer ORM**.  
10. No high-cardinality raw telemetry warehouse in ERP schema.  
11. Secrets never belong in Monitoring as plaintext — refs only.  
12. No Detailed ERD, Mermaid, SQL, APIs, migrations, or implementation in this document.  
13. Unanimous Permanent ARB approval required before implementation.

---

## 30. Planning Assumptions

1. Foundation AuthN/AuthZ/RBAC/Audit/Notification/Workflow remain available platform services.  
2. External observability platforms remain the telemetry execution/storage systems (SDD tooling guidance).  
3. Architecture Lock v1.1 remains final and unmodified.  
4. Sprint 29 follows the established **metadata-first backend** delivery pattern (Sprints 26–28).  
5. Frontend may be deferred unless separately authorized.  
6. Integration Hub may expose optional health projection contracts without transferring usage SoR.  
7. Analytics may consume control-plane reports read-only without transferring warehouse SoR.  
8. Exact persistence inventory is finalized at Detailed ERD within the approved ARB range.  
9. SDD Observability / Monitoring sections are tooling guidance elaborated as ERP control-plane metadata — not a conflicting product.

---

## 31. Planning Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-29-01 | Becoming metrics/log/trace **storage SoR** | **Critical** | Hard ownership matrix; external platforms remain stores; no telemetry warehouse entities |
| R-29-02 | SIEM / security monitoring product creep | **Critical** | `mon_signal_correlation` is non-SIEM metadata only; Foundation Audit remains warehouse |
| R-29-03 | Overlap with Integration Hub usage metering | **High** | Hub remains usage SoR; optional contract projections only |
| R-29-04 | Overlap with Foundation Audit | **High** | Audit SoR unchanged; Monitoring emits audit events only |
| R-29-05 | Accidental APM / infra monitoring product scope | **High** | Keep SDD tooling external; adapters/bindings only |
| R-29-06 | High-cardinality telemetry ingest into ERP DB | **High** | Metadata-only entity set; forbid raw telemetry warehouse entities |
| R-29-07 | Secret/token storage for external platforms in clear text | **High** | Secret refs on binding entity only; vault/Hub patterns |
| R-29-08 | Confusion with AI / Devportal operational reports | **Medium** | Distinct report entity audience; UUID/contracts only |

---

## 32. Phase Distribution (Planning Alignment)

Must match FRD-29 / Sprint 29 ARB phases — **unchanged**. Entity assignment is planning guidance only.

| Phase | Focus | Entities (indicative) | Cumulative |
|-------|--------|------------------------|------------|
| **Phase 0** | Schema shell · module scaffold · Alembic bootstrap · adapters skeleton | *(none)* | **0 / 17** |
| **Phase 1** | Policy · service registry · metric definitions · health-check registration | `mon_observability_policy` · `mon_observability_policy_version` · `mon_monitored_service` · `mon_monitored_component` · `mon_metric_definition` · `mon_health_check` · `mon_service_policy_assignment` | **7 / 17** |
| **Phase 2** | Log/trace policy · alert rules · routing | `mon_log_trace_policy` · `mon_alert_rule` · `mon_alert_routing_policy` | **10 / 17** |
| **Phase 3** | SLO/SLI · dashboard · external bindings · correlation | `mon_slo_definition` · `mon_sli_definition` · `mon_dashboard_definition` · `mon_external_platform_binding` · `mon_service_platform_assignment` · `mon_signal_correlation` | **16 / 17** |
| **Phase 4** | Observability reports · hardening · permissions seed · validation | `mon_observability_report` | **17 / 17** |

Then: Validation → Validation Fix (if needed) → Release Notes (v1.24-beta planned) → Completion Report — same governance path as Sprints 26–28.

No APIs, migrations, repositories, or services are prescribed here.

---

## 33. Recommended Implementation Order

Planning guidance only — **not** a sprint execution plan and **not** implementation. Mirrors Phase Distribution. No new entities.

| Order | Group | Entities (indicative) |
|------:|-------|------------------------|
| 1 | Policy · Service Registry · Metric · Health | `mon_observability_policy` · `mon_observability_policy_version` · `mon_monitored_service` · `mon_monitored_component` · `mon_metric_definition` · `mon_health_check` · `mon_service_policy_assignment` |
| 2 | Log/Trace · Alerting | `mon_log_trace_policy` · `mon_alert_rule` · `mon_alert_routing_policy` |
| 3 | Reliability · Dashboard · External Bindings · Correlation | `mon_slo_definition` · `mon_sli_definition` · `mon_dashboard_definition` · `mon_external_platform_binding` · `mon_service_platform_assignment` · `mon_signal_correlation` |
| 4 | Operations | `mon_observability_report` |

No APIs, migrations, repositories, or services are prescribed here.

---

## 34. Future Entity Considerations

Documentation only. **No entities** in Sprint 29 inventory.

| Roadmap Item | Notes |
|--------------|-------|
| Observability UI product entities | Separately authorized frontend — not Sprint 29 |
| Native metrics TSDB / log warehouse / trace backend entities | Explicitly future — forbidden as Sprint 29 SoR |
| Deep APM product entities | Future — not Monitoring ownership transfer of external APM |
| Full SIEM entities | Future / forbidden as Monitoring SoR |
| Cloud infrastructure monitoring product entities | Remain external / future |
| Deeper SLO evaluation automation metadata | May extend locked SLO/SLI without ownership redesign |
| Expanded adapter catalog | Additional platforms under same binding model |
| Incident workflow hooks | Future UUID hooks to ITSM/BPM without SIEM ownership |
| Master FRD consolidation | Documentation debt only |

---

## 35. Entity Dependency Summary

Documentation only. No new entities. No implementation.

| Aggregate | Primary Dependency |
|-----------|--------------------|
| Policy Governance | Foundation (Workflow · Audit) |
| Service Registry | Business / Platform modules (UUID only) |
| Signal Catalog | External platforms (definitions only) |
| Reliability | Foundation Notification (indirect via alerts) |
| Alerting Control Plane | Foundation Notification · Workflow |
| Dashboard Catalog | External platforms (definition refs) |
| Correlation | Foundation Audit boundary (non-SIEM) |
| External Bindings | External Observability Platforms · vault/Hub secret refs |
| Operations | Analytics (optional read-only) · Integration Hub (optional projections) |

---

## 36. Validation Checklist

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Entity Planning defines Monitoring as Observability Metadata / Control Plane only | ✅ |
| 2 | Recommended inventory is exactly **17** entities within ARB **14–20** / FRD **~16–18** | ✅ |
| 3 | Core / Extension / Operational classification aligns to FRD-29 / ARB | ✅ |
| 4 | Foundation ownership of AuthN/AuthZ/RBAC/Audit/Notification/Workflow affirmed | ✅ |
| 5 | Integration Hub usage / transport SoR affirmed | ✅ |
| 6 | Analytics / AI / Developer Portal ownership unchanged | ✅ |
| 7 | External observability platforms remain external | ✅ |
| 8 | No APM / log-store / metrics-DB / trace-backend / SIEM / infra-monitoring entities | ✅ |
| 9 | UUID-only peer references · no peer ORM | ✅ |
| 10 | Soft-delete · versioning · audit · multi-tenant · company/branch strategies stated (planning level) | ✅ |
| 11 | Risks R-29-01 … R-29-08 preserved | ✅ |
| 12 | No SQL · tables · columns · FKs · Mermaid · APIs · Backend Planning · implementation | ✅ |
| 13 | Architecture Lock v1.1 preserved | ✅ |
| 14 | Ready for ERD-29 Detailed ERD | ✅ |

---

## 37. Permanent Architectural Constraints

| # | Constraint |
|---|------------|
| 1 | Architecture Lock v1.1 is FINAL — no modification |
| 2 | Recommended **17** entities — no add · no remove · no rename without unanimous Permanent ARB approval; final count locked at Detailed ERD within **14–20** |
| 3 | Monitoring / Observability owns observability metadata / policy / control-plane only |
| 4 | External observability platforms remain external (not ERP telemetry SoR) |
| 5 | Foundation remains AuthN/AuthZ/RBAC/Audit/Notification/Workflow SoR |
| 6 | Integration Hub remains usage / transport SoR |
| 7 | Contracts / UUID / services / adapters only — **no peer ORM** |
| 8 | No APM / log-store / metrics-DB / trace-backend / SIEM / infra-monitoring product scope |
| 9 | No Detailed ERD, Mermaid, SQL, APIs, migrations, Backend Planning, or implementation in this document |
| 10 | BRD / SDD / DBS — no mandatory redesign |
| 11 | Unanimous Permanent ARB approval required before implementation |

---

## 38. Metadata

| Field | Value |
|-------|--------|
| **Version** | **1.1** |
| **Status** | **Locked — Ready for Future Reference** |
| **Document Status** | **Locked** |
| **FRD Baseline** | FRD-29 Locked v1.1 |
| **Next Stage** | **ERD-29 Detailed ERD** |
| **Entity Count (recommended)** | **17** |
| **Entity Range** | **14–20** |
| **Schema / Prefix (proposed)** | `monitoring` / `mon_` |
| **Architecture Lock** | v1.1 — Preserved |

---

## 39. Closing Statement

ERD-29 Entity Planning is now Locked and becomes the baseline for all future Detailed ERD, backend implementation, validation, and release activities.

No architectural or ownership changes were introduced.

No Detailed ERD, Mermaid, SQL, APIs, Migrations, Backend Planning, or Implementation are included in this document.

Architecture Lock v1.1 preserved.

Ready for ERD-29 Detailed ERD.