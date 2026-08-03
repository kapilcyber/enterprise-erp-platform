# BP-29 — Monitoring / Observability Backend Planning

| Field | Value |
|-------|--------|
| **Document** | BP-29 Monitoring / Observability Backend Planning |
| **Document ID** | BP-29 |
| **Version** | **1.2** |
| **Status** | **Locked — Ready for Future Reference** |
| **Document Status** | **Locked** |
| **Next Stage** | **Sprint 29 Phase 0 Backend Implementation** |
| **Sprint** | Sprint 29 — Monitoring / Observability |
| **Release Target** | ERP Core v1.24-beta (planned) |
| **Module** | `apps/api/src/modules/monitoring/` |
| **Schema / Prefix** | `monitoring` / `mon_` |
| **API Mount** | `/api/v1/monitoring` |
| **Business Tables** | Exactly **17** |
| **Architecture Lock** | v1.1 — Mandatory · Unchanged |
| **Aligned To** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · FRD-29 Locked v1.1 · ERD-29 Entity Planning Locked v1.1 · ERD-29 Detailed ERD Locked v1.1 · Sprint 29 ARB Recommendation Locked v1.1 |
| **Prior Release** | ERP Core v1.23-beta |
| **Prior Alembic Head (planning baseline)** | `0581_seed_devportal_phase4_permissions` (Sprint 28 close — verify at Phase 0) |
| **RBAC Namespace (planning)** | `monitoring.*` — final codes at Phase 4 permission seed |

> **Implementation planning only.** No code, SQL, migrations, models, repositories, services, routers, or implementation artifacts are deliverables of this document. Entity inventory, relationships, ownership, FRD, ERD, and Architecture Lock remain frozen.

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-29 | Initial BP-29 Monitoring / Observability Backend Planning. Phased backend strategy for exactly **17** `mon_*` entities under schema `monitoring`. Draft — Ready for Architect Review. No implementation. Architecture Lock v1.1 preserved. Next Stage: Phase 0 Implementation. |
| 1.1 | 2026-07-29 | Editorial Lock after Permanent Enterprise Architecture Review Board unanimous approval. Added Release Readiness Roadmap, Phase 0 Expanded Checklist, Cumulative Implementation Progress, and Expanded Remaining Work by phase. Updated metadata to Version 1.1 / Locked — Ready for Future Reference. Updated Closing Statement to Sprint 28 Locked style. No entity, phase, roadmap, or implementation-content changes. Still exactly **17** entities. |
| 1.2 | 2026-07-29 | Repository Convention Alignment (ARB-authorized editorial only). Package/file/test path references aligned to existing `apps/api/src/modules/*` implementation conventions (e.g. Sprint 28 `devportal`). No architecture, entity, phase, roadmap, FRD, or ERD changes. Still exactly **17** entities. |

---

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document Title** | Monitoring / Observability — Backend Planning |
| **Domain** | Monitoring / Observability |
| **Classification** | Internal — Confidential |
| **Authoritative Baselines** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · FRD-29 Locked v1.1 · ERD-29 Entity Planning Locked v1.1 · ERD-29 Detailed ERD Locked v1.1 · Sprint 29 ARB Recommendation Locked v1.1 · ERD-01…ERD-28 |
| **Permanent ARB** | 13 architects · 20+ years enterprise experience each · unanimous approval required |
| **Product Role** | Enterprise Observability Metadata and Control Plane |
| **Repository Path Note** | Sprint 29 Backend Planning stored under `docs/08_SPRINT_REPORTS/Sprint_29/Sprint_29_Backend_Planning.md` (same convention as Sprint 27–28). Documentation organization only. |

### Authoritative Planning Baseline

This Backend Planning is the **single implementation planning baseline** for Sprint 29.

Implementation must conform to:

- Architecture Lock v1.1
- FRD-29 Locked v1.1
- ERD-29 Entity Planning Locked v1.1
- ERD-29 Detailed ERD Locked v1.1
- This Backend Planning document

Any deviation requires unanimous approval of the Permanent Enterprise Architecture Review Board.

---

## 2. Purpose

This document freezes the **backend application architecture and implementation plan** for Monitoring / Observability:

- Exactly **17** entities (`mon_*`) under schema `monitoring`
- Modular monolith package `modules/monitoring`
- API mount `/api/v1/monitoring`
- Phased delivery: **0 → 7 → 10 → 16 → 17**
- Clean Architecture · DDD · UUID-only peer refs · no peer ORM
- Release target **ERP Core v1.24-beta (planned)**

**Monitoring / Observability owns observability metadata / policy / control-plane only.**  
**External observability platforms remain external.**  
**Foundation remains Auth / Audit / Notification / Workflow SoR.**  
**Integration Hub remains usage / transport SoR.**

---

## 3. Permanent Implementation Rules

These rules are **mandatory** for all Sprint 29 backend work and cannot be waived by phase convenience.

