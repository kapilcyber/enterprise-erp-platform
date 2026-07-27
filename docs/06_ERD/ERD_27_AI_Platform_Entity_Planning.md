# ERD-27 — Entity Planning  
## Enterprise AI Platform

| Field | Value |
|-------|--------|
| **Document** | ERD-27 AI Platform Entity Planning |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Document Status** | Locked |
| **Next Stage** | ERD-27 Detailed ERD |
| **Schema / Prefix (proposed)** | `ai` / `ai_` |
| **Business Entities (recommended)** | Exactly **34** |
| **Aligned To** | FRD-27 (Locked v1.1) · Architecture Lock v1.1 (C-01–C-06) · FRD-01 Foundation · FRD-25 BPM · FRD-26 Low-Code · FRD-18 Analytics · FRD-19 Document · FRD-21 Integration Hub |
| **Prior Release** | ERP Core v1.21-beta |

> **Planning only.** No Mermaid, SQL, columns, indexes, PK/FK diagrams, migrations, APIs, repository design, service layer, or implementation in this document.

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-23 | Initial Entity Planning for Enterprise AI Platform (34 entities after justified merges). Ready for Architect Review. |
| 1.1 | 2026-07-23 | Editorial Lock after Architecture Review. Added Entity Design Principles, Entity Classification, Dependency Overview, Recommended Implementation Order, and Enterprise AI Ownership Summary. No functional changes. No entity added or removed. Still exactly 34 entities. |

---

## Entity Design Principles

| Principle | Statement |
|-----------|-----------|
| **AI owns AI artifacts only** | AI Platform is intelligence SoR — not business documents, masters, or ledgers |
| **Version-first architecture** | Publishable AI artifacts are versioned; runtime binds exact published versions |
| **Published immutability** | Published versions are never silently replaced |
| **UUID references only** | Peer domains are referenced by UUID / module code — never peer schema FKs |
| **Contracts only** | Cross-module reads/writes use owning-module service contracts |
| **No peer ORM** | AI never writes peer-module ORM models |
| **AI recommendations never replace business authority** | AI recommends; BPM and Business Modules remain execution authorities |
| **Foundation ownership preserved** | AuthN · AuthZ · RBAC · Audit · Notification · Workflow Engine unchanged |
| **BPM ownership preserved** | Workflow design and runtime remain BPM / Foundation Workflow |
| **Low-Code ownership preserved** | Forms / pages / components remain Low-Code Platform |

---

## 1. Purpose

Entity Planning freezes the **complete business-entity inventory** for the Enterprise AI Platform before Detailed ERD and backend implementation.

Later ERD design and implementation **must use only these entities**. No new AI Platform entities may appear during implementation without formal architecture approval.

This document exists to:

- Translate FRD-27 capabilities into a governed entity set
- Preserve Architecture Lock v1.1 and cross-module ownership boundaries
- Prevent over-normalization and SoR duplication
- Provide a locked planning baseline for Detailed ERD-27

---

## 2. Scope

This document identifies **business entities only**.

| In Scope | Out of Scope |
|----------|--------------|
| Entity names, purpose, ownership, lifecycle, notes | SQL · columns · data types |
| Ownership matrix · cross-module UUID references | Indexes · constraints · PK/FK diagrams |
| Coverage of FRD-27 capabilities | Mermaid · relationship detail diagrams |
| Justified merges / splits of candidate entities | APIs · repositories · services |
| Validation that inventory is complete | Migrations · backend implementation · sprint reports |

**No schema. No implementation. No Detailed ERD in this document.**

---

## 3. Entity Planning Principles

