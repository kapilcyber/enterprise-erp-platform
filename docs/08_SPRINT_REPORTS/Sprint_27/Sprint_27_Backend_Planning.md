# Sprint 27 — Enterprise AI Platform Backend Planning

| Field | Value |
|-------|--------|
| **Document** | Sprint 27 Backend Planning |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Document Status** | Locked |
| **Next Stage** | Sprint 27 Phase 0 Backend Implementation |
| **Sprint** | Sprint 27 — Enterprise AI Platform |
| **Release Target** | ERP Core v1.22-beta (planned) |
| **Schema / Prefix (proposed)** | `ai` / `ai_` |
| **API Mount (proposed)** | `/api/v1/ai` |
| **Business Tables** | Exactly **34** |
| **Architecture Lock** | v1.1 — Mandatory · Unchanged |
| **Aligned To** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · FRD-27 Locked v1.1 · ERD-27 Entity Planning Locked v1.1 · ERD-27 Detailed ERD Locked v1.1 · Sprint 27 Backend Planning Architecture Review Board Verdict |
| **Prior Release** | ERP Core v1.21-beta |

> **Implementation planning only.** No code, APIs, SQL, migrations, schemas, or implementation artifacts are prescribed as deliverables of this document. Entity inventory, Mermaid relationships, ownership, FRD, ERD, and Architecture Lock remain frozen.

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-23 | Initial Sprint 27 Backend Planning from Architecture Review Board Verdict (APPROVED WITH EDITORIAL IMPROVEMENTS). Phased backend strategy for exactly 34 `ai_*` entities. |
| 1.1 | 2026-07-23 | Editorial Lock. Added Permanent Implementation Rules; expanded Phase 0 checklist; Validation Gate / Architect Review Checklist / Enterprise AI Risk Review / Remaining Work after every phase; Completion Report planning; Provider Adapter & Agent execution boundary rules; cumulative progress; Release Readiness roadmap. No architecture redesign. No entity, Mermaid, ownership, FRD, ERD, or Architecture Lock changes. |

---

## Permanent Implementation Rules

These rules are **mandatory** for all Sprint 27 backend work and cannot be waived by phase convenience.

| # | Rule |
|---|------|
| 1 | Always use locked documents as the **only** baseline (BRD · SDD · DBS · Architecture Lock v1.1 · FRD-27 · ERD-27 Entity Planning · ERD-27 Detailed ERD · this Backend Planning) |
| 2 | Never redesign frozen artifacts |
| 3 | Never violate ownership boundaries |
| 4 | **No peer ORM** — AI never writes peer-module ORM models |
| 5 | **UUID-only references** to peer domains — never peer-schema FKs |
| 6 | **Service contracts only** for cross-module reads/writes |
| 7 | **Modular Monolith** — new `modules/ai` package; no service-boundary redesign |
| 8 | **Clean Architecture** — Router → Service → Repository → Database; domain independent of ORM |
| 9 | **DDD** — domain enums, exceptions, entities/value objects; engines for pure policy |
| 10 | **Architecture Lock v1.1** mandatory (C-01–C-06 · DG-01–06 · PY-01–07) |
| 11 | **Business modules remain System of Record** |
| 12 | **AI Platform remains Intelligence Layer only** — AI recommends; BPM and Business Modules remain execution authorities |

### Provider Architecture Rule (Mandatory)

Provider SDKs **MUST NEVER** be called directly from Services.

```text
Router
  ↓
Service
  ↓
Provider Adapter
  ↓
Gateway
  ↓
Provider SDK
```

### Agent Execution Boundary (Mandatory)

Agents **MUST NEVER** access repositories directly.

```text
Agent
  ↓
Tool Registry
  ↓
Tool
  ↓
Application Service
  ↓
Business Module
```

**Never:**

```text
Agent
  ↓
Repository
```

---

## 1. Architecture Review Board Verdict (Preserved)

