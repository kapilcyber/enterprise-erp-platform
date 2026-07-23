# Sprint 26 Phase 2A Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.21-beta (planned) |
| **Sprint** | Sprint 26 — Low-Code Platform |
| **Phase** | Phase 2A — Form Structure |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-26 Locked v1.1 · ERD-26 Entity Planning Locked v1.1 · ERD-26 Locked v1.1 — Preserved |
| **Prior Phases** | Phase 1 — Complete |
| **Schema / Prefix** | `lowcode` / `lc_` |
| **New Tables** | 2 (`lc_form_section` · `lc_form_field`) |
| **Total Low-Code Tables** | 5 of 18 |
| **API Mount** | `/api/v1/lowcode` |
| **Alembic Head** | `0499_seed_lowcode_phase2a_permissions` |
| **Low-Code Tests** | 31 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `lc_form_section` | Section CRUD · display order · Draft-version gate |
| 2 | `lc_form_field` | Field CRUD · unique `field_key` per version · optional section · validation/binding JSON merged · structure validate |

### Field Types

text · textarea · rich_text · number · integer · decimal · date · time · datetime · boolean · select · multi_select · lookup · email · phone · url · attachment · display · hidden

### Validation Rules Enforced

- Sections belong to one Form Version
- Fields belong to one Form Version
- Fields may optionally belong to a Section (same version only)
- Only Draft Form Versions are editable (Published immutable · Retired read-only)
- `display_order >= 0` (section and field)
- Unique `field_key` within one Form Version
- `field_key` lowercase snake_case
- Soft delete only · UUID PKs · company scoped · audit columns
- No peer ORM · no component/data-source FKs (later phases) · no business data ownership

### Explicitly Not Done

- Pages · Components · Data Sources · Expressions · Expression Bindings
- Events · Localization · Runtime · Preview · Submission · Publish History
- UI · Rendering · Workflow · Notification · Documents
- Clone does not yet deep-copy structure (deferred)

---

## Files Created

### Models / Repositories

| File |
|------|
| `apps/api/src/modules/lowcode/models/form_section.py` |
| `apps/api/src/modules/lowcode/models/form_field.py` |
| `apps/api/src/modules/lowcode/repository/form_section_repository.py` |
| `apps/api/src/modules/lowcode/repository/form_field_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/lowcode/service/form_section_service.py` |
| `apps/api/src/modules/lowcode/service/form_field_service.py` |
| `apps/api/src/modules/lowcode/service/form_structure_validation_service.py` |
| `apps/api/src/modules/lowcode/service/engines/form_section_engine.py` |
| `apps/api/src/modules/lowcode/service/engines/form_field_engine.py` |

### Migrations

| Revision | File |
|----------|------|
| `0497_lc_form_section` | `apps/api/alembic/versions/0497_lc_form_section.py` |
| `0498_lc_form_field` | `apps/api/alembic/versions/0498_lc_form_field.py` |
| `0499_seed_lowcode_phase2a_permissions` | `apps/api/alembic/versions/0499_seed_lowcode_phase2a_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/lowcode/test_lowcode_phase2a_structure.py` |
| `apps/api/src/tests/security/lowcode/test_lowcode_phase2a_permissions.py` |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2a_module_import.py` |

### Report

| File |
|------|
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase2A_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/lowcode/domain/enums.py` | Section/field enums · field types · code prefixes |
| `apps/api/src/modules/lowcode/domain/exceptions.py` | Section/field/structure exceptions |
| `apps/api/src/modules/lowcode/domain/entities.py` | Section/field identities |
| `apps/api/src/modules/lowcode/domain/value_objects.py` | `StructureValidationResult` |
| `apps/api/src/modules/lowcode/models/__init__.py` | Export Phase 2A models (5 total) |
| `apps/api/src/modules/lowcode/service/engines/__init__.py` | Export section/field engines |
| `apps/api/src/modules/lowcode/service/application_service.py` | Wire sections · fields · structure validation |
| `apps/api/src/modules/lowcode/service/__init__.py` | Export Phase 2A services |
| `apps/api/src/modules/lowcode/schemas.py` | Section / field schemas |
| `apps/api/src/modules/lowcode/permissions.py` | Section / field / structure permissions |
| `apps/api/src/modules/lowcode/routers/__init__.py` | Sections · fields · structure routes |
| `apps/api/src/modules/lowcode/router.py` | Include Phase 2A routers |
| `apps/api/src/tests/integration/lowcode/test_lowcode_hub_module_import.py` | Model count → 5 |