| Principle | Application |
|-----------|-------------|
| AI Platform owns only AI artifacts | Prompts, models/providers, sessions, knowledge index metadata, agents/tools, policies, usage/cost, evaluations — not business documents |
| Business modules remain SoR | AI never owns PO, invoice, leave, ticket, journal, or other transactional data |
| Foundation ownership preserved | AuthN · AuthZ · RBAC · Audit · Notification · Workflow Engine unchanged |
| BPM ownership preserved | Workflow design/runtime remains FRD-25 / Foundation Workflow |
| Low-Code ownership preserved | Forms/pages/components remain FRD-26 |
| Document ownership preserved | Files remain Document Management; AI stores document UUID refs only |
| Analytics ownership preserved | Reporting warehouse remains Analytics; AI exposes metrics for read-only consumption |
| Integration Hub ownership preserved | External connector transport remains C-03 where required |
| UUID references only | Peer entities referenced by UUID / module code — never peer FKs to foreign schemas |
| No peer ORM | No SQLAlchemy/ORM writes into peer module models |
| Version-first architecture | Prompt, agent, tool, knowledge pack, guardrail, and provider configuration are versioned where applicable |
| Draft → Publish → Retire | Lifecycle for publishable AI artifacts |
| Published immutability | Published versions are never silently replaced |
| Clean Architecture · DDD · Modular Monolith | Required at implementation time; not prescribed here as schema |

### Coverage → Entity Mapping (justified merges)

| FRD / Planning Concern | Entity Decision |
|------------------------|-----------------|
| LLM / embedding / multimodal providers | `ai_provider` |
| Model registry | `ai_model` |
| Prompt templates / versions / variables | `ai_prompt_template` · `ai_prompt_version` · `ai_prompt_variable` |
| Enterprise AI Assistant · AI Copilot | **Merged** into `ai_assistant` (kind = assistant \| copilot) |
| AI Agent · Agent Version | `ai_agent` · `ai_agent_version` |
| AI Skill | `ai_skill` |
| AI Function · AI Tool · Tool Version | **Function merged** into `ai_tool`; versions in `ai_tool_version` |
| Knowledge Base · Source · Chunk | `ai_knowledge_base` · `ai_knowledge_source` · `ai_knowledge_chunk` |
| Embedding · Vector Index | `ai_embedding` · `ai_vector_index` |
| AI Session · Conversation · Message · Memory · Context | `ai_session` · `ai_conversation` · `ai_conversation_message` · `ai_conversation_memory` · `ai_context_package` |
| AI Gateway Policy · Routing Rule | `ai_gateway_policy` · `ai_routing_rule` |
| Guardrail · Moderation | `ai_guardrail_policy` · `ai_moderation_policy` |
| Evaluation · Evaluation Result | **Results merged** into `ai_evaluation` |
| Feedback | `ai_feedback` |
| Usage · Cost | `ai_usage_record` · `ai_cost_record` |
| Rate Limit · Cache · Configuration | `ai_rate_limit_policy` · `ai_cache_entry` · `ai_configuration` |
| Provider Credential Reference | `ai_provider_credential_reference` (secret-store pointer only) |
| OCR / STT / TTS / Vision integration points | **Merged** into `ai_multimodal_profile` (+ provider capability via `ai_provider`) |
| Audit Event Reference | **Not an AI SoR entity** — Foundation Audit remains C-06; AI emits events by contract |

### Entity Classification

| Group | Entities |
|-------|----------|
| **Core AI** | `ai_provider` · `ai_model` · `ai_prompt_template` · `ai_prompt_version` · `ai_prompt_variable` · `ai_assistant` · `ai_agent` · `ai_agent_version` · `ai_skill` · `ai_tool` · `ai_tool_version` |
| **Knowledge** | `ai_knowledge_base` · `ai_knowledge_source` · `ai_knowledge_chunk` · `ai_embedding` · `ai_vector_index` |
| **Runtime** | `ai_session` · `ai_conversation` · `ai_conversation_message` · `ai_conversation_memory` · `ai_context_package` |
| **Governance** | `ai_gateway_policy` · `ai_routing_rule` · `ai_guardrail_policy` · `ai_moderation_policy` · `ai_evaluation` · `ai_feedback` · `ai_rate_limit_policy` · `ai_configuration` · `ai_provider_credential_reference` |
| **Operations** | `ai_usage_record` · `ai_cost_record` · `ai_cache_entry` |
| **Future Ready** | `ai_multimodal_profile` |

*Classification is documentation-only. Entity count remains exactly **34**.*

### Dependency Overview

```text
Provider
  ↓
Model
  ↓
Prompt Template
  ↓
Prompt Version
  ↓
Assistant
  ↓
Agent (Agent Version · Skill · Tool · Tool Version)

Knowledge
  ↓
Knowledge Base
  ↓
Knowledge Source
  ↓
Knowledge Chunk
  ↓
Embedding
  ↓
Vector Index

Governance
  ↓
Gateway Policy
  ↓
Routing Rule
  ↓
Guardrail Policy
  ↓
Moderation Policy

Runtime
  ↓
Session
  ↓
Conversation
  ↓
Message / Memory / Context Package

Operations
  ↓
Usage Record · Cost Record · Cache Entry · Configuration
```

