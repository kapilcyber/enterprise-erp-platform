# Sprint 26 Phase 1 Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.21-beta (planned) |
| **Sprint** | Sprint 26 — Low-Code Platform |
| **Phase** | Phase 1 — Design Spine (Form Foundation) |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD** | FRD-26 Locked v1.1 |
| **ERD** | ERD-26 Entity Planning Locked v1.1 · ERD-26 Locked v1.1 |
| **Schema / Prefix** | `lowcode` / `lc_` |
| **API Mount** | `/api/v1/lowcode` |
| **Alembic Head** | `0496_seed_lowcode_phase1_permissions` |
| **Phase 1 Tables** | 3 of 18 |
| **Low-Code Tests** | 17 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `lc_form_category` | Category CRUD · Archive · Restore |
| 2 | `lc_form_definition` | Definition CRUD · stable identity · initial draft version seed |
| 3 | `lc_form_version` | Draft · Publish · Retire · Clone Version · Validate Publish |

### Workflow Rules Enforced

- Exactly ONE Published Version per Form Definition
- Draft versions editable
- Published versions immutable
- Retired versions read-only
- Definitions are stable identity (BPM stores Form UUID only)
- Soft delete / archive only — no hard purge
- Company-scoped repository · UUID PKs · audit columns
- No peer ORM · no business data ownership

### Version Strategy

| Topic | Policy |
|-------|--------|
| **Initial Draft Version** | Creating a Form Definition seeds **version_number = 1** as Draft (`v1`) automatically |
| **Version increment policy** | New drafts / clones receive `max(existing version_number) + 1` for that definition |
| **Clone Version** | Clone creates the **next editable Draft** under the same definition; source may be Draft, Published, or Retired; clone sets `cloned_from_version_id` |
| **Create Draft (explicit)** | `POST /versions` also creates the next Draft for an existing definition |
| **Published immutability** | Published versions cannot be edited; upgrades require Clone → edit Draft → Publish |
| **Retired never editable again** | Retired versions are read-only; they never return to Draft or become editable |
| **One Published lineage** | At most one Published version per definition; publishing a new Draft auto-retires any prior Published version |

```text
Definition create
        ↓
Initial Draft v1
        ↓
Edit Draft  →  Publish  →  (immutable Published)
        ↓                      ↓
     Clone ──────────────────→ next Draft (vN+1)
                                 ↓
                              Publish (prior Published auto-retired)
```

### Publish Validation Summary (Phase 1)

Publish **always** executes validation before allowing Publish (`validate-publish` API and inline gate inside `publish`).

| Check | Phase 1 coverage |
|-------|------------------|
| Form Version exists and is tenant/company resolvable | **Enforced** |
| Version status is **Draft** | **Enforced** (`PublishValidationService`) |
| Publish validation runs **before** publish | **Enforced** |
| Exactly one Published version after publish | **Enforced** (prior Published auto-retired on successful publish) |
| Form Definition exists (via version → definition) | **Enforced** for create-draft / list-by-definition paths; publish resolves version first |
| Definition is Active | **Deferred** — fuller definition-status gate when catalog policies harden (later phases) |
| Category is Active | **Deferred** — category optional on definition; active-category gate when binding policy hardens |
| Required form structure metadata (sections / fields) | **Deferred** — structure tables not in Phase 1 |
| Required labels / bindings / expressions | **Deferred** — later design phases |

**Phase 1 publish gate (implemented):** Version must be Draft; validation failure blocks publish.  
**Phase 1 publish side-effect (implemented):** Prior Published version for the same definition is auto-retired so exactly one Published remains.

### Not Implemented (by design)

- Sections · Fields · Pages · Components · Expressions
- Runtime · Preview · Submission · Publish History · Localization · Events
- Remaining 15 of 18 ERD-26 tables
- Prior module redesigns
- Architecture Lock / FRD-26 / ERD-26 changes

---

## Files Created

### Backend — `apps/api/src/modules/lowcode/`