| Question | Verdict |
|----------|---------|
| Ready for backend implementation? | **Yes** — phased waves only; not a big-bang of all capabilities |
| Entity redesign? | **Forbidden** — exactly 34 entities unchanged |
| Ownership redesign? | **Forbidden** |
| Final ARB call | **APPROVED WITH EDITORIAL IMPROVEMENTS** (incorporated herein) |

---

## 2. Recommended Implementation Phases (Preserved)

| Phase | Theme | Entities added | Cumulative |
|------:|-------|----------------|------------|
| **0** | Module skeleton (no business tables) | 0 | **0 / 34** |
| **1** | Core intelligence control plane | 21 | **21 / 34** |
| **2** | Knowledge & RAG | 5 | **26 / 34** |
| **3** | Agents & tools | 5 | **31 / 34** |
| **4** | Hardening & multimodal readiness | 3 | **34 / 34** |

Future Reserved AI Capabilities from ERD-27 remain **out of schema** and are not Sprint 27 entities.

---

## 3. Phase 0 — Module Skeleton (Expanded Checklist)

**Purpose:** Establish the AI Platform modular-monolith package and platform wiring **without** creating business tables.

**Entity progress:** **0 / 34**

### Phase 0 Deliverables (Planning Checklist)

| Area | Planned deliverable (no implementation in this document) |
|------|----------------------------------------------------------|
| **Module package** | `apps/api/src/modules/ai/` package root (`__init__.py`) |
| **Router** | `router.py` + `routers/` package; thin handlers only (DG-02) |
| **Dependencies** | `dependencies.py` — tenant context, RBAC, UoW/session injection (PY-07) |
| **Permissions** | `permissions.py` — `ai.*` namespace constants; Phase 0 shell / Phase 1 seed plan |
| **Schemas** | `schemas.py` (Pydantic v2) — shared envelopes; phase entities added later (PY-02) |
| **Domain** | `domain/` — enums, exceptions, entities, value objects (ORM-free; PY-03) |
| **Repositories** | `repository/` — scoped base repository; no peer-module repositories |
| **Services** | `service/` — application façade, scope validator, numbering (as needed) |
| **Engines** | `service/engines/` — package ready; phase engines added per wave |
| **Adapters** | `adapters/` — Foundation port first; Document / BPM / Low-Code / Analytics / Integration Hub ports as needed |
| **Tasks** | `tasks.py` — Celery task shell; idempotent patterns (PY-06) |
| **Tests** | Unit / security / module-import smoke tests for package wiring |
| **Alembic schema registration** | Create PostgreSQL schema `ai`; register models path for later `ai_*` tables (PY-04) — **no business tables in Phase 0** |
| **Router registration** | Include AI router on `/api/v1/ai` via shared API v1 router |
| **Celery registration** | Register AI task module with Celery app |
| **MyPy registration** | Include `modules.ai` in MyPy package / path configuration |

### Phase 0 Explicit Non-Goals

- No `ai_*` business tables
- No provider SDK calls
- No live LLM invoke
- No FRD/ERD/Architecture Lock changes

### Phase 0 Validation Gate (Mandatory)

| Gate | Required before Phase 1 |
|------|-------------------------|
| Ruff | Pass |
| MyPy | Pass |
| Pytest | Pass (Phase 0 suite) |
| Architecture validation | Clean Architecture package layout · DG-02 · PY-03 |
| Ownership validation | No peer ORM · no business SoR claims |
| API validation | Router mounted; no unauthorized open invoke surface |

### Phase 0 Completion Report (Mandatory)

Planned artifact:

`docs/08_SPRINT_REPORTS/Sprint_27/Sprint_27_Phase0_Completion_Report.md`

Must follow **exact Sprint 26 reporting standards** (scope, files, ownership, validation summary, remaining work).

### Phase 0 Architect Review Checklist

| Check | Required |
|-------|----------|
| Architecture Lock v1.1 preserved | ☐ |
| FRD-27 preserved | ☐ |
| ERD-27 (Entity Planning + Detailed) preserved | ☐ |
| Ownership preserved | ☐ |
| No peer ORM | ☐ |
| UUID-only references | ☐ |
| DDD preserved | ☐ |
| Clean Architecture preserved | ☐ |
| Validation Gate passed | ☐ |