| # | Rule |
|---|------|
| 1 | Always use locked documents as the **only** baseline |
| 2 | Never redesign frozen artifacts (FRD / Entity Planning / Detailed ERD) |
| 3 | Never violate ownership boundaries |
| 4 | **No peer ORM** — Monitoring never writes peer-module ORM models |
| 5 | **UUID-only references** to peer domains — never peer-schema FKs |
| 6 | **Service contracts / adapters only** for cross-module reads/writes |
| 7 | **Modular Monolith** — new `modules/monitoring` package; no service-boundary redesign |
| 8 | **Clean Architecture** — Router → Service → Engine → Repository → Model; domain independent of ORM |
| 9 | **DDD** — domain enums, exceptions, entities/value objects; engines for pure policy |
| 10 | **Architecture Lock v1.1** mandatory (C-01–C-06 · DG-01–06 · PY-01–07) |
| 11 | **Business modules remain System of Record** |
| 12 | **Monitoring remains Observability Metadata / Control Plane only** — not APM, log store, metrics DB, tracing backend, SIEM, or infra monitoring |
| 13 | Every phase **begins** with Permanent ARB review · locked-doc verification · conflict scan · ownership verification |
| 14 | Every phase **ends** with Validation Gate · Architect Review Checklist · Enterprise Risk Review · Completion Report |
| 15 | Validation Fix permitted **only** for Ruff · MyPy · Pytest · FastAPI/OpenAPI · imports · static analysis — never new functionality/entities/APIs/schema/migrations/architecture/ownership |
| 16 | Exactly **17** entities — no add · no remove · no rename without unanimous Permanent ARB approval |

### External Platform Binding Rule (Mandatory)

External platform secret materialization is forbidden. `secret_ref` attributes only. Bindings use adapters.

```text
Router
  ↓
ApplicationService
  ↓
ExternalObservabilityAdapter (contract)
  ↓
External Platform (Prometheus / Grafana / Loki / OTel / cloud APM / SIEM)
```

**Never:** store plaintext tokens · become telemetry SoR · peer-ORM into Hub / Foundation / Analytics / AI / DevPortal.

### Telemetry Boundary (Mandatory)

```text
Forbidden:
  Monitoring → metrics TSDB / log warehouse / trace backend / SIEM product / APM product
Allowed:
  Policy · registry · definition · alert routing · SLO/SLI · dashboard definition · binding · report **metadata** only
```

### Implementation Governance Flow

Documentation only.

```text
Architecture Lock
        ↓
FRD
        ↓
Entity Planning
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

## 4. Backend Architecture Principles

| Principle | Application |
|-----------|-------------|
| **Metadata First** | Control-plane CRUD before any telemetry runtime depth |
| **Contract First** | Peers via adapters/contracts only |
| **Security by Default** | Foundation AuthN/AuthZ/RBAC before enablement |
| **Zero Duplicate Ownership** | Foundation · Hub · Analytics · AI · DevPortal unchanged |
| **Published immutability** | Published policy versions / version-aware publishables never silently replaced |
| **Tenant isolation** | All repositories filter `tenant_id` (+ `company_id` where required) |
| **Soft delete / version stamps** | Per DBS / Detailed ERD |
| **Audit via Foundation** | Emit C-06 events; Monitoring is not audit warehouse |
| **Notifications via Foundation** | C-05 delivery; Monitoring does not own transport |
| **Workflow via Foundation** | C-04 approvals for policy publish · binding activate · critical alert routes |
| **Adapter Pattern** | External observability platforms via adapters |
| **Dependency Injection** | FastAPI Depends / container wiring (PY-07) |

```text
Router (FastAPI) — API layer
  ↓
Service — Application layer
  ↓
Engine (pure policy) — Domain policy
  ↓
Repository — Infrastructure persistence port
  ↓
