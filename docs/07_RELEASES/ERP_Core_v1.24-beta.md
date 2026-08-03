# ERP Core v1.24-beta — Release Notes

| Field | Value |
|-------|--------|
| **Document Type** | Enterprise Release Notes / Release Manifest |
| **Release Name** | ERP Core v1.24-beta |
| **Release Status** | Beta — Authorized (S29-REL-AUTH-01) |
| **Architecture Lock** | v1.1 — Preserved |
| **Classification** | Internal — Confidential |
| **Predecessor** | [ERP Core v1.23-beta](./ERP_Core_v1.23-beta.md) |
| **Primary Deliverable** | Sprint 29 — Monitoring / Observability |
| **Sprint State** | Completed (S29-SCR-01) |
| **Implementation State** | Complete — 17 / 17 entities |
| **Validation Gate** | PASS (S29-VG-EXEC-01) |

> **Release notes only.** This document describes the **ERP Core v1.24-beta** baseline after Sprint 29. It does not perform governance, authorize work, or modify implementation.

---

## 1. Release Information

| Field | Value |
|-------|--------|
| **Version** | ERP Core v1.24-beta |
| **Sprint** | Sprint 29 — Monitoring / Observability |
| **Module** | `apps/api/src/modules/monitoring/` |
| **Schema / Prefix** | `monitoring` / `mon_` |
| **Status** | Beta |
| **Release State** | Authorized (PEARB Release Authorization S29-REL-AUTH-01) |
| **Release Date** | TBD (organizational release procedures) |
| **Architecture Lock** | v1.1 — Preserved |
| **Previous Release** | ERP Core v1.23-beta |
| **FRD / ERD** | FRD-29 Locked v1.1 · ERD-29 Entity Planning Locked v1.1 · ERD-29 Detailed ERD Locked v1.1 |
| **Backend Planning** | Sprint 29 Backend Planning Locked v1.2 |
| **Recommended Git Tag** | `v1.24-beta` |
| **API Mount** | `/api/v1/monitoring` |
| **Alembic Head** | `0599_mon_observability_report` |
| **Monitoring Integration Tests** | **31 passed** (validation gate evidence) |

---

## 2. Release Overview

ERP Core **v1.24-beta** packages the **Monitoring / Observability** backend delivered in Sprint 29: control-plane metadata and lifecycle APIs for policies, service registry, metrics, health checks, alerting, SLO/SLI, dashboards, external platform bindings, signal correlation, and observability report definitions.

Monitoring stores **operational and configuration metadata** under the `monitoring` schema. It is **not** a runtime APM product, SIEM, telemetry warehouse, or production observability platform. Peer domains are referenced by **UUID only** — no peer ORM and no cross-module business foreign keys.

Sprint 29 Phases **0–4** are complete. The Monitoring module is **locked** (S29-P4-LOCK-01). Validation Gate **PASS**. Sprint 29 **completed** (S29-SCR-01).

---

## 3. Release Highlights

- **New module:** Monitoring / Observability (`modules/monitoring`) mounted at `/api/v1/monitoring`.
- **Full Locked inventory:** **17 / 17** entities implemented per Backend Planning Locked v1.2.
- **Alembic:** `monitoring` schema plus linear migrations **0582** through **0599**.
- **Layer stack:** Models · repositories · services · lifecycle engines · routers · DTOs · permission constants · application service façade.
- **Quality:** Ruff · MyPy · **31** monitoring integration tests · FastAPI startup · Alembic head — all **PASS** at Validation Gate.
- **Architecture:** Modular monolith · DDD · Clean Architecture · Architecture Lock v1.1 unchanged.

---

## 4. Included Features

Capabilities introduced (summary — not every field or endpoint):