### Phase 0 Enterprise AI Risk Review

| Checkpoint | Planning focus |
|------------|----------------|
| Security | RBAC shell; no open egress |
| Privacy | No conversation storage yet; tenant context wired |
| Prompt Injection | N/A (no invoke) — gate still reviewed |
| Data Leakage | No provider credentials in module |
| Guardrails | Policy engines not yet live — kill-switch hooks planned |
| Compliance | Audit adapter port planned (C-06) |
| Cost | No provider spend in Phase 0 |
| Model Governance | Registry tables deferred to Phase 1 |

### Phase 0 Remaining Work

| Area | Remaining |
|------|-----------|
| Business tables | All **34 / 34** `ai_*` entities |
| Phase 1 | Core control plane (21 entities) |
| Phase 2–4 | Knowledge · Agents · Hardening |
| Release path | Validation → Fix → Release Notes → Completion → Tag |

---

## 4. Phase 1 — Core Intelligence Control Plane

**Entity progress:** **21 / 34**

### Entities (Preserved)

`ai_provider` · `ai_model` · `ai_provider_credential_reference` · `ai_configuration` · `ai_prompt_template` · `ai_prompt_version` · `ai_prompt_variable` · `ai_gateway_policy` · `ai_routing_rule` · `ai_guardrail_policy` · `ai_moderation_policy` · `ai_rate_limit_policy` · `ai_assistant` · `ai_session` · `ai_conversation` · `ai_conversation_message` · `ai_conversation_memory` · `ai_context_package` · `ai_usage_record` · `ai_cost_record` · `ai_cache_entry`

### Alembic Migration Sequence (Preserved)

1. Registries: `ai_provider` → `ai_model` → `ai_provider_credential_reference` → `ai_configuration`
2. Prompts: `ai_prompt_template` → `ai_prompt_version` → `ai_prompt_variable`
3. Governance: `ai_gateway_policy` → `ai_routing_rule` → `ai_guardrail_policy` → `ai_moderation_policy` → `ai_rate_limit_policy`
4. Surfaces + runtime: `ai_assistant` → `ai_session` → `ai_conversation` → `ai_conversation_message` → `ai_conversation_memory` → `ai_context_package`
5. Ops: `ai_usage_record` → `ai_cost_record` → `ai_cache_entry`
6. Seed Phase 1 `ai.*` permissions / roles

### Repository / Service / Engine / Router Order (Preserved)

- **Repositories:** Provider · Model · CredentialReference · Configuration → Prompt* → Gateway/Routing/Guardrail/Moderation/RateLimit → Assistant → Session/Conversation/Message/Memory/ContextPackage → Usage/Cost/Cache
- **Services:** Numbering/scope → CRUD/lifecycle (same order) → Publish validation → Runtime resolve → Context assembly → Session/conversation → Usage/cost → Integration façade
- **Engines:** Prompt lifecycle/immutability → Publish gate → Gateway+routing → Guardrail+moderation → Rate-limit → Context packaging → Cache eligibility → Provider failover/degraded-mode
- **Routers:** Config/provider/model → Prompt publish → Governance policies → Assistants → Runtime session/conversation/invoke → Usage/cost/cache

### Provider Path (Phase 1 Enforcement)

Any model invoke **must** follow: Service → Provider Adapter → Gateway → Provider SDK. Services never import provider SDKs.

### Phase 1 Validation Gate (Mandatory)

| Gate | Required before Phase 2 |
|------|-------------------------|
| Ruff | Pass |
| MyPy | Pass |
| Pytest | Pass |
| Architecture validation | Router→Service→Adapter→Gateway→SDK · published immutability · PY-04 |
| Ownership validation | AI owns AI artifacts only · Audit via Foundation (C-06) |
| API validation | Design-time vs runtime permissions; no unauthorized tool/peer writes |

### Phase 1 Completion Report (Mandatory)

`docs/08_SPRINT_REPORTS/Sprint_27/Sprint_27_Phase1_Completion_Report.md`  
(Sprint 26 reporting standards.)

