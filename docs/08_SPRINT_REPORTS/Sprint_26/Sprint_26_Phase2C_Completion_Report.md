# Sprint 26 Phase 2C Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.21-beta (planned) |
| **Sprint** | Sprint 26 — Low-Code Platform |
| **Phase** | Phase 2C — Data & Expression Layer |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-26 Locked v1.1 · ERD-26 Entity Planning Locked v1.1 · ERD-26 Locked v1.1 — Preserved |
| **Prior Phases** | Phase 1 · Phase 2A · Phase 2B — Complete |
| **Schema / Prefix** | `lowcode` / `lc_` |
| **New Tables** | 3 (`lc_data_source` · `lc_expression` · `lc_expression_binding`) |
| **Supporting schema** | Optional `lc_form_field.data_source_id` FK (not a new entity) |
| **Total Low-Code Tables** | 10 of 18 |
| **API Mount** | `/api/v1/lowcode` |
| **Alembic Head** | `0508_seed_lowcode_phase2c_permissions` |
| **Low-Code Tests** | 57 passed |
| **Routes** | 67 |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `lc_data_source` | Module contract registry · ops/attribute metadata · activate/retire · archive/restore |
| 2 | `lc_expression` | UI expression CRUD · kinds · Draft / Publish / Retire · published immutable |
| 3 | `lc_expression_binding` | Bind expression → form version / section / field / page_version (UUID future) · multi-bind · draft-version gate |

### Expression Kinds (UI only)

visibility · required · enable · disable · default · calculate

### Data Source Operations (registry metadata)

read · write · lookup

### Validation Rules Enforced

- Data Sources are **registry only** — no business rows · no peer ORM · no runtime lookup execution
- Expressions are **UI logic only** — not BPM Decision Tables · not Business Rules · not workflow routing
- Expression Bindings are version-scoped design metadata; multiple bindings allowed
- Form-scoped binding mutations require Draft Form Version
- `page_version` bindings store UUID metadata only (page tables deferred)
- Draft editable · Published immutable · Retired read-only (expressions)
- Soft delete · UUID PKs · company scoped · audit columns
- Form Fields may optionally reference `data_source_id` (same Low-Code schema only)

### Explicitly Not Done

- Event Handlers · Localization · Pages · Publish History
- Runtime Submission · Preview · Rendering Engine
- Expression / lookup **execution** · Workflow · Notifications · Business Logic
- Publish Validation Integration (structure → form publish) — deferred
- Version Clone Enhancement (deep-copy sections/fields) — deferred
- UI

---

## Files Created

### Models / Repositories

| File |
|------|
| `apps/api/src/modules/lowcode/models/data_source.py` |
| `apps/api/src/modules/lowcode/models/expression.py` |
| `apps/api/src/modules/lowcode/models/expression_binding.py` |
| `apps/api/src/modules/lowcode/repository/data_source_repository.py` |
| `apps/api/src/modules/lowcode/repository/expression_repository.py` |
| `apps/api/src/modules/lowcode/repository/expression_binding_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/lowcode/service/data_source_service.py` |
| `apps/api/src/modules/lowcode/service/expression_service.py` |
| `apps/api/src/modules/lowcode/service/expression_binding_service.py` |
| `apps/api/src/modules/lowcode/service/engines/data_source_engine.py` |
| `apps/api/src/modules/lowcode/service/engines/expression_engine.py` |
| `apps/api/src/modules/lowcode/service/engines/expression_binding_engine.py` |

### Migrations

