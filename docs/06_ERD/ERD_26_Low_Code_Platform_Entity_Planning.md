# ERD-26 — Entity Planning  
## Low-Code Platform

| Field | Value |
|-------|--------|
| **Document** | ERD-26 Entity Planning |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Document Status** | Locked |
| **Next Stage** | Detailed ERD Design |
| **Schema / Prefix (proposed)** | `lowcode` / `lc_` |
| **Business Tables (recommended)** | Exactly **18** |
| **Aligned To** | FRD-26 (Locked v1.1) · FRD-25 (BPM form references) · Architecture Lock v1.1 (C-01–C-06) |
| **Prior Release** | ERP Core v1.20-beta |

> **Planning only.** No Mermaid, SQL, columns, indexes, PK/FK diagrams, migrations, APIs, or implementation in this document.

### Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial Entity Planning for Low-Code Platform (18 entities). Ready for Architect Review. |
| 1.1 | 2026-07-22 | Editorial Lock after Architecture Review. No functional or entity changes. |

---

## Entity Design Principles (applied)

| Principle | Application |
|-----------|-------------|
| Avoid over-normalization | Field validation + bindings live on `lc_form_field`; component properties live on `lc_component_version`; submission values live on `lc_runtime_submission` |
| Version is the design unit | Fields, sections, events, expression bindings, and localization hang off **form/page versions** |
| Published immutability | Published versions never silently replaced (FRD-26 Version Compatibility Policy) |
| Orchestration only | Submissions correlate handoff; **business SoR stays in modules** |
| BPM contract | BPM stores **form UUID only**; Low-Code resolves published form versions |
| Foundation remains SoR | RBAC · Audit · Notification · Workflow Engine unchanged |
| No peer ORM | Data sources are contract registries (module code + entity type), not peer FKs |

### Coverage → Entity Mapping

| FRD / Planning Concern | Entity Decision |
|------------------------|-----------------|
| Form Categories | `lc_form_category` |
| Form Definitions / Versions | `lc_form_definition` · `lc_form_version` |
| Field Groups / Sections | `lc_form_section` |
| Form Fields · Validation · Bindings | **Merged** into `lc_form_field` |
| Page Definitions / Versions / Regions | `lc_page_definition` · `lc_page_version` · `lc_page_region` |
| Component Catalog · Properties · Versions | `lc_component` · `lc_component_version` (**properties merged**) |
| Data Sources | `lc_data_source` |
| Expression Definitions / Bindings | `lc_expression` · `lc_expression_binding` |
| Runtime Events | `lc_event_handler` |
| Form / Page Localization | **Merged** into `lc_localization_entry` |
| Publish History | `lc_publish_history` |
| Runtime Submission · Values · Context | `lc_runtime_submission` (**values + context merged**) |
| Preview Session | `lc_preview_session` |

---

## 1. Entity Planning

### 1. `lc_form_category`

| Field | Value |
|-------|--------|
| **Entity Name** | Form Category |
| **Purpose** | Organize form definitions in the enterprise catalog (module-agnostic grouping / tags hierarchy root). |
| **Owned By** | Low-Code Platform |
| **Depends On** | Tenant / company scope (Foundation tenancy patterns) |
| **Important Relationships** | One category → many form definitions |
| **Notes** | Catalog navigation only. Does not own business processes. |

### 2. `lc_form_definition`

| Field | Value |
|-------|--------|
| **Entity Name** | Form Definition |
| **Purpose** | Stable identity for a dynamic form across versions (code, name, module affinity, owner). |
| **Owned By** | Low-Code Platform |
| **Depends On** | Optional `lc_form_category` |
| **Important Relationships** | One definition → many form versions; referenced by BPM / modules via UUID/key |
| **Notes** | **SoR for form identity.** BPM `bpm_form_reference` stores this UUID only (FRD-25 / FRD-26). |

### 3. `lc_form_version`

| Field | Value |
|-------|--------|
| **Entity Name** | Form Version |
| **Purpose** | Draft / Published / Retired lifecycle unit; published versions are immutable. |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_form_definition` |
| **Important Relationships** | Parent of sections, fields, event handlers, expression bindings, localization; target of page embeds and runtime resolution |
| **Notes** | Runtime resolves the **exact published version bound** at binding time (Version Compatibility Policy). |

### 4. `lc_form_section`

| Field | Value |
|-------|--------|
| **Entity Name** | Form Section (Field Group) |
| **Purpose** | Group fields into sections / panels within a form version. |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_form_version` |
| **Important Relationships** | One section → many fields; may bind section-level expressions |
| **Notes** | Design-time layout grouping only. |