### Phase 1 Architect Review Checklist

| Check | Required |
|-------|----------|
| Architecture Lock v1.1 preserved | ☐ |
| FRD-27 preserved | ☐ |
| ERD-27 preserved | ☐ |
| Ownership preserved | ☐ |
| No peer ORM | ☐ |
| UUID-only references | ☐ |
| DDD preserved | ☐ |
| Clean Architecture preserved | ☐ |
| Validation Gate passed | ☐ |

### Phase 1 Enterprise AI Risk Review

| Checkpoint | Planning focus |
|------------|----------------|
| Security | RBAC on design-time + invoke; credential references only |
| Privacy | Session/message retention & redaction options |
| Prompt Injection | Input hardening before gateway invoke |
| Data Leakage | No secrets in prompts/logs; residency routing |
| Guardrails | Policy-before-model; fail closed for protected workloads |
| Compliance | Publish/invoke audit events to Foundation |
| Cost | Usage/cost records + rate limits + kill-switch |
| Model Governance | Only registered/approved providers/models in production |

### Phase 1 Remaining Work

| Area | Remaining |
|------|-----------|
| Entities | **13 / 34** remaining (Phases 2–4) |
| Knowledge / RAG | Phase 2 (5 entities) |
| Agents / tools | Phase 3 (5 entities) |
| Evaluation / feedback / multimodal | Phase 4 (3 entities) |

---

## 5. Phase 2 — Knowledge & RAG

**Entity progress:** **26 / 34**

### Entities (Preserved)

`ai_knowledge_base` · `ai_knowledge_source` · `ai_knowledge_chunk` · `ai_embedding` · `ai_vector_index`

### Alembic / Repo / Service Order (Preserved)

- Migration FK order: base → source → chunk → embedding → vector_index + permission seed
- Repositories / services in the same chain
- Engines: RAG retrieval ranking/citation
- Async Celery jobs for embedding/ingestion (idempotent)
- Document UUID via Document Management contract — files remain Document SoR

### Phase 2 Validation Gate (Mandatory)

| Gate | Required before Phase 3 |
|------|-------------------------|
| Ruff | Pass |
| MyPy | Pass |
| Pytest | Pass |
| Architecture validation | No file SoR in AI · async ingestion · C-02 |
| Ownership validation | Document UUID only · Analytics read-only metrics unchanged |
| API validation | Curator permissions; tenant isolation on corpora |

### Phase 2 Completion Report (Mandatory)

`docs/08_SPRINT_REPORTS/Sprint_27/Sprint_27_Phase2_Completion_Report.md`

### Phase 2 Architect Review Checklist

| Check | Required |
|-------|----------|
| Architecture Lock v1.1 preserved | ☐ |
| FRD-27 preserved | ☐ |
| ERD-27 preserved | ☐ |
| Ownership preserved | ☐ |
| No peer ORM | ☐ |
| UUID-only references | ☐ |
| DDD preserved | ☐ |
| Clean Architecture preserved | ☐ |
| Validation Gate passed | ☐ |

### Phase 2 Enterprise AI Risk Review

| Checkpoint | Planning focus |
|------------|----------------|
| Security | Corpus RBAC / tenant isolation |
| Privacy | PII minimization in chunk metadata |
| Prompt Injection | Untrusted RAG chunk isolation |
| Data Leakage | No wholesale document body as SoR in AI |
| Guardrails | Retrieval still subject to gateway/guardrail path |
| Compliance | Ingestion eligibility auditability |
| Cost | Embedding job quotas / bounded concurrency |
| Model Governance | Embedding model from approved registry only |

### Phase 2 Remaining Work

| Area | Remaining |
|------|-----------|
| Entities | **8 / 34** remaining |
| Agents / tools | Phase 3 |
| Evaluation / feedback / multimodal | Phase 4 |

---

## 6. Phase 3 — Agents & Tools

**Entity progress:** **31 / 34**

### Entities (Preserved)