| Revision | File |
|----------|------|
| `0504_lc_data_source` | `apps/api/alembic/versions/0504_lc_data_source.py` |
| `0505_lc_expression` | `apps/api/alembic/versions/0505_lc_expression.py` |
| `0506_lc_expression_binding` | `apps/api/alembic/versions/0506_lc_expression_binding.py` |
| `0507_lc_form_field_data_source_ref` | `apps/api/alembic/versions/0507_lc_form_field_data_source_ref.py` |
| `0508_seed_lowcode_phase2c_permissions` | `apps/api/alembic/versions/0508_seed_lowcode_phase2c_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/lowcode/test_lowcode_phase2c_data_expression.py` |
| `apps/api/src/tests/security/lowcode/test_lowcode_phase2c_permissions.py` |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2c_module_import.py` |

### Report

| File |
|------|
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase2C_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/lowcode/domain/enums.py` | Data source / expression / binding enums · code prefixes |
| `apps/api/src/modules/lowcode/domain/exceptions.py` | Phase 2C exceptions |
| `apps/api/src/modules/lowcode/domain/entities.py` | Phase 2C identities |
| `apps/api/src/modules/lowcode/models/__init__.py` | Export Phase 2C models (10 total) |
| `apps/api/src/modules/lowcode/models/form_field.py` | Optional `data_source_id` |
| `apps/api/src/modules/lowcode/service/form_field_service.py` | Validate data source ref |
| `apps/api/src/modules/lowcode/service/engines/__init__.py` | Export Phase 2C engines |
| `apps/api/src/modules/lowcode/service/application_service.py` | Wire data sources / expressions / bindings |
| `apps/api/src/modules/lowcode/service/__init__.py` | Export Phase 2C services |
| `apps/api/src/modules/lowcode/schemas.py` | Data source / expression / binding schemas · field FK |
| `apps/api/src/modules/lowcode/permissions.py` | Phase 2C permissions |
| `apps/api/src/modules/lowcode/routers/__init__.py` | Phase 2C routes |
| `apps/api/src/modules/lowcode/router.py` | Include Phase 2C routers |
| `apps/api/src/tests/integration/lowcode/test_lowcode_hub_module_import.py` | Model count → 10 |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2a_module_import.py` | Model count → 10 |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2b_module_import.py` | Model count → 10 |
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase2B_Completion_Report.md` | Component Runtime Boundary (doc-only, pre-2C) |

---

## Repositories

| Repository |
|------------|
| `DataSourceRepository` |
| `ExpressionRepository` |
| `ExpressionBindingRepository` |

---

## Services

| Service | Role |
|---------|------|
| `DataSourceService` | Registry CRUD · activate/retire · archive/restore |
| `ExpressionService` | UI expression CRUD · publish / retire · archive/restore |
| `ExpressionBindingService` | Version-scoped bindings · draft form gate · soft delete |
| `DataSourceEngine` / `ExpressionEngine` / `ExpressionBindingEngine` | Contract · kind · target rules |

---

## Permissions

| Permission |
|------------|
| `lowcode.data_source:read` · `create` · `update` · `archive` · `restore` · `activate` · `retire` |
| `lowcode.expression:read` · `create` · `update` · `archive` · `restore` · `publish` · `retire` |
| `lowcode.expression_binding:read` · `create` · `update` · `delete` |

---

## APIs / Routes

**Mount:** `/api/v1/lowcode`

### Data Sources — `/api/v1/lowcode/data-sources`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `lowcode.data_source:read` |
| GET | `/{row_id}` | `lowcode.data_source:read` |
| POST | `` | `lowcode.data_source:create` |
| PATCH | `/{row_id}` | `lowcode.data_source:update` |
| POST | `/{row_id}/archive` | `lowcode.data_source:archive` |
| POST | `/{row_id}/restore` | `lowcode.data_source:restore` |
| POST | `/{row_id}/activate` | `lowcode.data_source:activate` |
| POST | `/{row_id}/retire` | `lowcode.data_source:retire` |

### Expressions — `/api/v1/lowcode/expressions`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `lowcode.expression:read` |
| GET | `/{row_id}` | `lowcode.expression:read` |
| POST | `` | `lowcode.expression:create` |
| PATCH | `/{row_id}` | `lowcode.expression:update` |
| POST | `/{row_id}/archive` | `lowcode.expression:archive` |
| POST | `/{row_id}/restore` | `lowcode.expression:restore` |
| POST | `/{row_id}/publish` | `lowcode.expression:publish` |
| POST | `/{row_id}/retire` | `lowcode.expression:retire` |
| GET | `/{row_id}/bindings` | `lowcode.expression_binding:read` |

### Expression Bindings — `/api/v1/lowcode/expression-bindings`

| Method | Path | Permission |
|--------|------|------------|
| GET | ``?form_version_id=`` | `lowcode.expression_binding:read` |
| GET | `/{row_id}` | `lowcode.expression_binding:read` |
| POST | `` | `lowcode.expression_binding:create` |
| PATCH | `/{row_id}` | `lowcode.expression_binding:update` |
| DELETE | `/{row_id}` | `lowcode.expression_binding:delete` |

---

## Tests

| Suite | Result |
|-------|--------|
| Unit data source / expression / binding engines | PASS |
| Security Phase 2C permissions | PASS |
| Integration Phase 2C import | PASS |
| Prior Phase 1 · 2A · 2B suites | PASS |
| **Total** | **57 passed** |

---

## Validation

| Gate | Result |
|------|--------|
| Exactly 3 new tables (`lc_data_source` · `lc_expression` · `lc_expression_binding`) | Pass |
| Total 10 of 18 ERD tables | Pass |
| Data source = registry only · no peer ORM · no business ownership | Pass |
| Expressions = UI only · not BPM rules / decision tables / workflow | Pass |
| Bindings version-scoped · multi-bind · draft form gate | Pass |
| Field → Data Source optional FK (Low-Code only) | Pass |
| No runtime / rendering / events / pages / localization | Pass |
| Architecture Lock v1.1 · FRD-26 · ERD-26 preserved | Pass |
| **57 tests passed** | Pass |

---

## Remaining Work for Phase 2D+

### Expression Runtime Boundary

Expressions and bindings define **design-time UI metadata only**.

They do NOT own:

- runtime evaluation / execution
- business rule replacement
- decision table replacement
- workflow routing
- lookup data materialization

These responsibilities belong to later Low-Code runtime services and the owning business modules / BPM.

| Area | Remaining ERD Tables / Capabilities |
|------|-------------------------------------|
| Events / localization | `lc_event_handler`, `lc_localization_entry` |
| Pages | `lc_page_definition`, `lc_page_version`, `lc_page_region` |
| Publish / runtime | `lc_publish_history`, `lc_runtime_submission`, `lc_preview_session` |
| Publish Validation Integration | Integrate structure validation into form publish (future) |
| Version Clone Enhancement | Deep-copy sections/fields with new UUIDs (future) |

**Remaining table count:** 8 of 18 ERD-26 business tables.

---

**Sprint 26 Phase 2C — Complete.**  
**Architecture Lock preserved.**