ASCII only. No Mermaid. No relationship cardinality. No schema.

### Recommended Implementation Order

Planning hint only — **not** a sprint plan and **not** implementation:

| Order | Group | Entities (indicative) |
|------:|-------|------------------------|
| 1 | Core registry | `ai_provider` · `ai_model` · `ai_provider_credential_reference` · `ai_configuration` |
| 2 | Prompt spine | `ai_prompt_template` · `ai_prompt_version` · `ai_prompt_variable` |
| 3 | Governance controls | `ai_gateway_policy` · `ai_routing_rule` · `ai_guardrail_policy` · `ai_moderation_policy` · `ai_rate_limit_policy` |
| 4 | Assistant surfaces | `ai_assistant` |
| 5 | Runtime conversation | `ai_session` · `ai_conversation` · `ai_conversation_message` · `ai_conversation_memory` · `ai_context_package` |
| 6 | Operations telemetry | `ai_usage_record` · `ai_cost_record` · `ai_cache_entry` |
| 7 | Knowledge / RAG | `ai_knowledge_base` · `ai_knowledge_source` · `ai_knowledge_chunk` · `ai_embedding` · `ai_vector_index` |
| 8 | Agents & tools | `ai_skill` · `ai_tool` · `ai_tool_version` · `ai_agent` · `ai_agent_version` |
| 9 | Evaluation & feedback | `ai_evaluation` · `ai_feedback` |
| 10 | Future ready | `ai_multimodal_profile` |

No APIs, migrations, repositories, or services are prescribed here.

---

## 4. Entity Inventory

### 1. `ai_provider`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Provider |
| **Purpose** | Registry of LLM, embedding, and multimodal providers available to the AI Gateway. |
| **Ownership** | AI Platform |
| **Lifecycle** | Active / Suspended / Retired |
| **Notes** | Provider-agnostic registry. No provider-specific business logic in ERP. Credentials never stored here. |

### 2. `ai_model`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Model |
| **Purpose** | Catalog of models (capability, modality, limits, cost class, residency, governance status). |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft / Approved / Deprecated / Retired |
| **Notes** | Bound to a provider by UUID reference within AI schema only. |

### 3. `ai_prompt_template`

| Field | Value |
|-------|--------|
| **Entity Name** | Prompt Template |
| **Purpose** | Stable identity for a reusable enterprise prompt template. |
| **Ownership** | AI Platform |
| **Lifecycle** | Active catalog identity (versions carry publish state) |
| **Notes** | SoR for prompt identity. Workloads bind to published prompt versions. |

### 4. `ai_prompt_version`

| Field | Value |
|-------|--------|
| **Entity Name** | Prompt Version |
| **Purpose** | Draft / Published / Retired prompt content and parameters; published versions immutable. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Version Compatibility Policy: runtime resolves exact published version bound at invoke time. |

### 5. `ai_prompt_variable`

| Field | Value |
|-------|--------|
| **Entity Name** | Prompt Variable |
| **Purpose** | Typed parameter definitions for a prompt version (names, types, requiredness metadata). |
| **Ownership** | AI Platform |
| **Lifecycle** | Follows parent prompt version (editable only while Draft) |
| **Notes** | No secrets as variable defaults. Values supplied at runtime from authorized context. |

### 6. `ai_assistant`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Assistant (includes Copilot) |
| **Purpose** | Governed assistant/copilot surface definition: bound prompt version, policies, allowed corpora/tools, host context. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | **Merged:** Assistant + Copilot. Distinguishes kind without duplicating SoR. Module-hosted UX allowed; AI owns definition. |

### 7. `ai_agent`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Agent |
| **Purpose** | Stable identity for a governed agent (goals, ownership, risk class). |
| **Ownership** | AI Platform |
| **Lifecycle** | Active catalog identity (versions carry publish state) |
| **Notes** | Agents recommend/act via tools only; never become business decision authority. |

### 8. `ai_agent_version`