`ai_skill` · `ai_tool` · `ai_tool_version` · `ai_agent` · `ai_agent_version`

### Alembic / Order (Preserved)

- Migration: tool → tool_version → skill → agent → agent_version + permission seed
- Engines: agent step/orchestration limits · tool allow-list / schema validation
- HITL for high-risk actions via BPM / Foundation Workflow contracts (C-04 / DG-03)
- Business writes **only** via owning module Application Services

### Agent Execution Boundary (Phase 3 Enforcement)

```text
Agent → Tool Registry → Tool → Application Service → Business Module
```

**Forbidden:** Agent → Repository (AI or peer).

### Phase 3 Validation Gate (Mandatory)

| Gate | Required before Phase 4 |
|------|-------------------------|
| Ruff | Pass |
| MyPy | Pass |
| Pytest | Pass |
| Architecture validation | Allow-list tools · no agent→repository · no peer ORM |
| Ownership validation | AI suggests only; modules/BPM execute |
| API validation | Designer vs publisher vs invoke permissions |

### Phase 3 Completion Report (Mandatory)

`docs/08_SPRINT_REPORTS/Sprint_27/Sprint_27_Phase3_Completion_Report.md`

### Phase 3 Architect Review Checklist

| Check | Required |
|-------|----------|
| Architecture Lock v1.1 preserved | ☐ |
| FRD-27 preserved | ☐ |
| ERD-27 preserved | ☐ |
| Ownership preserved | ☐ |
| No peer ORM | ☐ |
| UUID-only references | ☐ |
| DDD preserved | ☐ |
| Clean Architecture preserved | ☐ |
| Validation Gate passed | ☐ |

### Phase 3 Enterprise AI Risk Review

| Checkpoint | Planning focus |
|------------|----------------|
| Security | Tool sandbox; no OS/network/peer-DB (FR-27-040) |
| Privacy | Tool I/O minimization |
| Prompt Injection | Tool-output hardening |
| Data Leakage | No unrestricted egress from tools |
| Guardrails | Step/token limits; stop conditions |
| Compliance | High-risk actions require HITL / BPM |
| Cost | Agent loop quotas; kill-switch |
| Model Governance | Agent binds published prompt/tool versions only |

### Phase 3 Remaining Work

| Area | Remaining |
|------|-----------|
| Entities | **3 / 34** remaining |
| Evaluation · Feedback · Multimodal profile | Phase 4 |

---

## 7. Phase 4 — Hardening & Multimodal Readiness

**Entity progress:** **34 / 34**

### Entities (Preserved)

`ai_evaluation` · `ai_feedback` · `ai_multimodal_profile`

### Scope Notes (Planning)

- Evaluation/feedback loops; async evaluation jobs
- Multimodal profile = integration-point readiness metadata (OCR/STT/TTS/Vision) — **not** a license to build full multimodal pipelines as mandatory Phase 4 production scope beyond locked entities
- Analytics read-only metrics contract polish
- Ops: kill-switch / quota / chargeback readiness (cost records remain not Finance GL SoR)

### Phase 4 Validation Gate (Mandatory)

| Gate | Required before Release Readiness |
|------|-----------------------------------|
| Ruff | Pass |
| MyPy | Pass |
| Pytest | Pass |
| Architecture validation | 34/34 entities · Future Reserved still excluded |
| Ownership validation | Full ownership matrix intact |
| API validation | Full permission matrix; no shadow AI egress |

### Phase 4 Completion Report (Mandatory)

`docs/08_SPRINT_REPORTS/Sprint_27/Sprint_27_Phase4_Completion_Report.md`

### Phase 4 Architect Review Checklist

| Check | Required |
|-------|----------|
| Architecture Lock v1.1 preserved | ☐ |
| FRD-27 preserved | ☐ |
| ERD-27 preserved | ☐ |
| Ownership preserved | ☐ |
| No peer ORM | ☐ |
| UUID-only references | ☐ |
| DDD preserved | ☐ |
| Clean Architecture preserved | ☐ |
| Validation Gate passed | ☐ |

### Phase 4 Enterprise AI Risk Review