| Area | Capability |
|------|------------|
| **Monitoring (module)** | Central API surface for observability control-plane metadata |
| **Policies** | Observability policy and policy version definitions |
| **Services** | Monitored service registry |
| **Components** | Monitored component registry |
| **Metrics** | Metric definition metadata |
| **Health checks** | Health check definition metadata |
| **Policy assignment** | Service-to-policy assignment |
| **Log / trace policies** | Log and trace policy metadata |
| **Alert rules** | Alert rule definitions |
| **Alert routing** | Alert routing policy metadata |
| **SLO** | SLO definition metadata |
| **SLI** | SLI definition metadata |
| **Dashboards** | Dashboard definition metadata |
| **External platform bindings** | Bindings to external observability platforms (metadata) |
| **Service platform assignments** | Service-to-platform assignment metadata |
| **Signal correlation** | Signal correlation rule metadata |
| **Observability reports** | Observability report definition metadata (export format · lifecycle draft/active/archived) |

### API route groups (under `/api/v1/monitoring`)

| Route prefix | Domain |
|--------------|--------|
| `/policies` · `/policy-versions` | Policy catalog |
| `/services` · `/components` | Service registry |
| `/metric-definitions` · `/health-checks` | Metrics · health |
| `/service-policy-assignments` | Policy assignment |
| `/log-trace-policies` | Log / trace |
| `/alert-rules` · `/alert-routing-policies` | Alerting |
| `/slo-definitions` · `/sli-definitions` | SLO / SLI |
| `/dashboard-definitions` | Dashboards |
| `/external-platform-bindings` | External platforms |
| `/service-platform-assignments` | Platform assignment |
| `/signal-correlations` | Correlation |
| `/observability-reports` | Report definitions |

Lifecycle transitions are implemented per entity via services and lifecycle engines (e.g. observability report activate · mark-archived).

---

## 5. Implementation Summary

| Metric | Value |
|--------|--------|
| **Entities** | **17 / 17** |
| **Alembic chain** | **0582** → **0599** |
| **Current head** | **`0599_mon_observability_report`** |
| **Monitoring module** | **Complete** (Sprint 29 scope) |

### Entity tables (`mon_*`)

`mon_observability_policy` · `mon_observability_policy_version` · `mon_monitored_service` · `mon_monitored_component` · `mon_metric_definition` · `mon_health_check` · `mon_service_policy_assignment` · `mon_log_trace_policy` · `mon_alert_rule` · `mon_alert_routing_policy` · `mon_slo_definition` · `mon_sli_definition` · `mon_dashboard_definition` · `mon_external_platform_binding` · `mon_service_platform_assignment` · `mon_signal_correlation` · `mon_observability_report`

### Phase progression

| Phase | Outcome |
|-------|---------|
| **0** | `monitoring` schema · module scaffold · Alembic **0582** |
| **1** | **7** entities · **0583**–**0589** |
| **2** | **+3** entities · **0590**–**0592** |
| **3** | **+6** entities · **0593**–**0598** |
| **4** | **+1** entity · **0599** · **17 / 17** |

---

## 6. Quality Summary

Evidence from Sprint 29 Validation Gate execution (S29-VG-EXEC-01):

| Gate | Result |
|------|--------|
| Ruff (`src/modules/monitoring`) | **PASS** |
| MyPy (`src/modules/monitoring`) | **PASS** |
| Pytest (`src/tests/integration/monitoring`) | **PASS** — **31** tests |
| FastAPI startup | **PASS** — `Enterprise ERP API` |
| Alembic | **PASS** — head `0599_mon_observability_report` |
| **Validation Gate** | **PASS** |

---

## 7. Architecture Summary

| Principle | Confirmation |
|-----------|--------------|
| **Architecture Lock v1.1** | **Preserved** |
| **Modular Monolith** | New `modules/monitoring` package |
| **DDD** | Domain enums · exceptions · aggregates |
| **Clean Architecture** | Router → Service → Engine → Repository → Model |
| **UUID-only cross-module references** | Confirmed |
| **No peer ORM** | Confirmed |
| **No peer foreign keys** (monitoring business peers) | Confirmed |
| **Monitoring owns control-plane metadata only** | Not APM · SIEM · warehouse SoR |

---

## 8. What Is Included

| Category | Included |
|----------|----------|
| **Monitoring backend** | Full Phase 0–4 implementation |
| **API endpoints** | REST routers Phases 1–4 under `/api/v1/monitoring` |
| **Repositories** | Per-entity repositories |
| **Services** | Per-entity services + `MonitoringApplicationService` |
| **Lifecycle engines** | State transitions per domain rules |
| **Alembic migrations** | **0582_create_monitoring_schema** through **0599_mon_observability_report** |
| **Validation** | Integration smoke suite (**31** tests) · gate **PASS** |
| **Documentation** | Sprint 29 FRD/ERD/BP (locked) · sprint reports archived |
| **Governance lifecycle** | Completed per Sprint 29 archive (S29-SCR-01) |

