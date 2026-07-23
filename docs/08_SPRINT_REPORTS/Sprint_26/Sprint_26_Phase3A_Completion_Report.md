# Sprint 26 Phase 3A Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.21-beta (planned) |
| **Sprint** | Sprint 26 — Low-Code Platform |
| **Phase** | Phase 3A — Events & Localization |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-26 Locked v1.1 · ERD-26 Entity Planning Locked v1.1 · ERD-26 Locked v1.1 — Preserved |
| **Prior Phases** | Phase 1 · Phase 2A · Phase 2B · Phase 2C — Complete |
| **Schema / Prefix** | `lowcode` / `lc_` |
| **New Tables** | 2 (`lc_event_handler` · `lc_localization_entry`) |
| **Total Low-Code Tables** | 12 of 18 |
| **API Mount** | `/api/v1/lowcode` |
| **Alembic Head** | `0511_seed_lowcode_phase3a_permissions` |
| **Low-Code Tests** | 68 passed |
| **Routes** | 79 |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `lc_event_handler` | Event metadata CRUD · trigger catalog · target (form/section/field/page future) · execution_order · enabled · metadata_json · draft form gate |
| 2 | `lc_localization_entry` | Locale entries for form / field / section / component / page (future) · unique locale+key per owner · Draft / Publish / Retire |

### Event Types (metadata only)

onLoad · onChange · onFocus · onBlur · onValidate · onSubmit · onCancel · custom

### Localization Owner Types

form · field · section · component · page (future-ready UUID)

### Validation Rules Enforced

- Event handlers store **metadata only** — no execution · no workflow · no notifications · no integrations
- Localization stores locale / translation_key / translated_value only
- Unique `(owner_type, owner_ref_id, locale, translation_key)`
- Form-scoped mutations require Draft Form Version
- Localization: Draft editable · Published immutable · Retired read-only
- Soft delete · UUID PKs · company scoped · audit columns
- Page targets store UUID metadata only (page tables deferred)

### Explicitly Not Done

- Page Builder (`lc_page_definition` · `lc_page_version` · `lc_page_region`)
- Publish History · Runtime Submission · Preview Session
- Rendering Engine · Runtime evaluator / event execution
- Workflow · Notifications · Integrations · Business Rules · Decision Tables
- Publish Validation Integration · Version Clone Enhancement
- UI

---

## Files Created

### Models / Repositories

| File |
|------|
| `apps/api/src/modules/lowcode/models/event_handler.py` |
| `apps/api/src/modules/lowcode/models/localization_entry.py` |
| `apps/api/src/modules/lowcode/repository/event_handler_repository.py` |
| `apps/api/src/modules/lowcode/repository/localization_entry_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/lowcode/service/event_handler_service.py` |
| `apps/api/src/modules/lowcode/service/localization_entry_service.py` |
| `apps/api/src/modules/lowcode/service/engines/event_handler_engine.py` |
| `apps/api/src/modules/lowcode/service/engines/localization_entry_engine.py` |

### Migrations