| Checkpoint | Planning focus |
|------------|----------------|
| Security | Multimodal ingress still via gateway governance |
| Privacy | Media context via Document UUID only |
| Prompt Injection | Multimodal/untrusted content isolation |
| Data Leakage | Provider training opt-out / residency |
| Guardrails | Evaluation evidence for high-risk publish |
| Compliance | Feedback may open Foundation/BPM cases by UUID — AI not case SoR |
| Cost | Chargeback readiness without GL ownership |
| Model Governance | Continuous evaluation against published packs |

### Phase 4 Remaining Work

| Area | Remaining |
|------|-----------|
| Entities | **0 / 34** remaining (inventory complete) |
| Release path | Validation → Validation Fix → Release Notes → Sprint Completion → Release Tag |
| Frontend | Deferred unless separately authorized |
| Future Reserved capabilities | Explicitly **not** part of the 34 entities |

---

## 8. Cumulative Implementation Progress

| Phase | Entities complete | Cumulative |
|------:|-------------------|------------|
| Phase 0 | 0 | **0 / 34** |
| Phase 1 | 21 | **21 / 34** |
| Phase 2 | +5 | **26 / 34** |
| Phase 3 | +5 | **31 / 34** |
| Phase 4 | +3 | **34 / 34** |

---

## 9. Cross-Cutting Implementation Orders (Preserved — Unchanged)

### 9.1 Alembic Migration Sequence (Overall)

1. Create schema `ai` + DBS mixin baseline (Phase 0)
2. Phase 1 registries → prompts → governance → surfaces/runtime → ops + permission seed
3. Phase 2 knowledge chain + permission seed
4. Phase 3 tools/skills/agents + permission seed
5. Phase 4 evaluation/feedback/multimodal + permission seed

Rules: UUID PKs · audit columns · tenant isolation · soft-delete · no peer-schema FKs · secrets never stored in tables (credential reference = secret-store pointer only).

### 9.2 Repository Implementation Order (Preserved)

1. Provider · Model · CredentialReference · Configuration  
2. PromptTemplate · PromptVersion · PromptVariable  
3. GatewayPolicy · RoutingRule · GuardrailPolicy · ModerationPolicy · RateLimitPolicy  
4. Assistant  
5. Session · Conversation · Message · Memory · ContextPackage  
6. UsageRecord · CostRecord · CacheEntry  
7. KnowledgeBase · KnowledgeSource · KnowledgeChunk · Embedding · VectorIndex  
8. Skill · Tool · ToolVersion · Agent · AgentVersion  
9. Evaluation · Feedback · MultimodalProfile  

### 9.3 Service Implementation Order (Preserved)

1. Numbering / code sequence (if used)  
2. Scope validator  
3. CRUD + lifecycle (entity order above)  
4. Publish validation service  
5. Runtime resolve service  
6. Context assembly service  
7. Session/conversation service  
8. Usage/cost recording service  
9. Knowledge ingestion orchestration (async)  
10. Agent/tool invoke coordination (allow-list + ports only)  
11. Evaluation/feedback services  
12. Integration façade (Foundation Audit/Notification; peer ports)

### 9.4 Engine Implementation Order (Preserved)

1. Prompt lifecycle / immutability  
2. Publish gate  
3. Gateway + routing decision  
4. Guardrail + moderation  
5. Rate-limit / quota  
6. Context packaging  
7. Cache eligibility  
8. RAG retrieval ranking/citation  
9. Agent step/orchestration limits  
10. Tool allow-list / schema validation  
11. Evaluation scoring summary  
12. Provider failover / degraded-mode  

### 9.5 Router Implementation Order (Preserved)

1. Health/admin config (configuration, provider, model, credential-reference)  
2. Prompt template/version/variable + publish/retire  
3. Governance policies  
4. Assistants  
5. Runtime (session, conversation, message, invoke)  
6. Usage/cost/cache ops  
7. Knowledge admin + ingestion job control  
8. Skills/tools/agents + invoke  
9. Evaluation/feedback  
10. Multimodal profile  