---

## 9. What Is Not Included

| Item | Notes |
|------|--------|
| **Permission seed** | Not implemented in Sprint 29; permission **constants** only |
| **Production deployment** | Out of scope for this release manifest |
| **Runtime monitoring platform** | No metrics ingestion · no live telemetry pipeline |
| **Telemetry warehouse** | Analytics / warehouse remain separate SoR |
| **SIEM** | Security event SoR not replaced |
| **APM product** | No application performance runtime product |
| **Sprint 30 work** | Not part of v1.24-beta |
| **Future enhancements** | Deferred to future sprints / PEARB acts |

---

## 10. Compatibility

| Compatibility | Status |
|---------------|--------|
| **ERP Core architecture** | Compatible — modular monolith preserved |
| **Architecture Lock v1.1** | Compatible — unchanged |
| **Repository conventions** | Compatible — matches existing `apps/api` patterns |
| **Migration chain** | Compatible — head **`0599_mon_observability_report`** continues from v1.23-beta head **`0581_seed_devportal_phase4_permissions`** via **0582** |

Prior ERP Core modules remain in place; Monitoring adds schema **`monitoring`** and module wiring (router · Alembic · permissions constants).

---

## 11. Upgrade Notes

1. Apply Alembic migrations through the standard upgrade path to head **`0599_mon_observability_report`**.
2. Migration segment for this release: **`0582_create_monitoring_schema`** → **`0599_mon_observability_report`** (linear chain).
3. **No manual data migration** is documented for this release.
4. Ensure application configuration includes Monitoring router mount (default ERP Core API layout).

---

## 12. Known Limitations

| Limitation | Detail |
|------------|--------|
| **Beta release** | v1.24-beta — not GA |
| **Permission seed** | Deferred; RBAC seed data for monitoring resources not shipped |
| **Future enhancements** | Permission seed · deeper runtime integration — future sprints |
| **Blockers** | **None** recorded at Validation Gate or Sprint Completion |

---

## 13. Release Contents

| Content | Status |
|---------|--------|
| Monitoring / Observability module | **Included** |
| **17** entities | **Complete** |
| Phases 0–4 | **Complete** |
| Validation Gate | **PASS** |
| Release Authorization | **Recorded** (S29-REL-AUTH-01) |
| Sprint 29 | **Completed** (S29-SCR-01) |

### Authoritative governance references (read-only)

| Document | ID |
|----------|-----|
| Phase 4 Lock Resolution | S29-P4-LOCK-01 |
| Validation Gate Execution | S29-VG-EXEC-01 |
| Release Authorization | S29-REL-AUTH-01 |
| Sprint Completion | S29-SCR-01 |

Engineering and governance artifacts are archived under `docs/08_SPRINT_REPORTS/Sprint_29/`.

---

## 14. Release Statistics

| Statistic | Value |
|-----------|--------|
| **Sprint** | 29 |
| **Domain** | Monitoring / Observability |
| **Business tables** | **17** |
| **Alembic revisions (monitoring segment)** | **0582**–**0599** (**18** revisions including schema) |
| **Alembic head** | `0599_mon_observability_report` |
| **Monitoring integration tests** | **31** **PASS** |
| **API mount** | `/api/v1/monitoring` |
| **Route groups** | **17** resource surfaces (Phases 1–4) |

---

## 15. Closing Statement

**ERP Core v1.24-beta** reflects the **Sprint 29** Monitoring / Observability backend: **17 / 17** entities, Alembic head **`0599_mon_observability_report`**, Validation Gate **PASS**, Release **authorized**, Sprint 29 **completed**, Architecture Lock **v1.1 preserved**.

This release notes document is a **manifest for consumers and operators**. Deployment, permission seeding, and runtime observability integrations remain outside this document’s scope.

---

*End of ERP Core v1.24-beta Release Notes*