Model (SQLAlchemy) → PostgreSQL schema `monitoring`
```

Cross-cutting:

```text
Adapters → Foundation · Integration Hub · Analytics · External Platforms
```

---

## 5. Module Structure

| Concern | Planning decision |
|---------|-------------------|
| **Package root** | `apps/api/src/modules/monitoring/` |
| **Bounded context** | Monitoring / Observability |
| **Schema** | `monitoring` |
| **Table prefix** | `mon_` |
| **API mount** | `/api/v1/monitoring` |
| **RBAC namespace** | `monitoring.*` |
| **Celery package** | Monitoring tasks under module `tasks` (idempotent) |
| **Alembic** | Revisions under platform Alembic tree; discover `monitoring` models |

---

## 6. Folder Structure / Package Layout

Planning layout for `apps/api/src/modules/monitoring/` aligned to existing repository module conventions (authoritative peers: `modules/devportal`, `modules/ai`, and all other `modules/*` — no implementation in this document):

```text
modules/monitoring/
├── __init__.py
├── router.py                 # aggregate include → /api/v1/monitoring
├── routers/                  # thin handlers only (DG-02)
├── dependencies.py           # tenant · RBAC · UoW (PY-07)
├── permissions.py            # monitoring.* constants
├── schemas.py                # Pydantic v2 DTOs (PY-02) — flat file (repo convention)
├── domain/                   # enums · exceptions · entities/VOs (ORM-free; PY-03)
├── models/                   # SQLAlchemy mon_* models
├── repository/               # repository interfaces + implementations
├── service/                  # application services (singular service/, not services/)
│   └── engines/              # lifecycle · publish · validation policy
├── adapters/                 # Foundation · Hub · Analytics · External platform ports
└── tasks.py                  # Celery shells (idempotent; PY-06)
```

**Tests (repo convention):** global suite under `apps/api/src/tests/` — `unit/monitoring/`, `security/monitoring/`, `integration/monitoring/` (not module-local `modules/monitoring/tests/`).

**Not used (absent across `modules/*`):** `schemas/` package · `mappers/` package · module-level `config.py` · module-local `tests/`.

**Registrations (Phase 0):** `shared/router.py` API v1 include · `workers/celery_app.py` autodiscovery · `pyproject.toml` MyPy package path · `alembic/env.py` model discovery.

---

## 7. Clean Architecture Layers

| Layer | Responsibility | Must not |
|-------|----------------|----------|
| **API (routers)** | HTTP mapping · auth dependency · status codes | Business rules · ORM |
| **Application (services)** | Use-cases · transactions · orchestration · adapter calls | Pure domain pollution by framework |
| **Domain (engines · enums · exceptions · entities)** | Policy · lifecycle · invariants | ORM · HTTP · peer SDKs |
| **Infrastructure (models · repositories · adapters)** | Persistence · external I/O | Bypass service/engine for writes |

---

## 8. Domain Layer

Planning contents:

| Element | Intent |
|---------|--------|
| Domain enums | `status` · `severity` · `signal_kind` · `platform_type` · `environment_class` · `report_kind` |
| Domain exceptions | Unauthorized · Validation · InvalidTransition · PublishedImmutable · SecretMaterializationForbidden · TelemetrySoRForbidden · AdapterFailure |
| Entities / value objects | ORM-free representations for policy version identity, assignment keys, binding refs |
| Engines | Pure lifecycle / publish / immutability / assignment eligibility rules |

**No SQLAlchemy imports in `domain/`.**

---

## 9. Application Layer

| Element | Intent |
|---------|--------|
| Entity services | CRUD + lifecycle per aggregate |
| Application façade | `MonitoringApplicationService` wiring phase services |
| Use-case methods | Publish policy · activate binding · assign policy/platform · route alert · generate report |
| Ports | Workflow · Audit · Notification · Hub projection · External platform · Analytics export |

Services call engines for policy and repositories for persistence. Adapters for peers only.

---

## 10. Infrastructure Layer

| Element | Intent |
|---------|--------|
| SQLAlchemy models | Exactly **17** `mon_*` tables per Detailed ERD Locked v1.1 |
| Repository implementations | Tenant-scoped queries · soft-delete filters · optimistic `version` |
| Adapters | Foundation / Hub / Analytics / External platform HTTP or service clients |
| Unit of Work / session | Shared DB session per request / task |

**Forbidden:** peer-module model imports · cross-schema ORM joins · plaintext secret columns.

---

## 11. API Layer

| Concern | Planning |
|---------|----------|
| Framework | FastAPI |
| Mount | `/api/v1/monitoring` |
| Style | Thin routers (DG-02) |
| Auth | Foundation JWT / session dependencies |
| AuthZ | `monitoring.*` permission checks |
| OpenAPI | Generated by FastAPI — Monitoring does not own OpenAPI generation product |
| DTOs | Pydantic v2 request/response schemas |

**Forbidden routes:** telemetry ingest warehouse · SIEM query product · secret materialization · peer-module mutation endpoints.

---

## 12. Locked Entity Inventory (Exactly 17)

| # | Entity / Table |
|---|----------------|
| 1 | `mon_observability_policy` |
| 2 | `mon_observability_policy_version` |
| 3 | `mon_monitored_service` |
| 4 | `mon_monitored_component` |
| 5 | `mon_metric_definition` |
| 6 | `mon_log_trace_policy` |
| 7 | `mon_health_check` |
| 8 | `mon_alert_rule` |
| 9 | `mon_alert_routing_policy` |
| 10 | `mon_slo_definition` |
| 11 | `mon_sli_definition` |
| 12 | `mon_dashboard_definition` |
| 13 | `mon_signal_correlation` |
| 14 | `mon_external_platform_binding` |
| 15 | `mon_service_policy_assignment` |
| 16 | `mon_service_platform_assignment` |
| 17 | `mon_observability_report` |

No add · no remove · no rename.

---

## 13. Aggregate Implementation Order

| Order | Aggregate | Entities |
|------:|-----------|----------|
| 1 | Policy Governance | `mon_observability_policy` · `mon_observability_policy_version` · `mon_service_policy_assignment` |
| 2 | Service Registry | `mon_monitored_service` · `mon_monitored_component` |
| 3 | Signal Catalog | `mon_metric_definition` · `mon_log_trace_policy` |
| 4 | Reliability | `mon_health_check` · `mon_slo_definition` · `mon_sli_definition` |
| 5 | Alerting Control Plane | `mon_alert_rule` · `mon_alert_routing_policy` |
| 6 | Dashboard Catalog | `mon_dashboard_definition` |
| 7 | Correlation | `mon_signal_correlation` |
| 8 | External Bindings | `mon_external_platform_binding` · `mon_service_platform_assignment` |
| 9 | Operations | `mon_observability_report` |

---

## 14. Phase Distribution (Locked)

**Locked — do not change.** Matches FRD-29 / ARB / Entity Planning / Detailed ERD.

| Phase | Focus | Cumulative |
|-------|--------|------------|
| **Phase 0** | Schema shell · module scaffold · Alembic bootstrap · adapters skeleton | **0 / 17** |
| **Phase 1** | Policy · service registry · metric definitions · health-check · policy assignment | **7 / 17** |
| **Phase 2** | Log/trace policy · alert rules · alert routing | **10 / 17** |
| **Phase 3** | SLO/SLI · dashboard · external bindings · correlation · platform assignment | **16 / 17** |
| **Phase 4** | Observability reports · hardening · permissions seed · validation gate | **17 / 17** |

### 14.1 Phase entity lists (preserved)

| Phase | Entities |
|-------|----------|
| **1** | `mon_observability_policy` · `mon_observability_policy_version` · `mon_monitored_service` · `mon_monitored_component` · `mon_metric_definition` · `mon_health_check` · `mon_service_policy_assignment` |
| **2** | `mon_log_trace_policy` · `mon_alert_rule` · `mon_alert_routing_policy` |
| **3** | `mon_slo_definition` · `mon_sli_definition` · `mon_dashboard_definition` · `mon_external_platform_binding` · `mon_service_platform_assignment` · `mon_signal_correlation` |
| **4** | `mon_observability_report` |

Future Reserved capabilities remain **out of schema** and are not Sprint 29 entities.

---

## 15. Repository Interfaces & Implementations

### 15.1 Repository Order

| Order | Repositories (indicative) |
|------:|---------------------------|
| 1 | ObservabilityPolicy · ObservabilityPolicyVersion |
| 2 | MonitoredService · MonitoredComponent |
| 3 | MetricDefinition · HealthCheck · ServicePolicyAssignment |
| 4 | LogTracePolicy · AlertRule · AlertRoutingPolicy |
| 5 | SloDefinition · SliDefinition · DashboardDefinition |
| 6 | ExternalPlatformBinding · ServicePlatformAssignment · SignalCorrelation |
| 7 | ObservabilityReport |

### 15.2 Repository Rules

| Rule | Statement |
|------|-----------|
| Interface | Application depends on repository protocols/ABCs |
| Implementation | Infrastructure SQLAlchemy repositories |
| Scope | Always filter `tenant_id` (+ `company_id`) |
| Soft delete | Default exclude `is_deleted = TRUE` |
| Concurrency | Honor `version` optimistic stamp |
| Peers | No peer-module repositories · no peer ORM |
| `slo_id` on alert rule | UUID attribute lookup only — **no ORM FK** per Detailed ERD |

---

## 16. Service Layer

| Order | Services (indicative) |
|------:|----------------------|
| 1 | Scope / tenant validator · numbering/code helpers (if used) |
| 2 | ObservabilityPolicyService · ObservabilityPolicyVersionService |
| 3 | MonitoredServiceService · MonitoredComponentService |
| 4 | MetricDefinitionService · HealthCheckService · ServicePolicyAssignmentService |
| 5 | LogTracePolicyService · AlertRuleService · AlertRoutingPolicyService |
| 6 | SloDefinitionService · SliDefinitionService · DashboardDefinitionService |
| 7 | ExternalPlatformBindingService · ServicePlatformAssignmentService · SignalCorrelationService |
| 8 | ObservabilityReportService (contract projections) |
| 9 | Foundation Audit / Notification / Workflow integration façade |
| 10 | `MonitoringApplicationService` façade wiring phase services |

---

## 17. Engine Layer

| Order | Engines (indicative) |
|------:|----------------------|
| 1 | Policy version lifecycle / published immutability |
| 2 | Service / component registration eligibility |
| 3 | Metric definition validation (reject raw time-series SoR intent) |
| 4 | Log/trace policy signal-kind rules |
| 5 | Health-check registration rules (registration only — not probe-runner product) |
| 6 | Alert rule / severity / routing eligibility |
| 7 | SLO/SLI consistency rules |
| 8 | Dashboard definition publish rules |
| 9 | External binding activation / secret-ref hygiene |
| 10 | Assignment activation rules (policy / platform) |
| 11 | Signal correlation non-SIEM guardrails |
| 12 | Report projection freshness / fail-closed rules |

Engines are pure policy — **no ORM, no peer SDK calls, no HTTP**.

---

## 18. Adapter Layer

| Adapter (indicative) | Peer | Mode |
|----------------------|------|------|
| `FoundationAuthAdapter` | Foundation Auth/RBAC | Permission / identity context |
| `FoundationAuditAdapter` | Foundation Audit | Emit C-06 events |
| `FoundationNotificationAdapter` | Foundation Notification | C-05 alert/ops notifications |
| `FoundationWorkflowAdapter` | Foundation Workflow | C-04 approvals |
| `IntegrationHubProjectionAdapter` | Integration Hub | Optional health/transport projection UUID/contracts |
| `AnalyticsExportAdapter` | Analytics | Optional read-only control-plane metrics consumption |
| `AiPlatformHookAdapter` | AI Platform | Optional future UUID hooks only — no SoR takeover |
| `ExternalObservabilityAdapter` | Prometheus/Grafana/Loki/OTel/cloud APM/SIEM | Binding validation / adapter calls — platforms remain external |

**No peer ORM inside adapters.**

---

## 19. DTO Planning

| DTO family | Intent |
|------------|--------|
| Create / Update / Patch | Write contracts per entity |
| Read / List / Detail | Response contracts |
| Publish / Retire / Activate | Lifecycle action payloads |
| Assignment | Policy / platform assignment requests |
| Report generate / export | Operational report requests |
| Error | Standard domain error envelopes |

Pydantic v2 only. No ORM models exposed on API boundary.

---

## 20. DTO Mapping Planning

No dedicated `mappers/` package exists in the repository. Mapping follows existing module practice (`schemas.py` + services):

| Concern | Intent (repo-aligned) |
|---------|------------------------|
| Schema ↔ Domain | Request DTOs in `schemas.py` consumed by services / commands |
| Domain ↔ Model | Services construct / update SQLAlchemy model fields |
| Model ↔ Response | Pydantic `OrmModel` / `from_attributes` response DTOs in `schemas.py` |
| Adapter payloads | Contract DTOs for Foundation / Hub / External (adapters + schemas) |

DTO mapping must not embed business policy (engines own policy).

---

## 21. Validation Planning

| Layer | Validation |
|-------|------------|
| API | Pydantic field/type validation |
| Application | Cross-field / tenancy / uniqueness checks |
| Engine | Lifecycle transitions · published immutability · telemetry SoR rejection · secret-ref required when binding activated |
| Persistence | DB unique / FK constraints per Detailed ERD |

Fail closed on adapter/projection failures — do not invent telemetry or “healthy” binding state.

---

## 22. Authorization Planning / RBAC Integration

| Concern | Planning |
|---------|----------|
| Namespace | `monitoring.*` (planning placeholder) |
| Final codes | Confirmed at Phase 4 permission seed |
| Enforcement | Foundation RBAC via FastAPI dependencies |
| Roles (FRD) | Monitoring Admin · SRE Operator · Service Owner · Monitoring Auditor · Security/Compliance Officer |
| Report permissions (planning) | `monitoring.report:read` · `monitoring.report:export` (final codes at seed) |
| Least privilege | Service Owners cannot approve Admin-class changes |

Monitoring does **not** invent a parallel identity store.

---

## 23. Workflow Integration

| Concern | Planning |
|---------|----------|
| Owner | Foundation Workflow Engine (C-04) |
| Planned approval classes | Policy publish · External binding activate · Critical alert routing |
| Example codes (planning) | `MON_POLICY_APPROVAL` · `MON_BINDING_APPROVAL` · `MON_ALERT_ROUTE_APPROVAL` |
| Storage | `workflow_instance_id` UUID on relevant tables (no peer FK) |
| Monitoring role | Initiate / participate — never replace Workflow Engine |

---

## 24. Notification Integration

| Concern | Planning |
|---------|----------|
| Owner | Foundation Notification (C-05) |
| Triggers | Alert metadata events · policy publish · binding failure · report export completion |
| Channel refs | `notification_channel_ref` UUID on `mon_alert_routing_policy` |
| Monitoring role | Emit notification requests — never own SMS/email/PagerDuty delivery |

---

## 25. Integration Hub Contracts

| Concern | Planning |
|---------|----------|
| Usage metering SoR | **Remains Integration Hub** |
| Optional projections | Transport/health via UUID/contracts only |
| Attribute | `hub_projection_ref` on platform assignment (optional) |
| Forbidden | Peer ORM · Monitoring usage warehouse |

---

## 26. Analytics Contracts

| Concern | Planning |
|---------|----------|
| Warehouse SoR | **Remains Analytics** |
| Mode | Optional read-only consumption of control-plane operational metrics |
| Monitoring role | May expose exportable control-plane report metadata — not BI/ETL engine |

---

## 27. AI Platform Contracts

| Concern | Planning |
|---------|----------|
| AI telemetry SoR | **Remains AI Platform** |
| Mode | Optional future UUID hooks only |
| Forbidden | AI traffic SoR takeover · peer ORM |

---

## 28. Event Publishing

| Event class (planning) | Destination |
|------------------------|-------------|
| Significant mutations | Foundation Audit (C-06) |
| Alert / ops notifications | Foundation Notification (C-05) |
| Workflow transitions | Foundation Workflow |
| Optional domain events | Platform event bus via contracts (if used by monolith pattern) — no peer ORM |

No Monitoring-owned audit warehouse events store.

---

## 29. Transaction Boundaries / Unit of Work

| Rule | Statement |
|------|-----------|
| Request UoW | One DB session / Unit of Work per API request |
| Task UoW | One session per Celery task execution |
| Boundary | Service method commits via UoW after successful engine + repository work |
| Adapter side-effects | Prefer outbox/idempotent emit after commit where platform pattern requires |
| Partial publish | Forbidden — invalid transitions roll back |

---

## 30. Dependency Injection

Order (planning):

1. FastAPI dependencies: tenant · user · permissions (PY-07)  
2. Session / Unit of Work  
3. Repository implementations  
4. Engines  
5. Adapters / ports: Foundation · Hub · Analytics · External observability  
6. Entity services  
7. Application façade  
8. Routers  

**No peer ORM injection. No Hub/Foundation/Analytics/AI SQLAlchemy models in Monitoring DI graph.**

Celery tasks: pass IDs + tenant context; idempotent (PY-06).

---

## 31. Logging Strategy

| Concern | Planning |
|---------|----------|
| Style | Structured logs (JSON or platform standard) |
| Correlate | `tenant_id` · `request_id` · entity ids |
| Never log | Secrets · tokens · raw telemetry payloads as SoR dumps |
| Control-plane events | Policy publish · binding failure · projection failure |

Monitoring may emit operational logs for the control plane without becoming telemetry warehouse SoR.

---

## 32. Exception Strategy

| Class | Handling |
|-------|----------|
| Validation / domain | 4xx with stable error codes |
| Unauthorized / forbidden | Foundation RBAC denials |
| Published immutability | Reject silent overwrite |
| Adapter failure | Fail closed · do not invent healthy/telemetry state |
| Concurrency | Optimistic lock conflict on `version` |
| Unexpected | 5xx · log · no data leakage |

---

## 33. Configuration Strategy

| Concern | Planning |
|---------|----------|
| Module settings | Environment / settings object for adapter endpoints, timeouts |
| Secrets | External vault/Hub patterns only — never in Monitoring tables as plaintext |
| Schema name | `monitoring` |
| API prefix | `/api/v1/monitoring` |

---

## 34. Feature Flags

| Flag theme (planning) | Intent |
|-----------------------|--------|
| External adapter enablement | Per platform_type |
| Optional Hub projection | On/off without schema change |
| Optional Analytics export | On/off |
| Deferred UI | Frontend not required for backend phases |

Flags must not introduce new entities.

---

## 35. Caching Strategy

| Concern | Planning |
|---------|----------|
| Default | No aggressive cache required for metadata CRUD |
| Optional | Short TTL cache for published policy/version reads if needed |
| Invalidation | On publish/retire/activate |
| Forbidden | Cache of raw telemetry time-series as Monitoring SoR |

---

## 36. Background Jobs / Scheduler Planning

| Job theme (planning) | Intent |
|----------------------|--------|
| Report generation | Async generate/export for large operational reports |
| Binding health ping (optional) | Adapter status check — metadata only; fail closed |
| Soft-delete retention sweep | Align to enterprise retention (if platform standard) |

Celery (or platform scheduler) only. Idempotent tasks. No probe-runner product depth unless later FRD authorization.

---

## 37. Testing Strategy

| Layer | Focus |
|-------|-------|
| Unit | Engines · validators · schema/service mapping helpers |
| Service | Use-cases with fake repositories/adapters |
| API | Router permission · validation · status codes |
| Security | RBAC · tenant isolation · secret-ref rejection |
| Integration | DB constraints · soft-delete · optimistic version |
| Contract | Adapter fakes for Foundation / Hub / External |

**Location (repo convention):** `apps/api/src/tests/unit/monitoring/`, `apps/api/src/tests/security/monitoring/`, `apps/api/src/tests/integration/monitoring/` (same pattern as `tests/*/devportal/`).

Validation Fix scope remains static/test hygiene only — no new features.

---

## 38. Package Dependencies (Planning)

| Dependency class | Notes |
|------------------|-------|
| FastAPI · Pydantic v2 | API / DTO |
| SQLAlchemy · Alembic | Persistence / migrations (implementation later) |
| Platform Foundation clients | Auth · RBAC · Audit · Notification · Workflow |
| Celery (platform) | Background tasks |
| HTTP client (platform standard) | External adapters |
| Test stack | Pytest · httpx · MyPy · Ruff |

No new microservice frameworks. Modular monolith only.

---

## 39. Router Order

| Order | Router groups (indicative) · Mount `/api/v1/monitoring` |
|------:|--------------------------------------------------------|
| 1 | `/policies` · `/policy-versions` (+ publish/retire) |
| 2 | `/services` · `/components` |
| 3 | `/metric-definitions` · `/health-checks` · `/service-policy-assignments` |
| 4 | `/log-trace-policies` · `/alert-rules` · `/alert-routing-policies` |
| 5 | `/slo-definitions` · `/sli-definitions` · `/dashboard-definitions` |
| 6 | `/external-platform-bindings` · `/service-platform-assignments` · `/signal-correlations` |
| 7 | `/reports` (read/export) |
| 8 | Ops / health as required |

**Forbidden routes:** telemetry ingest warehouse · SIEM product APIs · secret materialization · peer-module writes.

---

## 40. Alembic Strategy

| Concern | Planning |
|---------|----------|
| Schema create | Phase 0 — `monitoring` schema shell |
| Model discovery | Register `modules.monitoring.models` |
| Phase migrations | One logical revision theme per phase (names planning-only) |
| Permissions seed | Phase 4 — `monitoring.*` |
| No redesign | Columns/FKs must match Detailed ERD Locked v1.1 |

### Indicative revision themes (names planning-only)

| Phase | Theme (indicative) |
|-------|--------------------|
| 0 | `create_monitoring_schema` / module bootstrap |
| 1 | `mon_phase1_policy_registry_metric_health` |
| 2 | `mon_phase2_log_trace_alert_routing` |
| 3 | `mon_phase3_slo_dashboard_binding_correlation` |
| 4 | `seed_monitoring_phase4_permissions` |

Exact revision IDs assigned at implementation time.

---

## 41. Permission Strategy

| Concern | Planning |
|---------|----------|
| Constants module | `permissions.py` |
| Seed timing | Phase 4 |
| Namespace | `monitoring.*` |
| Mapping | Align to FRD roles / report read-export |
| Enforcement | Every mutating and sensitive read route |

---

## 42. Phase-wise Implementation Roadmap

| Phase | Deliverables (planning) | Exit |
|-------|-------------------------|------|
| **0** | Package scaffold · router mount · DI shell · adapters skeleton · Alembic schema shell · empty model registry | Completion Report · 0/17 |
| **1** | 7 entities · repos · services · engines · routers · migrations | Completion Report · 7/17 |
| **2** | +3 alerting/log-trace entities · Notification channel ref wiring | Completion Report · 10/17 |
| **3** | +6 reliability/dashboard/binding/correlation entities · External adapters | Completion Report · 16/17 |
| **4** | +1 report entity · permissions seed · hardening · validation gate | Completion Report · 17/17 |
| **Validation** | Ruff · MyPy · Pytest · FastAPI/OpenAPI · ownership scan | Validation Report |
| **Validation Fix** | Static/test hygiene only | Fix Report (if needed) |
| **Release** | ERP Core v1.24-beta (planned) | Release Notes |
| **Completion** | Sprint 29 Completion Report | Closed |

---

## 43. Validation Gate

Every phase and final validation must confirm:

| # | Gate |
|---|------|
| 1 | Exactly **17** entities — no drift from Detailed ERD |
| 2 | Schema `monitoring` / prefix `mon_` |
| 3 | No peer ORM · UUID-only peers |
| 4 | Foundation / Hub / Analytics / AI / DevPortal ownership preserved |
| 5 | No telemetry warehouse / APM / SIEM / infra monitoring product scope |
| 6 | Soft-delete · tenant · audit · version stamps present |
| 7 | RBAC enforced on routes |
| 8 | Tests pass (phase-scoped) |
| 9 | Ruff · MyPy clean (phase-scoped) |
| 10 | Architecture Lock v1.1 preserved |

---

## 44. Architect Review Checklist

| # | Check |
|---|-------|
| 1 | Locked baselines unchanged |
| 2 | Aggregates match Entity Planning |
| 3 | Relationships match Detailed ERD |
| 4 | `mon_alert_rule.slo_id` remains UUID attribute (no ORM FK) |
| 5 | Optional `mon_slo_definition.service_id` uses ON DELETE SET NULL |
| 6 | Adapters only for peers / external platforms |
| 7 | Engines remain ORM-free |
| 8 | No new entities or tables |

---

## 45. Enterprise Risk Review

| ID | Risk | Mitigation in Backend Planning |
|----|------|--------------------------------|
| R-29-01 | Telemetry storage SoR | No ingest warehouse tables/routes |
| R-29-02 | SIEM creep | Correlation metadata only; Audit remains Foundation |
| R-29-03 | Hub usage overlap | Hub contracts only |
| R-29-04 | Audit overlap | Emit-only adapter |
| R-29-05 | APM/infra creep | Adapter bindings only |
| R-29-06 | High-cardinality ingest | Engine rejects telemetry SoR intent |
| R-29-07 | Secret plaintext | `secret_ref` only · validation reject |
| R-29-08 | AI/DevPortal report confusion | Distinct report service + ownership checks |

---

## 46. Completion Report Requirement

Each phase Completion Report must include:

- Entities delivered / cumulative count  
- Migrations applied (IDs)  
- Tests run / results  
- Ownership verification  
- Architecture Lock confirmation  
- Deviations (none expected)  

---

## 47. Cross-Module Integration Checkpoints

| Peer | Checkpoint |
|------|------------|
| Foundation Auth/RBAC | Permissions resolve; tenant context present |
| Foundation Audit | Mutation events emitted |
| Foundation Notification | Alert routing uses channel UUID contracts |
| Foundation Workflow | Approval codes wired where required |
| Integration Hub | Optional projection only; usage SoR unchanged |
| Analytics | Optional read-only; warehouse SoR unchanged |
| AI / DevPortal | No SoR transfer |
| External platforms | Adapter bind/activate; platforms remain external |

---

## 48. Ownership Verification (Preserved)

| Concern | Owner |
|---------|--------|
| All 17 `mon_*` tables · control-plane services | Monitoring / Observability |
| Auth · RBAC · Audit warehouse · Notification delivery · Workflow | Foundation |
| Usage metering · transport | Integration Hub |
| Analytics warehouse | Analytics |
| AI telemetry metadata | AI Platform |
| DX operational reports | API Developer Portal |
| Prometheus / Grafana / Loki / OTel / cloud APM / SIEM | External systems |

---

## Release Readiness Roadmap

Validation
↓
Validation Fix (if required)
↓
Release Documentation
↓
Sprint Completion Report
↓
Git Tag / Release Tag
↓
ERP Core v1.24-beta (planned)

Documentation only.

---

## Phase 0 — Expanded Checklist (Planning)

Entity progress: **0 / 17**

Planning checklist items:

- Package scaffold
- Router registration
- Dependency Injection shell
- Alembic schema bootstrap
- Model registration
- Adapter skeleton
- Repository interfaces
- Service skeleton
- Engine skeleton
- Validation gate

Planning only.

---

## Cumulative Implementation Progress (Locked)

No roadmap changes. Editorial display only.

| Phase | Entities complete |
|-------|--------------------|
| Phase 0 | 0 / 17 |
| Phase 1 | 7 / 17 |
| Phase 2 | 10 / 17 |
| Phase 3 | 16 / 17 |
| Phase 4 | 17 / 17 |

---

## 49. Remaining Work (After This Document)

After EVERY phase, Completion Report must list remaining work. Indicative cumulative remaining:

| After Phase | Entities complete | Remaining |
|-------------|-------------------|-----------|
| Phase 0 | 0 / 17 | All remaining entities + Phases 1–4 |
| Phase 1 | 7 / 17 | 10 remaining |
| Phase 2 | 10 / 17 | 7 remaining |
| Phase 3 | 16 / 17 | 1 remaining |
| Phase 4 | 17 / 17 | 0 remaining |

Additional planning deliverables (non-code in this doc):

| Item | Status |
|------|--------|
| Phase 0–4 Implementation | Not started |
| Migrations | Not generated in this document |
| Code / APIs | Not generated in this document |
| Validation / Release / Completion | Later governance stages |

---

## 50. Metadata

| Field | Value |
|-------|--------|
| **Version** | **1.2** |
| **Status** | **Locked — Ready for Future Reference** |
| **Document Status** | **Locked** |
| **Entity Count** | **17** |
| **Schema / Prefix** | `monitoring` / `mon_` |
| **Module** | `apps/api/src/modules/monitoring/` |
| **API Mount** | `/api/v1/monitoring` |
| **Next Stage** | **Sprint 29 Phase 0 Backend Implementation** |
| **Architecture Lock** | v1.1 — Preserved |
| **Detailed ERD Baseline** | Locked v1.1 |
| **Entity Planning Baseline** | Locked v1.1 |
| **Package Convention Baseline** | Repository `modules/*` (e.g. `devportal`) — Implementation Convention Precedence |

---

## Version History / Document Revision (Editorial)

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-29 | Initial BP-29 Monitoring / Observability Backend Planning. Draft — Ready for Architect Review. |
| 1.1 | 2026-07-29 | Editorial Lock: Release Readiness Roadmap, Phase 0 Expanded Checklist, Cumulative Progress, Expanded Remaining Work; updated metadata and Closing Statement to Sprint 28 Locked style. |
| 1.2 | 2026-07-29 | Repository Convention Alignment: package/file/test path references aligned to existing `modules/*` conventions; no architecture/entity/phase/roadmap changes. |

---

## 51. Closing Statement

Backend Planning is now Locked and becomes the baseline for all Phase 0–4 backend implementation, validation, and release activities.

No architectural or ownership changes were introduced.

Package layout references are aligned to repository implementation conventions (`schemas.py`, `service/`, global `apps/api/src/tests/`, no `mappers/` / module `config.py` / module-local `tests/`).

**Sprint 29 Backend Planning — Complete.**

**Architecture Lock preserved.**

**FRD preserved.**

**Entity Planning preserved.**

**Detailed ERD preserved.**

**Exactly 17 entities remain unchanged.**

**Ready for Sprint 29 Phase 0 Backend Implementation.**