| Field | Value |
|-------|--------|
| **Entity Name** | Agent Version |
| **Purpose** | Draft / Published / Retired agent configuration: prompt bindings, allowed skills/tools, stop limits, HITL policy hooks. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Published immutability. Orchestration limits are metadata, not a second workflow engine. |

### 9. `ai_skill`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Skill |
| **Purpose** | Reusable skill package that composes tools/prompts for agents. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Skills Registry SoR. Skills do not own business transactions. |

### 10. `ai_tool`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Tool (includes Function) |
| **Purpose** | Approved callable tool/function registration: schema identity, side-effect class, auth scope metadata. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | **Merged:** Function Registry into Tool Registry. Allow-list only. Side effects execute via owning-module contracts, never peer ORM. |

### 11. `ai_tool_version`

| Field | Value |
|-------|--------|
| **Entity Name** | Tool Version |
| **Purpose** | Versioned tool schema and contract metadata; breaking changes require deliberate agent rebind. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Version Compatibility Policy artifact. |

### 12. `ai_knowledge_base`

| Field | Value |
|-------|--------|
| **Entity Name** | Knowledge Base |
| **Purpose** | Registered enterprise knowledge corpus metadata (ownership, classification, retention, access policy). |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Index metadata SoR only. Original files remain Document Management. |

### 13. `ai_knowledge_source`

| Field | Value |
|-------|--------|
| **Entity Name** | Knowledge Source |
| **Purpose** | Registered source within a knowledge base (document UUID, curated pack, approved extract contract). |
| **Ownership** | AI Platform |
| **Lifecycle** | Active / Suspended / Retired |
| **Notes** | Document UUID references only — Document remains file SoR. |

### 14. `ai_knowledge_chunk`

| Field | Value |
|-------|--------|
| **Entity Name** | Knowledge Chunk |
| **Purpose** | Chunk metadata produced during ingestion for retrieval (not a document SoR). |
| **Ownership** | AI Platform |
| **Lifecycle** | Created on ingest · invalidated on source update/retire |
| **Notes** | Supports RAG grounding/citations. No business ledger rows stored as chunks. |

### 15. `ai_embedding`

| Field | Value |
|-------|--------|
| **Entity Name** | Embedding |
| **Purpose** | Embedding generation metadata linking chunks/models for semantic retrieval. |
| **Ownership** | AI Platform |
| **Lifecycle** | Created / Rebuilt / Invalidated |
| **Notes** | Storage technology deferred to Detailed ERD. Entity freezes the business concept only. |

### 16. `ai_vector_index`

| Field | Value |
|-------|--------|
| **Entity Name** | Vector Index |
| **Purpose** | Registered vector index for a knowledge base / embedding model combination. |
| **Ownership** | AI Platform |
| **Lifecycle** | Active / Rebuilding / Retired |
| **Notes** | Enables semantic/vector search under RBAC corpus policy. |

### 17. `ai_session`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Session |
| **Purpose** | Runtime AI session control record (user/tenant/workload, bound versions, status, retention clock). |
| **Ownership** | AI Platform |
| **Lifecycle** | Open → Active → Closed / Expired |
| **Notes** | Session management SoR. Does not own business case records. |

### 18. `ai_conversation`

| Field | Value |
|-------|--------|
| **Entity Name** | Conversation |
| **Purpose** | Conversation thread within an AI session. |
| **Ownership** | AI Platform |
| **Lifecycle** | Active → Archived / Purged per retention |
| **Notes** | Privacy and retention controlled by policy. |

### 19. `ai_conversation_message`

| Field | Value |
|-------|--------|
| **Entity Name** | Conversation Message |
| **Purpose** | Individual user / assistant / tool / system messages in a conversation. |
| **Ownership** | AI Platform |
| **Lifecycle** | Append-oriented within retention window |
| **Notes** | May reference prompt/model/tool versions by UUID. Not a business transaction log. |

### 20. `ai_conversation_memory`

| Field | Value |
|-------|--------|
| **Entity Name** | Conversation Memory |
| **Purpose** | Governed memory summaries / long-term memory entries under privacy rules. |
| **Ownership** | AI Platform |
| **Lifecycle** | Active → Expired / Purged |
| **Notes** | Optional; never cross-tenant. Not Master Data. |

