# Sprint 26 Phase 2B Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.21-beta (planned) |
| **Sprint** | Sprint 26 — Low-Code Platform |
| **Phase** | Phase 2B — Component Catalog |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-26 Locked v1.1 · ERD-26 Entity Planning Locked v1.1 · ERD-26 Locked v1.1 — Preserved |
| **Prior Phases** | Phase 1 · Phase 2A — Complete |
| **Schema / Prefix** | `lowcode` / `lc_` |
| **New Tables** | 2 (`lc_component` · `lc_component_version`) |
| **Supporting schema** | Optional `lc_form_field.component_version_id` FK (not a new entity) |
| **Total Low-Code Tables** | 7 of 18 |
| **API Mount** | `/api/v1/lowcode` |
| **Alembic Head** | `0503_seed_lowcode_phase2b_permissions` |
| **Low-Code Tests** | 44 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `lc_component` | Catalog identity CRUD · kind governance · archive/restore · seed Draft v1 |
| 2 | `lc_component_version` | Draft · Publish · Retire · Clone · properties_json merged · one Published per Component |

### Component Kinds

text · textarea · rich_text · number · date · datetime · boolean · select · multi_select · lookup · grid · section · divider · attachment · display · custom

### Validation Rules Enforced

- Component is stable identity; Component Version is the design unit
- Exactly ONE Published Component Version per Component (prior Published auto-retired)
- Draft editable · Published immutable · Retired read-only
- Form Fields may optionally reference `component_version_id` (same Low-Code schema only)
- Soft delete · UUID PKs · company scoped · audit columns
- No peer ORM · no business data ownership
- FRD-26 Component Compatibility Policy: published forms pin the component version used at design/publish time

### Explicitly Not Done

- Data Sources · Expressions · Expression Bindings · Events · Localization
- Pages · Runtime · Preview · Submission · Publish History
- Publish Validation Integration (structure → form publish) — deferred
- Version Clone Enhancement (deep-copy sections/fields) — deferred
- UI · Rendering · Workflow · Notifications · Documents

---

## Files Created

### Models / Repositories

| File |
|------|
| `apps/api/src/modules/lowcode/models/component.py` |
| `apps/api/src/modules/lowcode/models/component_version.py` |
| `apps/api/src/modules/lowcode/repository/component_repository.py` |
| `apps/api/src/modules/lowcode/repository/component_version_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/lowcode/service/component_service.py` |
| `apps/api/src/modules/lowcode/service/component_version_service.py` |
| `apps/api/src/modules/lowcode/service/engines/component_engine.py` |
| `apps/api/src/modules/lowcode/service/engines/component_version_engine.py` |

### Migrations

| Revision | File |
|----------|------|
| `0500_lc_component` | `apps/api/alembic/versions/0500_lc_component.py` |
| `0501_lc_component_version` | `apps/api/alembic/versions/0501_lc_component_version.py` |
| `0502_lc_form_field_component_version_ref` | `apps/api/alembic/versions/0502_lc_form_field_component_version_ref.py` |
| `0503_seed_lowcode_phase2b_permissions` | `apps/api/alembic/versions/0503_seed_lowcode_phase2b_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/lowcode/test_lowcode_phase2b_components.py` |
| `apps/api/src/tests/security/lowcode/test_lowcode_phase2b_permissions.py` |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2b_module_import.py` |

### Report

| File |
|------|
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase2B_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/lowcode/domain/enums.py` | Component kinds/status · code prefixes |
| `apps/api/src/modules/lowcode/domain/exceptions.py` | Component version exceptions |
| `apps/api/src/modules/lowcode/domain/entities.py` | Component identities |
| `apps/api/src/modules/lowcode/models/__init__.py` | Export Phase 2B models (7 total) |
| `apps/api/src/modules/lowcode/models/form_field.py` | Optional `component_version_id` |
| `apps/api/src/modules/lowcode/repository/form_field_repository.py` | Clearable component_version_id |
| `apps/api/src/modules/lowcode/service/form_field_service.py` | Validate component version ref |
| `apps/api/src/modules/lowcode/service/engines/__init__.py` | Export component engines |
| `apps/api/src/modules/lowcode/service/application_service.py` | Wire components |
| `apps/api/src/modules/lowcode/service/__init__.py` | Export Phase 2B services |
| `apps/api/src/modules/lowcode/schemas.py` | Component / version schemas · field FK |
| `apps/api/src/modules/lowcode/permissions.py` | Component permissions |
| `apps/api/src/modules/lowcode/routers/__init__.py` | Component routes |
| `apps/api/src/modules/lowcode/router.py` | Include Phase 2B routers |
| `apps/api/src/tests/integration/lowcode/test_lowcode_hub_module_import.py` | Model count → 7 |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2a_module_import.py` | Model count → 7 |
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase2A_Completion_Report.md` | Editorial remaining-work wording |