### 5. `lc_form_field`

| Field | Value |
|-------|--------|
| **Entity Name** | Form Field |
| **Purpose** | Field definition on a form version: type, component ref, labels, **validation rules**, and **data binding** metadata. |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_form_version`; optional `lc_form_section`; optional `lc_component_version`; optional `lc_data_source` |
| **Important Relationships** | Belongs to version/section; may reference component version; binding points at data-source attribute keys (not peer rows) |
| **Notes** | **Merged:** Field Validation Rules + Field Bindings. Attachment fields reference **Document UUID** only. No peer business FKs. |

### 6. `lc_page_definition`

| Field | Value |
|-------|--------|
| **Entity Name** | Page Definition |
| **Purpose** | Stable identity for a composed page / screen. |
| **Owned By** | Low-Code Platform |
| **Depends On** | Tenant scope |
| **Important Relationships** | One definition → many page versions |
| **Notes** | Page builder SoR identity. Does not replace ERP navigation IA. |

### 7. `lc_page_version`

| Field | Value |
|-------|--------|
| **Entity Name** | Page Version |
| **Purpose** | Draft / Published / Retired page composition version (immutable when published). |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_page_definition` |
| **Important Relationships** | Parent of page regions, page-level events, expression bindings, localization |
| **Notes** | Same publish / compatibility rules as form versions. |

### 8. `lc_page_region`

| Field | Value |
|-------|--------|
| **Entity Name** | Page Layout Region |
| **Purpose** | Layout containers (header, body, sidebar, actions, wizard step) and embeds of published forms / components. |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_page_version`; optional embed of `lc_form_version` and/or `lc_component_version` |
| **Important Relationships** | Ordered regions within a page version; may embed one published form version by reference |
| **Notes** | Embeds **form version UUID**, never copies form field SoR. |

### 9. `lc_component`

| Field | Value |
|-------|--------|
| **Entity Name** | Component Catalog Entry |
| **Purpose** | Governed catalog identity for reusable UI components (text, select, lookup, grid, attachment, etc.). |
| **Owned By** | Low-Code Platform |
| **Depends On** | Platform admin governance |
| **Important Relationships** | One component → many component versions |
| **Notes** | Unapproved components cannot be used in publishable definitions (FRD-26). |

### 10. `lc_component_version`

| Field | Value |
|-------|--------|
| **Entity Name** | Component Version |
| **Purpose** | Versioned component specification including **typed properties**, defaults, and validation hooks. |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_component` |
| **Important Relationships** | Referenced by form fields and page regions at publish time |
| **Notes** | **Merged:** Component Properties. Published forms remain compatible with the component version used at publish (Component Compatibility Policy). Breaking changes require explicit new versions. |

### 11. `lc_data_source`

| Field | Value |
|-------|--------|
| **Entity Name** | Data Source |
| **Purpose** | Registry of module-backed contracts (module code, entity type, allowed operations, attribute catalog metadata). |
| **Owned By** | Low-Code Platform (registry only) |
| **Depends On** | Owning business module / Master Data / Organization **services** (C-01 / C-02) |
| **Important Relationships** | Referenced by form field bindings; never stores business rows |
| **Notes** | **Not** a peer ORM model. Lookups and writes execute only via owning module contracts. |

### 12. `lc_expression`

| Field | Value |
|-------|--------|
| **Entity Name** | Expression Definition |
| **Purpose** | Sandboxed UI expression definitions (visibility, required, enablement, default, calculate). |
| **Owned By** | Low-Code Platform |
| **Depends On** | Tenant scope |
| **Important Relationships** | Bound to targets via `lc_expression_binding` |
| **Notes** | UI logic only — **not** a replacement for BPM Decision Tables / Business Rules. |

### 13. `lc_expression_binding`