| Area | Files |
|------|--------|
| Package | `__init__.py`, `router.py`, `schemas.py`, `permissions.py`, `dependencies.py`, `tasks.py` |
| Domain | `domain/__init__.py`, `domain/enums.py`, `domain/exceptions.py`, `domain/entities.py`, `domain/value_objects.py` |
| Models | `models/__init__.py`, `models/mixins.py`, `models/form_category.py`, `models/form_definition.py`, `models/form_version.py` |
| Repositories | `repository/base.py`, `repository/code_sequence_repository.py`, `repository/form_category_repository.py`, `repository/form_definition_repository.py`, `repository/form_version_repository.py` |
| Services | `service/__init__.py`, `service/application_service.py`, `service/lowcode_integration_service.py`, `service/lowcode_number_service.py`, `service/lowcode_scope_validator.py`, `service/form_category_service.py`, `service/form_definition_service.py`, `service/form_version_service.py`, `service/publish_validation_service.py` |
| Engines | `service/engines/__init__.py`, `service/engines/form_category_engine.py`, `service/engines/form_definition_engine.py`, `service/engines/form_version_engine.py` |
| Adapters | `adapters/__init__.py`, `adapters/foundation_port.py` |
| Routers | `routers/__init__.py` |

### Migrations — `apps/api/alembic/versions/`

| Revision | File |
|----------|------|
| `0492_create_lowcode_schema` | `0492_create_lowcode_schema.py` |
| `0493_lc_form_category` | `0493_lc_form_category.py` |
| `0494_lc_form_definition` | `0494_lc_form_definition.py` |
| `0495_lc_form_version` | `0495_lc_form_version.py` |
| `0496_seed_lowcode_phase1_permissions` | `0496_seed_lowcode_phase1_permissions.py` |

### Tests — `apps/api/src/tests/`

| Kind | File |
|------|------|
| Unit | `unit/lowcode/test_lowcode_hub_engines.py` |
| Unit | `unit/lowcode/test_lowcode_hub_tasks.py` |
| Security | `security/lowcode/test_lowcode_hub_permissions.py` |
| Integration | `integration/lowcode/test_lowcode_hub_module_import.py` |

### Report