### 21. `ai_context_package`

| Field | Value |
|-------|--------|
| **Entity Name** | Context Package |
| **Purpose** | Assembled authorized context snapshot for an invocation (module, entity UUID, retrieved chunk refs, prompt version). |
| **Ownership** | AI Platform |
| **Lifecycle** | Ephemeral / retained per audit-lite policy |
| **Notes** | Context management SoR. Contains references only — not peer business row copies as SoR. |

### 22. `ai_gateway_policy`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Gateway Policy |
| **Purpose** | Gateway-level policy packs (allow/deny, residency, workload class, kill-switch hooks). |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Policy before model. Published versions immutable. |

### 23. `ai_routing_rule`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Routing Rule |
| **Purpose** | Rules selecting provider/model by capability, cost, latency, residency, failover. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Provider Configuration Version Compatibility artifact family. |

### 24. `ai_guardrail_policy`

| Field | Value |
|-------|--------|
| **Entity Name** | Guardrail Policy |
| **Purpose** | Versioned safety/guardrail packs applied pre/during/post invocation. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Fail closed for protected workloads when unavailable. |

### 25. `ai_moderation_policy`

| Field | Value |
|-------|--------|
| **Entity Name** | Moderation Policy |
| **Purpose** | Content moderation classes and actions (block / escalate / redact). |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Complements guardrails; does not replace Foundation security. |

### 26. `ai_evaluation`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Evaluation |
| **Purpose** | Evaluation run against published prompt/knowledge/guardrail configurations (quality, groundedness, safety) including result summary. |
| **Ownership** | AI Platform |
| **Lifecycle** | Queued → Running → Completed / Failed |
| **Notes** | **Merged:** Evaluation Result into Evaluation. Async-capable. Never mutates business SoR. |

### 27. `ai_feedback`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Feedback |
| **Purpose** | User/operator feedback on AI outputs (rating, comments, correction flags). |
| **Ownership** | AI Platform |
| **Lifecycle** | Captured → Reviewed / Closed |
| **Notes** | May open Foundation/BPM review workflows by UUID contract; AI does not own case SoR. |

### 28. `ai_usage_record`

| Field | Value |
|-------|--------|
| **Entity Name** | Usage Record |
| **Purpose** | Usage telemetry (calls, tokens, workload, tenant/user) for governance. |
| **Ownership** | AI Platform |
| **Lifecycle** | Append-oriented operational record |
| **Notes** | Operational metadata. Analytics may consume read-only aggregates. |

### 29. `ai_cost_record`

| Field | Value |
|-------|--------|
| **Entity Name** | Cost Record |
| **Purpose** | Cost estimates/actuals for chargeback and budget governance. |
| **Ownership** | AI Platform |
| **Lifecycle** | Append-oriented operational record |
| **Notes** | Complements usage records. Not Finance GL SoR. |

### 30. `ai_rate_limit_policy`

| Field | Value |
|-------|--------|
| **Entity Name** | Rate Limit Policy |
| **Purpose** | Quotas and rate limits per tenant/role/workload. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | Enforced by gateway; excess traffic queued/rejected per policy. |

### 31. `ai_cache_entry`

| Field | Value |
|-------|--------|
| **Entity Name** | Cache Entry |
| **Purpose** | Eligible idempotent retrieval/generation cache entries under policy. |
| **Ownership** | AI Platform |
| **Lifecycle** | Created → Expired / Invalidated |
| **Notes** | Cache is **not** SoR. Must not disable guardrails. |

### 32. `ai_configuration`

| Field | Value |
|-------|--------|
| **Entity Name** | AI Configuration |
| **Purpose** | Platform / tenant / workload configuration settings for AI enablement. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Active → Retired |
| **Notes** | No secrets in configuration values. |

### 33. `ai_provider_credential_reference`

| Field | Value |
|-------|--------|
| **Entity Name** | Provider Credential Reference |
| **Purpose** | Pointer/reference to enterprise secret-store credentials for a provider — never the secret itself. |
| **Ownership** | AI Platform |
| **Lifecycle** | Active / Rotated / Retired |
| **Notes** | Secrets remain in enterprise secret stores. Aligns with FRD security rules. |

### 34. `ai_multimodal_profile`