| Field | Value |
|-------|--------|
| **Entity Name** | Expression Binding |
| **Purpose** | Attach an expression to a form/page/section/field target for a given version and trigger kind. |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_expression`; target form/page version artifacts |
| **Important Relationships** | Expression → many bindings; binding → one design target |
| **Notes** | Design-time metadata evaluated at preview/runtime. |

### 14. `lc_event_handler`

| Field | Value |
|-------|--------|
| **Entity Name** | Runtime Event Handler |
| **Purpose** | Declares governed handlers for `onLoad` / `onChange` / `onValidate` / `onSubmit` / `onCancel` / custom events on a form or page version. |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_form_version` or `lc_page_version`; optional expression / module callback contract metadata |
| **Important Relationships** | Version → many handlers |
| **Notes** | Not a BPM trigger engine; not Foundation Notification. External transport via Integration Hub patterns when required. |

### 15. `lc_localization_entry`

| Field | Value |
|-------|--------|
| **Entity Name** | Definition Localization |
| **Purpose** | Locale-specific labels and messages for form and page versions. |
| **Owned By** | Low-Code Platform |
| **Depends On** | `lc_form_version` or `lc_page_version` |
| **Important Relationships** | Version → many locale entries |
| **Notes** | **Merged:** Form Localization + Page Localization into one entity keyed by artifact type. |

### 16. `lc_publish_history`

| Field | Value |
|-------|--------|
| **Entity Name** | Publish History |
| **Purpose** | Append-oriented Low-Code record of publish / retire actions (who, when, from→to version, reason). |
| **Owned By** | Low-Code Platform (operational trail) |
| **Depends On** | Form or page definition/version identities |
| **Important Relationships** | Definition lineage → many publish events |
| **Notes** | Complements **Foundation Audit** (C-06); does **not** replace Foundation Audit SoR. Supports FRD publish-activity reporting. |

### 17. `lc_runtime_submission`

| Field | Value |
|-------|--------|
| **Entity Name** | Runtime Submission |
| **Purpose** | Correlation envelope for a runtime submit: resolved form/page version, context (`module_code` + `entity_id` UUID, optional BPM task UUID), validation outcome, and **field values snapshot** prior to handoff. |
| **Owned By** | Low-Code Platform (handoff correlation only) |
| **Depends On** | Published `lc_form_version` and/or `lc_page_version`; business context UUIDs |
| **Important Relationships** | Links design version + runtime context; handoff target is owning module / BPM contract |
| **Notes** | **Merged:** Runtime Submission Values + Runtime Context. **Never** business SoR. No peer ORM writes. Idempotency / retry correlation only. |

### 18. `lc_preview_session`

| Field | Value |
|-------|--------|
| **Entity Name** | Preview Session |
| **Purpose** | Design-time preview session for draft or published definitions with sample/safe context. |
| **Owned By** | Low-Code Platform |
| **Depends On** | Target form/page version; designer user (Foundation identity) |
| **Important Relationships** | Designer → session → version under preview |
| **Notes** | Short-lived / operational. Does not create workflow instances or mutate business SoR. |

---

## 2. Recommended Entity Count

| Metric | Value |
|--------|------:|
| **Recommended business entities** | **18** |
| **Merged (not separate tables)** | Field Validation · Field Binding · Component Properties · Form/Page Localization (unified) · Submission Values · Runtime Context |
| **Explicitly out of Low-Code SoR** | Business transactions · Workflow instances/tasks · Masters · Notification delivery · Audit warehouse · Documents |

**Phaseability (planning hint — not an implementation plan):** Design spine (categories · definitions · versions) → Form structure (sections · fields) → Components & data sources → Expressions/events/localization → Pages → Publish history → Preview/runtime submission.

---

## Entity Ownership Summary

| Domain | Responsibility |
|---------|----------------|
| Low-Code Platform | Owns all 18 `lc_*` entities |
| BPM | Stores Form UUID references only |
| Foundation | RBAC · Audit · Notification · Workflow Engine |
| Business Modules | Business Data System of Record |
| Document Management | Document/File ownership |
| Integration Hub | External transport only |
| Analytics | Reporting consumption |

---

## 3. Architecture Notes

### Cross Module Ownership