---

## 10. Permission Strategy (Preserved)

- Namespace: **`ai.*`** via Foundation RBAC  
- Roles (FRD): AI Platform Admin · Prompt Engineer · Knowledge Curator · Agent Designer · Publisher/Governance · Operator · Auditor · Consumer · Module Configurator · Security/Privacy Officer  
- Separate `:publish` · `:invoke` · `:admin` · `:audit`  
- Seed permissions **per phase**  
- Separation of duties: authors must not unilaterally publish high-risk packs  

---

## 11. Dependency Injection Strategy (Preserved)

- FastAPI dependencies for tenant, user, permissions (PY-07)  
- Session/UoW into repositories  
- Services take repositories + engines + **ports/adapters** only  
- Adapters: Foundation · Document · BPM · Low-Code · Analytics · Integration Hub · optional Master Data/Organization  
- **No peer ORM injection**  
- Celery tasks: IDs + tenant context; idempotent (PY-06)  
- Provider SDKs only behind Provider Adapter → Gateway  

---

## 12. Validation Strategy (Preserved + Phase Gates)

| Layer | Focus |
|-------|--------|
| Pydantic v2 | Request/response; never leak secrets |
| Domain | Lifecycle; published immutability |
| Publish validation | ERD Publish Dependency Matrix |
| Runtime resolution | Published versions only; fail closed when required |
| Tool invoke | Allow-list + schema + HITL for high-risk |
| Scope | Tenant (+ company/branch where required) |
| Context | UUID refs only; PII minimization |

Every phase must pass the **Validation Gate** (Ruff · MyPy · Pytest · Architecture · Ownership · API) before the next phase begins.

---

## 13. Testing Strategy (Preserved)

1. Unit engines  
2. Service lifecycle / immutability / tenancy  
3. API RBAC matrix  
4. Adapter contracts — assert no peer ORM  
5. Async task idempotency  
6. Safety fixtures (prompt injection / fail-closed guardrails)  
7. Regression: published immutability; cache cannot skip guardrails  
8. Early phases: fake provider adapters in CI; optional gated live provider suite later  

---

## 14. Cross-Module Integration Checkpoints (Preserved)

| Checkpoint | Phase | Pass criteria |
|------------|------:|---------------|
| Foundation AuthN/RBAC | 0–1 | All AI routes permissioned |
| Foundation Audit (C-06) | 1+ | Significant actions audited; AI not audit SoR |
| Foundation Notification (C-05) | 1+ | Alerts via Notification only |
| Workflow/BPM (C-04) | 3 | HITL via contracts; suggestion ≠ approval |
| Document UUID | 2 | Files remain Document SoR |
| Low-Code UUID | 1+ | Form/page context refs only |
| Analytics read-only | 1 / 4 | Metrics export; Analytics remains reporting SoR |
| Integration Hub (C-03) | 1 | Provider transport policy where required |
| Business modules | 3 | Writes only through owning module services |

---

## 15. AI Platform Ownership Verification (Preserved)

| AI owns | AI must not own |
|---------|-----------------|
| All 34 `ai_*` intelligence artifacts | Business transactions / masters / ledgers |
| Prompt/agent/tool/policy publish lifecycle | AuthN · AuthZ · RBAC |
| Knowledge index metadata (not files) | Foundation Audit warehouse |
| Sessions/conversations/context | Notification delivery |
| Usage/cost/cache/config | Workflow design/runtime |
| Multimodal profiles | Low-Code forms/pages · Document files · Analytics warehouse · Integration Hub transport |

**Decision boundary:** AI recommends. BPM and Business Modules remain execution authorities.

---

## 16. Mandatory Phase Reporting Standard

Every phase (0–4) **must** end with a completion report under:

`docs/08_SPRINT_REPORTS/Sprint_27/`

| Phase | Planned report |
|------:|----------------|
| 0 | `Sprint_27_Phase0_Completion_Report.md` |
| 1 | `Sprint_27_Phase1_Completion_Report.md` |
| 2 | `Sprint_27_Phase2_Completion_Report.md` |
| 3 | `Sprint_27_Phase3_Completion_Report.md` |
| 4 | `Sprint_27_Phase4_Completion_Report.md` |