| Field | Value |
|-------|--------|
| **Entity Name** | Multimodal Profile |
| **Purpose** | Integration profile for OCR, Speech-to-Text, Text-to-Speech, Vision, and future multimodal workloads under the same gateway/governance model. |
| **Ownership** | AI Platform |
| **Lifecycle** | Draft → Publish → Retire |
| **Notes** | **Merged:** OCR / Speech / Vision provider reference concepts. Does not own media files (Document UUID refs only). |

---

## 5. Entity Ownership Matrix

| Entity | Owner | Reason |
|--------|--------|--------|
| `ai_provider` | AI Platform | Provider registry is AI control-plane SoR |
| `ai_model` | AI Platform | Model catalog is AI control-plane SoR |
| `ai_prompt_template` | AI Platform | Prompt identity SoR |
| `ai_prompt_version` | AI Platform | Prompt version SoR |
| `ai_prompt_variable` | AI Platform | Prompt parameterization metadata |
| `ai_assistant` | AI Platform | Assistant/copilot definition SoR |
| `ai_agent` | AI Platform | Agent identity SoR |
| `ai_agent_version` | AI Platform | Agent version SoR |
| `ai_skill` | AI Platform | Skills registry SoR |
| `ai_tool` | AI Platform | Tool/function registry SoR |
| `ai_tool_version` | AI Platform | Tool version SoR |
| `ai_knowledge_base` | AI Platform | Knowledge corpus metadata SoR |
| `ai_knowledge_source` | AI Platform | Source registration metadata |
| `ai_knowledge_chunk` | AI Platform | Chunk metadata for RAG |
| `ai_embedding` | AI Platform | Embedding metadata |
| `ai_vector_index` | AI Platform | Vector index registration |
| `ai_session` | AI Platform | Session control SoR |
| `ai_conversation` | AI Platform | Conversation thread SoR |
| `ai_conversation_message` | AI Platform | Message history (retention-bound) |
| `ai_conversation_memory` | AI Platform | Governed memory metadata |
| `ai_context_package` | AI Platform | Context assembly snapshot |
| `ai_gateway_policy` | AI Platform | Gateway policy SoR |
| `ai_routing_rule` | AI Platform | Routing policy SoR |
| `ai_guardrail_policy` | AI Platform | Safety pack SoR |
| `ai_moderation_policy` | AI Platform | Moderation pack SoR |
| `ai_evaluation` | AI Platform | Evaluation run SoR |
| `ai_feedback` | AI Platform | Feedback capture SoR |
| `ai_usage_record` | AI Platform | Usage telemetry SoR |
| `ai_cost_record` | AI Platform | Cost telemetry SoR |
| `ai_rate_limit_policy` | AI Platform | Quota policy SoR |
| `ai_cache_entry` | AI Platform | Cache metadata (non-SoR data) |
| `ai_configuration` | AI Platform | AI configuration SoR |
| `ai_provider_credential_reference` | AI Platform | Secret-store pointer metadata |
| `ai_multimodal_profile` | AI Platform | Multimodal integration profile SoR |
| Authentication / sessions / RBAC | **Foundation** | Identity authority |
| Audit events | **Foundation Audit** | C-06 — AI emits, does not own warehouse |
| Notifications | **Foundation Notification** | C-05 — AI does not own delivery |
| Workflow instances / tasks | **BPM / Foundation Workflow** | C-04 — AI does not own workflow |
| Forms / pages | **Low-Code** | FRD-26 |
| Files / documents | **Document Management** | File SoR |
| Enterprise reports | **Analytics** | Reporting SoR |
| External connectors | **Integration Hub** | C-03 transport |
| Business documents / masters | **Business Modules / Master Data / Organization** | Business SoR / C-01 |

### Enterprise AI Ownership Summary

| AI owns | AI does NOT own |
|---------|-----------------|
| Providers · models · credential references | Authentication · Authorization · RBAC |
| Prompt templates · versions · variables | Foundation Audit warehouse |
| Assistants (incl. copilots) · agents · skills · tools | Notification delivery |
| Knowledge base / source / chunk · embedding · vector index metadata | Workflow design · instances · tasks · history |
| Sessions · conversations · messages · memory · context packages | Forms · pages · components (Low-Code) |
| Gateway · routing · guardrail · moderation · rate-limit policies | Document / file storage |
| Evaluations · feedback | Enterprise BI / reporting warehouse |
| Usage · cost · cache · configuration | Integration Hub transport |
| Multimodal profiles | Business transactions · masters · ledgers |