| File |
|------|
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase1_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/shared/router.py` | Registered `lowcode_router` |
| `apps/api/alembic/env.py` | Registered `modules.lowcode.models` |
| `apps/api/src/workers/celery_app.py` | Autodiscover `modules.lowcode` |
| `apps/api/pyproject.toml` | MyPy override `modules.lowcode.*` |

---

## APIs / Routes

**Mount:** `/api/v1/lowcode`  
**Total Phase 1 routes:** 21

### Categories — `/api/v1/lowcode/categories`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `lowcode.category:read` |
| GET | `/{row_id}` | `lowcode.category:read` |
| POST | `` | `lowcode.category:create` |
| PATCH | `/{row_id}` | `lowcode.category:update` |
| POST | `/{row_id}/archive` | `lowcode.category:archive` |
| POST | `/{row_id}/restore` | `lowcode.category:restore` |
| DELETE | `/{row_id}` | `lowcode.category:delete` (soft archive) |

### Definitions — `/api/v1/lowcode/definitions`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `lowcode.definition:read` |
| GET | `/{row_id}` | `lowcode.definition:read` |
| POST | `` | `lowcode.definition:create` |
| PATCH | `/{row_id}` | `lowcode.definition:update` |
| POST | `/{row_id}/archive` | `lowcode.definition:archive` |
| POST | `/{row_id}/restore` | `lowcode.definition:restore` |
| GET | `/{row_id}/versions` | `lowcode.version:read` |

### Versions — `/api/v1/lowcode/versions`

| Method | Path | Permission |
|--------|------|------------|
| GET | `/{row_id}` | `lowcode.version:read` |
| POST | `` | `lowcode.version:create` |
| PATCH | `/{row_id}` | `lowcode.version:update` |
| POST | `/{row_id}/validate-publish` | `lowcode.version:validate` |
| POST | `/{row_id}/publish` | `lowcode.version:publish` |
| POST | `/{row_id}/retire` | `lowcode.version:retire` |
| POST | `/{row_id}/clone` | `lowcode.version:clone` |

---

## Services

| Service | Role |
|---------|------|
| `LowcodeApplicationService` | Application facade |
| `LowcodeIntegrationService` | Cross-module consume ports |
| `LowcodeNumberService` | Document numbering (`FC-` / `FRM-` / `FVER-`) |
| `FormCategoryService` | Category CRUD + activate/deactivate |
| `FormDefinitionService` | Definition CRUD + initial draft version seed |
| `FormVersionService` | Draft / publish / retire / clone lifecycle |
| `PublishValidationService` | Phase 1 publish gate (see Publish Validation Summary) |

---

## Repositories

| Repository |
|------------|
| `FormCategoryRepository` |
| `FormDefinitionRepository` |
| `FormVersionRepository` |
| `CodeSequenceRepository` |
| `LowcodeScopedRepository` (base) |

---

## Permissions

| Permission |
|------------|
| `lowcode.category:read` · `create` · `update` · `delete` · `archive` · `restore` |
| `lowcode.definition:read` · `create` · `update` · `archive` · `restore` |
| `lowcode.version:read` · `create` · `update` · `publish` · `retire` · `clone` · `validate` |

### Roles Seeded

| Role | Slice |
|------|--------|
| `LOWCODE_ADMIN` | All |
| `FORM_DESIGNER` | Design (no publish / retire / delete) |
| `FORM_PUBLISHER` | Read + publish / retire + limited updates |
| `LOWCODE_AUDITOR` | Read |

---

## Tasks

| Celery Task | Name |
|-------------|------|
| `form_inventory_snapshot` | `lowcode.form_inventory_snapshot` |
| `published_version_guard` | `lowcode.published_version_guard` |
| `draft_aging_report` | `lowcode.draft_aging_report` |

---

## Tests

| Suite | Result |
|-------|--------|
| Unit engines | PASS |
| Unit tasks | PASS |
| Security permissions | PASS |
| Integration module import | PASS |
| **Total** | **17 passed** |

---

## Cross-Module Consume (Phase 1)

| Module | Integration |
|--------|-------------|
| Foundation Security | RBAC permissions / roles (consume) |
| Foundation Audit | Publish / create / update / archive audit |
| BPM | Form UUID resolution contract (BPM stores UUID only — unchanged) |

### Runtime Ownership Boundary

| Rule | Statement |
|------|-----------|
| BPM Form reference | BPM stores **Form Definition UUID only** — BPM does **not** own form definitions or versions |
| Low-Code resolve | Low-Code resolves the **Published Form Version** for design-time binding and future runtime render |
| No peer DB coupling | **No direct database dependency** (no ORM FK) between BPM tables and Low-Code tables |
| Future runtime | Consumes **published form metadata only** from Low-Code; Draft is never a production runtime target |
| Business SoR | **Business modules remain System of Record** for transactional data; Low-Code handoff only (later phases) |
| Documents / Notification / Audit / Workflow Engine | Remain Foundation / Document Management ownership — unchanged |

### Do Not Own (confirmed)

Business documents · Masters · Workflow instances · Notification delivery · Audit warehouse · Documents · Sections/Fields/Pages (later phases)

---

## Remaining Work for Phase 2A+

| Area | Remaining ERD Tables / Capabilities |
|------|-------------------------------------|
| Form structure | `lc_form_section`, `lc_form_field` |
| Components | `lc_component`, `lc_component_version` |
| Data / expressions | `lc_data_source`, `lc_expression`, `lc_expression_binding` |
| Events / localization | `lc_event_handler`, `lc_localization_entry` |
| Pages | `lc_page_definition`, `lc_page_version`, `lc_page_region` |
| Publish / runtime | `lc_publish_history`, `lc_runtime_submission`, `lc_preview_session` |
| UI | Form Studio · Page Studio · Component Catalog |
| Runtime | Published-only render · submit handoff to owning modules |

**Phase 2A+ table count remaining:** 15 of 18 ERD-26 business tables.

---

**Sprint 26 Phase 1 — Complete.**  
**Documentation status:** Architect editorial review applied — ready for Phase 2A.
