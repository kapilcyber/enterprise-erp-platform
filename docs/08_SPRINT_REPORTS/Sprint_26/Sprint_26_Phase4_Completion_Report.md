# Sprint 26 Phase 4 Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.21-beta (planned) |
| **Sprint** | Sprint 26 — Low-Code Platform |
| **Phase** | Phase 4 — Publish History · Runtime Submission · Preview Session |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-26 Locked v1.1 · ERD-26 Entity Planning Locked v1.1 · ERD-26 Locked v1.1 — Preserved |
| **Prior Phases** | Phase 1 · Phase 2A · Phase 2B · Phase 2C · Phase 3A · Phase 3B — Complete |
| **Schema / Prefix** | `lowcode` / `lc_` |
| **New Tables** | 3 (`lc_publish_history` · `lc_runtime_submission` · `lc_preview_session`) |
| **Total Low-Code Tables** | **18 of 18** |
| **API Mount** | `/api/v1/lowcode` |
| **Alembic Head** | `0519_seed_lowcode_phase4_permissions` |
| **Low-Code Tests** | **90 passed** |
| **Routes** | **110** |
| **Sprint Backend** | **100% Complete** |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `lc_publish_history` | Append-oriented publish / retire trail · actor · timestamp · reason · version transition UUIDs |
| 2 | `lc_runtime_submission` | Correlation envelope only · published form/page UUID · module_code · entity_id · optional bpm_task_id · status · validation/metadata JSON |
| 3 | `lc_preview_session` | Design-time draft/published preview · sample context · TTL/expiration · designer ownership · close/expire |

### Publish History Rules

- Stores only: publish · retire · version transition · actor · timestamp · reason
- Append-oriented (no update API)
- Complements Foundation Audit — does **not** replace it
- Recorded automatically on form/page version publish and retire

### Runtime Submission Rules

- Correlation metadata only — **no** business SoR · **no** peer ORM · **no** transaction storage
- Requires Published form and/or page version
- Unique `(company_id, correlation_id)`
- Status: received · validated · failed · handoff · cancelled

### Preview Session Rules

- Design-time only: draft preview · published preview
- Mode must match version status
- Supports sample context · expiration · designer ownership
- Never mutates business data · never starts workflow · never creates business runtime records

### Explicitly Not Done

- Rendering engine
- Workflow runtime / notification delivery
- Integration execution
- Business logic / business persistence
- Document storage
- Analytics
- Frontend / UI
- Publish Validation Integration into form publish (future)
- Form Version deep-clone of sections/fields (future)

---

## Files Created

### Models / Repositories

| File |
|------|
| `apps/api/src/modules/lowcode/models/publish_history.py` |
| `apps/api/src/modules/lowcode/models/runtime_submission.py` |
| `apps/api/src/modules/lowcode/models/preview_session.py` |
| `apps/api/src/modules/lowcode/repository/publish_history_repository.py` |
| `apps/api/src/modules/lowcode/repository/runtime_submission_repository.py` |
| `apps/api/src/modules/lowcode/repository/preview_session_repository.py` |

### Services / Engines

| File |
|------|
| `apps/api/src/modules/lowcode/service/publish_history_service.py` |
| `apps/api/src/modules/lowcode/service/runtime_submission_service.py` |
| `apps/api/src/modules/lowcode/service/preview_session_service.py` |
| `apps/api/src/modules/lowcode/service/engines/publish_history_engine.py` |
| `apps/api/src/modules/lowcode/service/engines/runtime_submission_engine.py` |
| `apps/api/src/modules/lowcode/service/engines/preview_session_engine.py` |

### Migrations

| Revision | File |
|----------|------|
| `0516_lc_publish_history` | `apps/api/alembic/versions/0516_lc_publish_history.py` |
| `0517_lc_runtime_submission` | `apps/api/alembic/versions/0517_lc_runtime_submission.py` |
| `0518_lc_preview_session` | `apps/api/alembic/versions/0518_lc_preview_session.py` |
| `0519_seed_lowcode_phase4_permissions` | `apps/api/alembic/versions/0519_seed_lowcode_phase4_permissions.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/lowcode/test_lowcode_phase4_runtime.py` |
| `apps/api/src/tests/security/lowcode/test_lowcode_phase4_permissions.py` |
| `apps/api/src/tests/integration/lowcode/test_lowcode_phase4_module_import.py` |

### Reports