| Concern | System of Record | Low-Code Role |
|---------|------------------|---------------|
| Form / page / component / expression definitions | **Low-Code** | Owns |
| Form/page versions, sections, fields, regions, events, localization | **Low-Code** | Owns |
| Data source **registry** | **Low-Code** | Owns registry; **modules** own data |
| Publish history (operational) | **Low-Code** | Owns trail; **Foundation Audit** remains enterprise audit SoR |
| Runtime submission correlation | **Low-Code** | Handoff envelope only |
| Business documents / ledgers | **Owning business module** | Submit via contracts |
| Masters (party / item / org) | **Master Data / Organization (C-01)** | Lookup via services |
| Form references on BPM | **BPM** stores UUID; **Low-Code** resolves | Fulfills FRD-25 / FRD-26 |
| Workflow instances / tasks / history | **BPM / Foundation Workflow (C-04)** | Never owned by Low-Code |
| Notifications | **Foundation Notification (C-05)** | Optional notify-on-publish only |
| Audit | **Foundation Audit (C-06)** | Consumes / complements |
| Documents / files | **Document Management** | Attachment UUID refs only |
| External connectors | **Integration Hub (C-03)** | Transport only |
| Enterprise BI | **Analytics** | Read-only metrics |

### Dependency Notes

```text
lc_form_category
        ↓
lc_form_definition
        ↓
lc_form_version  ←── lc_publish_history
        ├── lc_form_section
        │         └── lc_form_field  → lc_component_version
        │                            → lc_data_source (contract key)
        ├── lc_event_handler
        ├── lc_expression_binding → lc_expression
        └── lc_localization_entry

lc_component
        ↓
lc_component_version   (properties merged)

lc_page_definition
        ↓
lc_page_version  ←── lc_publish_history
        ├── lc_page_region  → embeds lc_form_version (UUID)
        ├── lc_event_handler
        ├── lc_expression_binding → lc_expression
        └── lc_localization_entry

Runtime:
lc_preview_session      → form/page version (design-time)
lc_runtime_submission   → published form/page version
                        → module_code + entity_id UUID
                        → optional BPM task UUID
                        → handoff to owning module / BPM (no peer ORM)
```

**Dependency rules (planning):**

1. **Version is the design unit** for forms and pages.
2. **Published versions are immutable**; upgrades are explicit and auditable.
3. **BPM stores form UUID only**; Low-Code resolves the bound published version.
4. **Business entity references are UUID-only** (`module_code` + `entity_id`).
5. **No peer ORM writes**; data sources are contracts, not FKs into peer schemas.
6. **Expressions are UI logic**; BPM retains decision/routing SoR.
7. **Foundation owns RBAC, Audit, Notification, Workflow Engine.**
8. **Document Management owns files**; Low-Code stores document UUID references only.
9. **Exactly 18 recommended business entities** after justified merges.
10. **C-01–C-06 and Architecture Lock v1.1 preserved.**

---

## Entity Lifecycle

```text
Draft
        ↓
Architect Review
        ↓
Entity Planning Locked
        ↓
Detailed ERD Design
        ↓
Backend Implementation
        ↓
Frontend Implementation
```

This is documentation only.

---

## 4. Validation Table

| Gate | Result |
|------|--------|
| FRD-26 SoR (forms · pages · components · expressions) covered | Pass |
| Form/Page draft → publish → retire lifecycle represented | Pass |
| BPM form UUID reference pattern preserved (no form SoR in BPM) | Pass |
| Field validation + bindings merged into `lc_form_field` (no over-normalization) | Pass |
| Component properties merged into `lc_component_version` | Pass |
| Localization unified (`lc_localization_entry`) | Pass |
| Submission values + runtime context merged into `lc_runtime_submission` | Pass |
| Low-Code does **not** own business transactions / masters / workflow instances | Pass |
| Foundation owns RBAC · Audit · Notification · Workflow Engine | Pass |
| Document Management owns files (UUID refs only) | Pass |
| C-01–C-06 / Architecture Lock v1.1 / Modular Monolith / Clean Architecture / DDD | Pass |
| No SQL · Mermaid · PK/FK · columns · indexes · implementation in this document | Pass |
| Recommended entity count phaseable like Sprint 25 | Pass (18) |

---

## 5. Status

| Field | Value |
|-------|--------|
| **Document Status** | Locked |
| **Next Stage** | Detailed ERD Design |

ERD-26 Entity Planning is now locked as the approved planning baseline for the Low-Code Platform.

Future implementation must follow this planning document unless superseded through formal architecture review.

---

**Confirmations**

- FRD-26 unchanged
- No SQL · no Mermaid · no PK/FK · no indexes · no implementation
- Ownership boundaries preserved (Low-Code vs BPM vs Foundation vs business modules)
- Editorial lock only — no functional or entity changes