| Revision | File |
|----------|------|
| `0509_lc_event_handler` | `apps/api/alembic/versions/0509_lc_event_handler.py` |
| `0510_lc_localization_entry` | `apps/api/alembic/versions/0510_lc_localization_entry.py` |
| `0511_seed_lowcode_phase3a_permissions` | `apps/api/alembic/versions/0511_seed_lowcode_phase3a_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/lowcode/test_lowcode_phase3a_events_localization.py` |
| `apps/api/src/tests/security/lowcode/test_lowcode_phase3a_permissions.py` |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase3a_module_import.py` |

### Report

| File |
|------|
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase3A_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/lowcode/domain/enums.py` | Event types · localization owners · code prefixes |
| `apps/api/src/modules/lowcode/domain/exceptions.py` | Phase 3A exceptions |
| `apps/api/src/modules/lowcode/domain/entities.py` | Phase 3A identities |
| `apps/api/src/modules/lowcode/models/__init__.py` | Export Phase 3A models (12 total) |
| `apps/api/src/modules/lowcode/service/engines/__init__.py` | Export Phase 3A engines |
| `apps/api/src/modules/lowcode/service/application_service.py` | Wire event handlers / localization |
| `apps/api/src/modules/lowcode/service/__init__.py` | Export Phase 3A services |
| `apps/api/src/modules/lowcode/schemas.py` | Event handler / localization schemas |
| `apps/api/src/modules/lowcode/permissions.py` | Phase 3A permissions |
| `apps/api/src/modules/lowcode/routers/__init__.py` | Phase 3A routes |
| `apps/api/src/modules/lowcode/router.py` | Include Phase 3A routers |
| `apps/api/src/tests/integration/lowcode/test_lowcode_hub_module_import.py` | Model count → 12 |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2a_module_import.py` | Model count → 12 |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2b_module_import.py` | Model count → 12 |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase2c_module_import.py` | Model count → 12 |

---

## Repositories

| Repository |
|------------|
| `EventHandlerRepository` |
| `LocalizationEntryRepository` |

---

## Services

| Service | Role |
|---------|------|
| `EventHandlerService` | Event metadata CRUD · draft form gate · soft delete |
| `LocalizationEntryService` | Localization CRUD · unique owner key · publish / retire |
| `EventHandlerEngine` / `LocalizationEntryEngine` | Trigger / owner / immutability rules |

---

## Permissions

| Permission |
|------------|
| `lowcode.event_handler:read` · `create` · `update` · `delete` |
| `lowcode.localization:read` · `create` · `update` · `delete` · `publish` · `retire` |

---

## APIs / Routes

**Mount:** `/api/v1/lowcode`

### Event Handlers — `/api/v1/lowcode/event-handlers`

| Method | Path | Permission |
|--------|------|------------|
| GET | ``?form_version_id=`` | `lowcode.event_handler:read` |
| GET | `/{row_id}` | `lowcode.event_handler:read` |
| POST | `` | `lowcode.event_handler:create` |
| PATCH | `/{row_id}` | `lowcode.event_handler:update` |
| DELETE | `/{row_id}` | `lowcode.event_handler:delete` |

### Localization Entries — `/api/v1/lowcode/localization-entries`

| Method | Path | Permission |
|--------|------|------------|
| GET | ``?form_version_id=`` or ``owner_type``+``owner_ref_id`` | `lowcode.localization:read` |
| GET | `/{row_id}` | `lowcode.localization:read` |
| POST | `` | `lowcode.localization:create` |
| PATCH | `/{row_id}` | `lowcode.localization:update` |
| DELETE | `/{row_id}` | `lowcode.localization:delete` |
| POST | `/{row_id}/publish` | `lowcode.localization:publish` |
| POST | `/{row_id}/retire` | `lowcode.localization:retire` |

---

## Tests

| Suite | Result |
|-------|--------|
| Unit event / localization engines | PASS |
| Security Phase 3A permissions | PASS |
| Integration Phase 3A import | PASS |
| Prior Phase 1 · 2A · 2B · 2C suites | PASS |
| **Total** | **68 passed** |

---

## Validation

| Gate | Result |
|------|--------|
| Exactly 2 new tables (`lc_event_handler` · `lc_localization_entry`) | Pass |
| Total 12 of 18 ERD tables | Pass |
| Event handlers = metadata only · no execution / workflow / notifications | Pass |
| Localization unique locale+key within owner · draft/publish/retire | Pass |
| No pages · publish history · runtime · preview · rendering | Pass |
| Architecture Lock v1.1 · FRD-26 · ERD-26 preserved | Pass |
| **68 tests passed** | Pass |

---

## Remaining Work for Phase 3B+

### Event Runtime Boundary

Event handlers and localization entries define **design-time metadata only**.

They do NOT own:

- event execution / evaluation
- notification delivery
- workflow routing
- integration transport
- page rendering

These responsibilities belong to later Low-Code runtime services, Foundation engines, and owning business modules.

### Page Runtime Boundary

Page definitions, versions and regions define layout metadata only.

They do NOT own:

- page rendering
- navigation engine
- workflow execution
- runtime component execution
- notification delivery
- business data

Rendering and runtime behavior belong to future Low-Code Runtime Services.

This is documentation only. No implementation. No FRD / ERD / architecture changes.

| Area | Remaining ERD Tables / Capabilities |
|------|-------------------------------------|
| Pages | `lc_page_definition`, `lc_page_version`, `lc_page_region` |
| Publish / runtime | `lc_publish_history`, `lc_runtime_submission`, `lc_preview_session` |
| Publish Validation Integration | Integrate structure validation into form publish (future) |
| Version Clone Enhancement | Deep-copy sections/fields with new UUIDs (future) |

**Remaining table count:** 6 of 18 ERD-26 business tables.

---

**Sprint 26 Phase 3A — Complete.**  
**Architecture Lock preserved.**