---

## Repositories

| Repository |
|------------|
| `ComponentRepository` |
| `ComponentVersionRepository` |

---

## Services

| Service | Role |
|---------|------|
| `ComponentService` | Catalog CRUD · activate/retire · seed Draft v1 |
| `ComponentVersionService` | Draft / publish / retire / clone · properties_json |
| `ComponentEngine` / `ComponentVersionEngine` | Kind + immutability rules |

---

## Permissions

| Permission |
|------------|
| `lowcode.component:read` · `create` · `update` · `archive` · `restore` |
| `lowcode.component_version:read` · `create` · `update` · `publish` · `retire` · `clone` |

---

## APIs / Routes

**Mount:** `/api/v1/lowcode`

### Components — `/api/v1/lowcode/components`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `lowcode.component:read` |
| GET | `/{row_id}` | `lowcode.component:read` |
| POST | `` | `lowcode.component:create` |
| PATCH | `/{row_id}` | `lowcode.component:update` |
| POST | `/{row_id}/archive` | `lowcode.component:archive` |
| POST | `/{row_id}/restore` | `lowcode.component:restore` |
| GET | `/{row_id}/versions` | `lowcode.component_version:read` |

### Component Versions — `/api/v1/lowcode/component-versions`

| Method | Path | Permission |
|--------|------|------------|
| GET | `/{row_id}` | `lowcode.component_version:read` |
| POST | `` | `lowcode.component_version:create` |
| PATCH | `/{row_id}` | `lowcode.component_version:update` |
| POST | `/{row_id}/publish` | `lowcode.component_version:publish` |
| POST | `/{row_id}/retire` | `lowcode.component_version:retire` |
| POST | `/{row_id}/clone` | `lowcode.component_version:clone` |

---

## Tests

| Suite | Result |
|-------|--------|
| Unit component engines | PASS |
| Security Phase 2B permissions | PASS |
| Integration Phase 2B import | PASS |
| Prior Phase 1 · 2A suites | PASS |
| **Total** | **44 passed** |

---

## Validation

| Gate | Result |
|------|--------|
| Exactly 2 new tables (`lc_component` · `lc_component_version`) | Pass |
| Total 7 of 18 ERD tables | Pass |
| One Published per Component · published immutability | Pass |
| Field → Component Version optional FK (Low-Code only) | Pass |
| No peer ORM · no later-phase entities (data sources/pages/runtime) | Pass |
| Architecture Lock v1.1 · FRD-26 · ERD-26 preserved | Pass |
| **44 tests passed** | Pass |

---

## Remaining Work for Phase 2C+

### Component Runtime Boundary

Component Versions define rendering metadata only.

They do NOT own:

- runtime field values
- business data
- lookup data
- expression execution
- event execution

These responsibilities belong to later Low-Code runtime services and the owning business modules.

This is documentation only. No implementation. No FRD / ERD / architecture changes.

| Area | Remaining ERD Tables / Capabilities |
|------|-------------------------------------|
| Data / expressions | `lc_data_source`, `lc_expression`, `lc_expression_binding` |
| Events / localization | `lc_event_handler`, `lc_localization_entry` |
| Pages | `lc_page_definition`, `lc_page_version`, `lc_page_region` |
| Publish / runtime | `lc_publish_history`, `lc_runtime_submission`, `lc_preview_session` |
| Publish Validation Integration | Integrate structure validation into form publish (future) |
| Version Clone Enhancement | Deep-copy sections/fields with new UUIDs (future) |

**Remaining table count:** 11 of 18 ERD-26 business tables.

---

**Sprint 26 Phase 2B — Complete.**  
**Architecture Lock preserved.**