Reports must follow **exact Sprint 26 reporting standards**, including:

- Sprint / phase metadata  
- Scope delivered / not implemented  
- Files / models / repositories / services / engines / permissions / tasks / tests  
- Ownership boundaries preserved  
- Validation summary  
- **Remaining Work** section  
- Architect editorial confirmation where applicable  

**Planning only in this document — reports are produced after each phase implementation.**

---

## 17. Release Readiness Roadmap

After Phase 4 Validation Gate passes:

```text
Validation
  ↓
Validation Fix
  ↓
Release Notes
  ↓
Sprint Completion Report
  ↓
Release Tag
```

| Artifact (planned) | Location pattern |
|--------------------|------------------|
| `Sprint_27_Validation_Report.md` | `docs/08_SPRINT_REPORTS/Sprint_27/` |
| `Sprint_27_Validation_Fix_Report.md` | `docs/08_SPRINT_REPORTS/Sprint_27/` |
| Release Notes | `docs/07_RELEASES/` (ERP Core v1.22-beta planned) |
| `Sprint_27_Completion_Report.md` | `docs/08_SPRINT_REPORTS/Sprint_27/` |
| Release Tag | Platform release process |

No release artifacts are created by this planning document.

---

## 18. Risks & Hidden Concerns (Preserved — Planning Awareness)

| Risk / concern | Planning mitigation |
|----------------|---------------------|
| Big-bang delivery | Enforce Phases 0–4 gates |
| Shadow AI | Gateway-only egress |
| AI output treated as approval | HITL + no peer writes |
| Secret leakage | Credential references; log redaction |
| Unbounded agents / cost | Quotas · kill-switch |
| Vector storage choice | Behind `ai_vector_index` metadata; no new entities |
| Cache bypassing guardrails | Cache eligibility engine |
| Prompt injection via RAG/tools | Isolation + allow-lists |
| Celery cross-tenant jobs | Tenant context mandatory on tasks |
| Streaming vs moderation timing | Pre/post policy checks planned |

---

## 19. Validation Table (This Editorial Lock)

| Gate | Result |
|------|--------|
| Exactly **34** entities referenced — no add/remove/rename | Pass |
| Mermaid / relationships / ownership / FRD / ERD / Architecture Lock unmodified | Pass |
| Migration · repository · service · engine · router orders preserved | Pass |
| Permanent Implementation Rules present | Pass |
| Phase 0 expanded checklist complete | Pass |
| Validation Gate after every phase | Pass |
| Completion Report planning after every phase | Pass |
| Architect Review Checklist after every phase | Pass |
| Enterprise AI Risk Review after every phase | Pass |
| Provider Adapter path strengthened | Pass |
| Agent → Tool → Application Service boundary strengthened | Pass |
| Cumulative progress 0→21→26→31→34 | Pass |
| Remaining Work after every phase | Pass |
| Release Readiness roadmap present | Pass |
| Planning only — no code / APIs / migrations / SQL | Pass |
| Ready for Sprint 27 Phase 0 Backend Implementation | Pass |

---

## Document Status

| Field | Value |
|-------|--------|
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Document Status** | Locked |
| **Next Stage** | Sprint 27 Phase 0 Backend Implementation |
| **Business Tables** | Exactly **34** |

---

## Closing Statement

Sprint 27 Backend Planning is now **Locked** and becomes the implementation planning baseline for Sprint 27 Phase 0 backend implementation through Phase 4 and release readiness.

Exactly **34** entities remain unchanged. Mermaid relationships, ownership boundaries, FRD-27, ERD-27, dependency/migration/repository/service/engine/router orders, and Architecture Lock v1.1 are preserved.

Provider SDKs must never be called from Services. Agents must never access repositories directly. Business modules remain Systems of Record. AI Platform remains the Intelligence Layer only.

Future backend implementation must follow this document and the locked baselines unless superseded through formal architecture governance.