---

## Repositories

| Repository |
|------------|
| `FormSectionRepository` |
| `FormFieldRepository` |

---

## Services

| Service | Role |
|---------|------|
| `FormSectionService` | Section CRUD · Draft-version gate |
| `FormFieldService` | Field CRUD · unique key · section affinity |
| `FormStructureValidationService` | Structure integrity validate |
| `FormSectionEngine` / `FormFieldEngine` | Display order · type · key rules |

---

## Permissions

| Permission |
|------------|
| `lowcode.section:read` · `create` · `update` · `delete` |
| `lowcode.field:read` · `create` · `update` · `delete` |
| `lowcode.structure:validate` |

Roles `LOWCODE_ADMIN` · `FORM_DESIGNER` · `FORM_PUBLISHER` · `LOWCODE_AUDITOR` re-granted Phase 2A slices.

---

## APIs / Routes

**Mount:** `/api/v1/lowcode`  
**Phase 2A routes added:** 11 · **Total lowcode routes:** 32

### Sections — `/api/v1/lowcode/sections`

| Method | Path | Permission |
|--------|------|------------|
| GET | ``?form_version_id=` | `lowcode.section:read` |
| GET | `/{row_id}` | `lowcode.section:read` |
| POST | `` | `lowcode.section:create` |
| PATCH | `/{row_id}` | `lowcode.section:update` |
| DELETE | `/{row_id}` | `lowcode.section:delete` (soft) |

### Fields — `/api/v1/lowcode/fields`

| Method | Path | Permission |
|--------|------|------------|
| GET | ``?form_version_id=` or `?section_id=` | `lowcode.field:read` |
| GET | `/{row_id}` | `lowcode.field:read` |
| POST | `` | `lowcode.field:create` |
| PATCH | `/{row_id}` | `lowcode.field:update` |
| DELETE | `/{row_id}` | `lowcode.field:delete` (soft) |

### Structure — `/api/v1/lowcode/structure`

| Method | Path | Permission |
|--------|------|------------|
| POST | `/validate?form_version_id=` | `lowcode.structure:validate` |

---

## Tests

| Suite | Result |
|-------|--------|
| Unit structure engines | PASS |
| Security Phase 2A permissions | PASS |
| Integration Phase 2A import | PASS |
| Prior Phase 1 suites | PASS |
| **Total** | **31 passed** |

---

## Validation

| Gate | Result |
|------|--------|
| Exactly 2 new tables (`lc_form_section` · `lc_form_field`) | Pass |
| Total 5 of 18 ERD tables | Pass |
| Draft-only edits · published immutability | Pass |
| Unique field_key · display_order · soft delete · company scope | Pass |
| No peer ORM · no business SoR · no later-phase tables | Pass |
| Architecture Lock v1.1 · FRD-26 · ERD-26 preserved | Pass |
| Ruff clean · 31 tests passed | Pass |

---

## Remaining Work for Phase 2B+

| Area | Remaining ERD Tables / Capabilities |
|------|-------------------------------------|
| Components | `lc_component`, `lc_component_version` |
| Data / expressions | `lc_data_source`, `lc_expression`, `lc_expression_binding` |
| Events / localization | `lc_event_handler`, `lc_localization_entry` |
| Pages | `lc_page_definition`, `lc_page_version`, `lc_page_region` |
| Publish / runtime | `lc_publish_history`, `lc_runtime_submission`, `lc_preview_session` |
| Version Clone Enhancement | Deep-copy Sections and Fields while generating new UUIDs, preserving display order and parent-child relationships. This enhancement belongs to a future phase. No implementation in this document. |
| Publish Validation Integration | Integrate `FormStructureValidationService` into `PublishValidationService` before allowing a Form Version to be Published. A Form Version must successfully pass structure validation before Publish. This is a planned Phase 2B enhancement only. No implementation in this document. |

**Remaining table count:** 13 of 18 ERD-26 business tables.

---

**Sprint 26 Phase 2A — Complete.**  
**Architecture Lock preserved.**