| File |
|------|
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase4_Completion_Report.md` |
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `docs/08_SPRINT_REPORTS/Sprint_26/Sprint_26_Phase3B_Completion_Report.md` | Runtime Ownership Boundary (doc-only pre-step) |
| `apps/api/src/modules/lowcode/domain/enums.py` | Phase 4 entity types · actions · statuses · code prefixes |
| `apps/api/src/modules/lowcode/domain/exceptions.py` | Phase 4 state exceptions |
| `apps/api/src/modules/lowcode/domain/entities.py` | Phase 4 identities |
| `apps/api/src/modules/lowcode/models/__init__.py` | Export Phase 4 models (18 total) |
| `apps/api/src/modules/lowcode/service/engines/__init__.py` | Export Phase 4 engines |
| `apps/api/src/modules/lowcode/service/application_service.py` | Wire publish history · runtime submissions · preview sessions |
| `apps/api/src/modules/lowcode/service/__init__.py` | Export Phase 4 services |
| `apps/api/src/modules/lowcode/service/form_version_service.py` | Record publish history on publish/retire |
| `apps/api/src/modules/lowcode/service/page_version_service.py` | Record publish history on publish/retire |
| `apps/api/src/modules/lowcode/service/preview_session_service.py` | Idempotent expire after lazy TTL |
| `apps/api/src/modules/lowcode/schemas.py` | Phase 4 request/response schemas |
| `apps/api/src/modules/lowcode/permissions.py` | Phase 4 permissions · publisher/auditor reads |
| `apps/api/src/modules/lowcode/routers/__init__.py` | Phase 4 routes |
| `apps/api/src/modules/lowcode/router.py` | Include Phase 4 routers |
| Integration import tests (hub · 2A · 2B · 2C · 3A · 3B) | Model count → 18 |

---

## Repositories

| Repository |
|------------|
| `PublishHistoryRepository` |
| `RuntimeSubmissionRepository` |
| `PreviewSessionRepository` |

---

## Services

| Service | Role |
|---------|------|
| `PublishHistoryService` | Append-only trail · form/page publish & retire helpers |
| `RuntimeSubmissionService` | Create correlation · get by correlation · update status |
| `PreviewSessionService` | Create draft/published preview · close · expire · lazy TTL |
| `PublishHistoryEngine` / `RuntimeSubmissionEngine` / `PreviewSessionEngine` | Action · correlation · mode/lifecycle validation |

---

## Permissions

| Permission |
|------------|
| `lowcode.publish_history:read` |
| `lowcode.runtime_submission:read` · `create` · `update` |
| `lowcode.preview_session:read` · `create` · `close` · `expire` |

---

## APIs / Routes

**Mount:** `/api/v1/lowcode`

### Publish History — `/api/v1/lowcode/publish-history`

| Method | Path | Permission |
|--------|------|------------|
| GET | `/by-form/{form_definition_id}` | `lowcode.publish_history:read` |
| GET | `/by-page/{page_definition_id}` | `lowcode.publish_history:read` |
| GET | `/{row_id}` | `lowcode.publish_history:read` |

### Runtime Submissions — `/api/v1/lowcode/runtime-submissions`

| Method | Path | Permission |
|--------|------|------------|
| GET | ``?module_code=&entity_id=`` | `lowcode.runtime_submission:read` |
| GET | `/by-correlation/{correlation_id}` | `lowcode.runtime_submission:read` |
| GET | `/{row_id}` | `lowcode.runtime_submission:read` |
| POST | `` | `lowcode.runtime_submission:create` |
| PATCH | `/{row_id}/status` | `lowcode.runtime_submission:update` |

### Preview Sessions — `/api/v1/lowcode/preview-sessions`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `lowcode.preview_session:read` |
| GET | `/{row_id}` | `lowcode.preview_session:read` |
| POST | `` | `lowcode.preview_session:create` |
| POST | `/{row_id}/close` | `lowcode.preview_session:close` |
| POST | `/{row_id}/expire` | `lowcode.preview_session:expire` |

---

## Tests

| Suite | Result |
|-------|--------|
| Unit Phase 4 engines | PASS |
| Security Phase 4 permissions | PASS |
| Integration Phase 4 import | PASS |
| Prior Phase 1 · 2A · 2B · 2C · 3A · 3B suites | PASS |
| **Total** | **90 passed** |

---

## Validation

| Gate | Result |
|------|--------|
| Exactly 3 new tables (`lc_publish_history` · `lc_runtime_submission` · `lc_preview_session`) | Pass |
| Total **18 of 18** ERD tables | Pass |
| Publish history append-only · complements Foundation Audit | Pass |
| Runtime submission correlation only · published versions · no business SoR | Pass |
| Preview design-time only · no business mutation · no workflow start | Pass |
| Architecture Lock v1.1 · FRD-26 · ERD-26 preserved | Pass |
| **90 tests passed** | Pass |
| Low-Code Backend 100% complete | Pass |

---

## Remaining Work

### Runtime Ownership Boundary (confirmed)

Publish History, Runtime Submission and Preview Session are operational metadata only.

They do NOT become:

- Business System of Record
- Workflow Engine
- Audit System
- Document Storage
- Notification Engine

Business modules remain System of Record.  
Foundation Audit remains enterprise audit.  
Foundation Workflow remains workflow engine.  
Document Management owns files.

### Deferred (outside Phase 4 / ERD table scope)

| Area | Notes |
|------|-------|
| Rendering engine | Future Low-Code Runtime / UI |
| Workflow / Notification / Integration execution | Foundation / Integration Hub ownership |
| Publish Validation Integration | Wire structure validation into form publish |
| Form Version Clone Enhancement | Deep-copy sections/fields with new UUIDs |
| Frontend / Designer UI | Deferred |

**Remaining ERD table count:** 0 of 18.

---

**Sprint 26 Phase 4 — Complete.**  
**Low-Code Backend — 100% Complete (18/18).**  
**Architecture Lock preserved.**