---

## 6. Cross Module References

AI Platform may reference peer domains by **UUID / module code / service contract only**. No ownership duplication. No peer ORM.

| Peer Domain | Expected UUID / Contract References | AI Must Not Own |
|-------------|-------------------------------------|-----------------|
| **Foundation** | `tenant_id`, `user_id`, RBAC permission checks, Audit correlation ids, optional Notification request ids | AuthN/AuthZ, Audit warehouse, Notification delivery, Workflow Engine |
| **Organization** | Company / branch / org-unit UUID for scoping | Org masters |
| **Master Data** | Party / item / other master UUID for context | Master records (C-01) |
| **Document** | Document / file UUID for knowledge ingestion and multimodal context | File storage / document SoR |
| **Analytics** | None as FK; AI exposes metrics for read-only consumption | BI warehouse / reporting SoR |
| **Low-Code** | Form definition/version UUID, page definition/version UUID for copilots | Forms/pages/components |
| **Workflow / BPM** | Workflow definition/version UUID, instance UUID, task UUID for HITL / process-aware assistance | Workflow design, instances, tasks, history |
| **Business Modules** | `module_code` + `entity_id` UUID for context and write proposals | Business transactions and ledgers |
| **Integration Hub** | Connector / integration run UUID where external transport is used | External transport SoR |

---

## 7. Dependency Notes

| Rule | Statement |
|------|-----------|
| **Version-first** | Prompt, agent, tool, knowledge pack, guardrail, moderation, gateway/routing, multimodal profile, and provider configuration are versioned where publishable |
| **Publish lifecycle** | Draft → Review/Evaluation → Approval → Publish → Production → Monitoring → Feedback → Retire (FRD-27 lifecycle) |
| **Published immutability** | Published versions never silently replaced |
| **No peer ORM** | AI services must not import or write peer module ORM models |
| **UUID references** | All peer links are UUID / module-code oriented |
| **Contracts only** | Reads/writes to business data go through owning module services |
| **No business data ownership** | AI is intelligence SoR only |
| **AI Decision Boundary** | AI recommends; BPM and Business Modules remain execution authorities |
| **Architecture Lock v1.1** | Final — never modified by this planning document |

---

## 8. Validation Table

| Gate | Result |
|------|--------|
| Every FRD-27 capability represented (Core · Extension · multimodal integration points) | ✓ |
| Justified merges documented (Assistant+Copilot · Function→Tool · Evaluation Result → Evaluation · OCR/STT/TTS/Vision → Multimodal Profile) | ✓ |
| Audit remains Foundation (no competing AI audit warehouse entity) | ✓ |
| No duplicate ownership vs Foundation · BPM · Low-Code · Document · Analytics · Integration Hub · Business Modules | ✓ |
| Architecture Lock v1.1 preserved (C-01–C-06) | ✓ |
| FRD-27 unchanged | ✓ |
| UUID references only · no peer ORM · contracts only | ✓ |
| Version-first · Draft/Publish/Retire · published immutability where applicable | ✓ |
| No entity added | ✓ |
| No entity removed | ✓ |
| Still exactly **34** entities | ✓ |
| Ownership unchanged | ✓ |
| No implementation | ✓ |
| No SQL | ✓ |
| No APIs | ✓ |
| No Detailed ERD / Mermaid / indexes / constraints / repositories / services | ✓ |
| Documentation only (editorial lock) | ✓ |
| Ready for ERD-27 Detailed ERD | ✓ |

---

## Document Status

| Field | Value |
|-------|--------|
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Document Status** | Locked |
| **Next Stage** | ERD-27 Detailed ERD |
| **Recommended Entity Count** | **34** |

### Entity Lifecycle (documentation process)

```text
Draft Entity Planning
        ↓
Architect Review
        ↓
Entity Planning Locked
        ↓
Detailed ERD Design
        ↓
Backend Implementation
```

This is documentation only.

---

## Closing Statement

ERD-27 Entity Planning is now the frozen planning baseline.

Future Detailed ERD and backend implementation must follow this document unless superseded through formal architecture review.
