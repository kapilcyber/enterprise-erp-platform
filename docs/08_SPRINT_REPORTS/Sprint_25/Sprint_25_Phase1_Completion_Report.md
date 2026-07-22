# Sprint 25 Phase 1 Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.20-beta (planned) |
| **Sprint** | Sprint 25 — Workflow & BPM Designer |
| **Phase** | Phase 1 — Design Spine |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD** | FRD-25 Locked |
| **ERD** | ERD-25 Locked |
| **Schema / Prefix** | `bpm` / `bpm_` |
| **API Mount** | `/api/v1/bpm` |
| **Alembic Head** | `0470_seed_bpm_permissions` |
| **Phase 1 Tables** | 4 of 20 |
| **BPM Tests** | 16 passed |

---

## Scope Delivered

| # | Table | Capability |
|---|--------|------------|
| 1 | `bpm_workflow_category` | Category CRUD |
| 2 | `bpm_workflow_template` | Template CRUD · Copy Template |
| 3 | `bpm_workflow_definition` | Definition CRUD · stable identity |
| 4 | `bpm_workflow_version` | Draft · Publish · Retire · Clone Version · Version Timeline |

### Workflow Rules Enforced

- Exactly ONE Published Version per Definition
- Draft versions editable
- Published versions immutable
- Retired versions read-only
- Templates reusable
- Definitions are stable identity

### Not Implemented (by design)

- Foundation Workflow Engine (`wf_*`) — untouched
- Phase 2–N ERD tables (nodes, runtime, simulation, etc.)
- Prior module redesigns
- Architecture Lock changes

---

## Files Created

### Backend — `apps/api/src/modules/bpm/`

| Area | Files |
|------|--------|
| Package | `__init__.py`, `router.py`, `schemas.py`, `permissions.py`, `dependencies.py`, `tasks.py` |
| Domain | `domain/__init__.py`, `domain/enums.py`, `domain/exceptions.py`, `domain/entities.py`, `domain/value_objects.py` |
| Models | `models/__init__.py`, `models/mixins.py`, `models/workflow_category.py`, `models/workflow_template.py`, `models/workflow_definition.py`, `models/workflow_version.py` |
| Repositories | `repository/base.py`, `repository/code_sequence_repository.py`, `repository/workflow_category_repository.py`, `repository/workflow_template_repository.py`, `repository/workflow_definition_repository.py`, `repository/workflow_version_repository.py` |
| Services | `service/__init__.py`, `service/application_service.py`, `service/bpm_integration_service.py`, `service/bpm_number_service.py`, `service/bpm_scope_validator.py`, `service/workflow_category_service.py`, `service/workflow_template_service.py`, `service/workflow_definition_service.py`, `service/workflow_version_service.py` |
| Engines | `service/engines/__init__.py`, `service/engines/workflow_category_engine.py`, `service/engines/workflow_template_engine.py`, `service/engines/workflow_definition_engine.py`, `service/engines/workflow_version_engine.py` |
| Adapters | `adapters/__init__.py`, `adapters/foundation_port.py`, `adapters/master_data_port.py`, `adapters/organization_port.py`, `adapters/analytics_port.py`, `adapters/integration_port.py` |
| Routers | `routers/__init__.py` |

### Migrations — `apps/api/alembic/versions/`

| Revision | File |
|----------|------|
| `0465_create_bpm_schema` | `0465_create_bpm_schema.py` |
| `0466_bpm_workflow_category` | `0466_bpm_workflow_category.py` |
| `0467_bpm_workflow_template` | `0467_bpm_workflow_template.py` |
| `0468_bpm_workflow_definition` | `0468_bpm_workflow_definition.py` |
| `0469_bpm_workflow_version` | `0469_bpm_workflow_version.py` |
| `0470_seed_bpm_permissions` | `0470_seed_bpm_permissions.py` |

### Tests — `apps/api/src/tests/`

| Kind | File |
|------|------|
| Unit | `unit/bpm/test_bpm_hub_engines.py` |
| Unit | `unit/bpm/test_bpm_hub_tasks.py` |
| Security | `security/bpm/test_bpm_hub_permissions.py` |
| Integration | `integration/bpm/test_bpm_hub_module_import.py` |

### Frontend — `apps/web/src/`

| Area | Files |
|------|--------|
| Types | `modules/bpm/types/bpm.ts` |
| Services | `modules/bpm/services/bpm-api.ts` |
| Components | `modules/bpm/components/bpm-ui.tsx`, `permission-gate.tsx`, `category-explorer.tsx`, `category-form.tsx`, `template-library.tsx`, `template-form.tsx`, `definition-list.tsx`, `definition-form.tsx`, `definition-detail.tsx` |
| Routes | `app/bpm/layout.tsx`, `app/bpm/page.tsx`, `app/bpm/categories/page.tsx`, `app/bpm/categories/new/page.tsx`, `app/bpm/categories/[id]/page.tsx`, `app/bpm/templates/page.tsx`, `app/bpm/templates/new/page.tsx`, `app/bpm/templates/[id]/page.tsx`, `app/bpm/definitions/page.tsx`, `app/bpm/definitions/new/page.tsx`, `app/bpm/definitions/[id]/page.tsx` |

### Report

| File |
|------|
| `docs/07_RELEASES/Sprint_25_Phase1_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/shared/router.py` | Registered `bpm_router` |
| `apps/api/alembic/env.py` | Registered `modules.bpm.models` |
| `apps/api/src/workers/celery_app.py` | Autodiscover `modules.bpm` |

---

## APIs / Routes

**Mount:** `/api/v1/bpm`  
**Total Phase 1 routes:** 21

### Categories — `/api/v1/bpm/categories`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `bpm.category:read` |
| GET | `/{row_id}` | `bpm.category:read` |
| POST | `` | `bpm.category:create` |
| PATCH | `/{row_id}` | `bpm.category:update` |
| DELETE | `/{row_id}` | `bpm.category:delete` |

### Templates — `/api/v1/bpm/templates`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `bpm.template:read` |
| GET | `/{row_id}` | `bpm.template:read` |
| POST | `` | `bpm.template:create` |
| PATCH | `/{row_id}` | `bpm.template:update` |
| POST | `/{row_id}/copy` | `bpm.template:copy` |

### Definitions — `/api/v1/bpm/definitions`

| Method | Path | Permission |
|--------|------|------------|
| GET | `` | `bpm.definition:read` |
| GET | `/{row_id}` | `bpm.definition:read` |
| POST | `` | `bpm.definition:create` |
| PATCH | `/{row_id}` | `bpm.definition:update` |
| GET | `/{row_id}/versions` | `bpm.version:read` |

### Versions — `/api/v1/bpm/versions`

| Method | Path | Permission |
|--------|------|------------|
| GET | `/{row_id}` | `bpm.version:read` |
| POST | `` | `bpm.version:create` |
| PATCH | `/{row_id}` | `bpm.version:update` |
| POST | `/{row_id}/publish` | `bpm.version:publish` |
| POST | `/{row_id}/retire` | `bpm.version:retire` |
| POST | `/{row_id}/clone` | `bpm.version:clone` |

---

## Components

| Component | Purpose |
|-----------|---------|
| `CategoryExplorer` | Enterprise list · search · filters · pagination · column preferences · CSV export · sticky toolbar |
| `CategoryForm` | Create / Edit · unsaved warning |
| `TemplateLibrary` | Enterprise list · Copy Template dialog · export |
| `TemplateForm` | Create / Edit |
| `DefinitionList` | Enterprise list · module/status filters · export |
| `DefinitionForm` | Create definition |
| `DefinitionDetail` | Detail · Version Timeline · Publish Dialog · Clone Dialog · unsaved warning |
| `PermissionGate` | Permission-aware UI |
| `BpmSkeleton` / `BpmEmptyState` / `BpmRetry` / `StickyToolbar` / `ConfirmDialog` / `UnsavedWarning` | Shared UX primitives |

---

## Services

| Service | Role |
|---------|------|
| `BpmApplicationService` | Application facade |
| `BpmIntegrationService` | Cross-module consume ports |
| `BpmNumberService` | Document numbering (`CAT-` / `TPL-` / `DEF-` / `VER-`) |
| `WorkflowCategoryService` | Category CRUD + activate/deactivate |
| `WorkflowTemplateService` | Template CRUD + copy |
| `WorkflowDefinitionService` | Definition CRUD + initial draft version seed |
| `WorkflowVersionService` | Draft / publish / retire / clone lifecycle |

---

## Repositories

| Repository |
|------------|
| `WorkflowCategoryRepository` |
| `WorkflowTemplateRepository` |
| `WorkflowDefinitionRepository` |
| `WorkflowVersionRepository` |
| `CodeSequenceRepository` |
| `BpmScopedRepository` (base) |

---

## Permissions

| Permission |
|------------|
| `bpm.category:read` · `create` · `update` · `delete` |
| `bpm.template:read` · `create` · `update` · `copy` |
| `bpm.definition:read` · `create` · `update` |
| `bpm.version:read` · `create` · `update` · `publish` · `retire` · `clone` |

### Roles Seeded

| Role | Slice |
|------|--------|
| `BPM_ADMIN` | All |
| `PROCESS_DESIGNER` | Design (no publish / retire / delete) |
| `PROCESS_OWNER` | Read + publish / retire + limited updates |
| `WORKFLOW_OPERATOR` | Read |
| `WORKFLOW_AUDITOR` | Read |

---

## Tasks

| Celery Task | Name |
|-------------|------|
| `definition_inventory_snapshot` | `bpm.definition_inventory_snapshot` |
| `published_version_guard` | `bpm.published_version_guard` |
| `draft_aging_report` | `bpm.draft_aging_report` |

---

## Tests

| Suite | Result |
|-------|--------|
| Unit engines | PASS |
| Unit tasks | PASS |
| Security permissions | PASS |
| Integration module import | PASS |
| **Total** | **16 passed** |

---

## Cross-Module Consume (Phase 1)

| Module | Integration |
|--------|-------------|
| Foundation Security | Role UUID resolve (consume) |
| Master Employee | `owner_employee_id` FK / adapter |
| Organization | `department_id` FK / adapter |
| Analytics | Report UUID ref adapter (read-only) |
| Integration Hub | Connector UUID ref adapter |

### Do Not Own (confirmed)

Business documents · Finance · Sales · CRM · Inventory · Foundation `wf_*`

---

## Remaining Work for Phase 2

| Area | Remaining ERD Tables / Capabilities |
|------|-------------------------------------|
| Visual Designer | `bpm_designer_node`, `bpm_designer_transition` |
| Intelligence | `bpm_decision_table`, `bpm_business_rule`, `bpm_workflow_variable`, `bpm_form_reference` |
| Governance | `bpm_assignment_rule`, `bpm_escalation_policy`, `bpm_sla_policy`, `bpm_task_delegation` |
| Triggers / Comms | `bpm_workflow_trigger`, `bpm_notification_template` |
| Simulation | `bpm_simulation_run` (status · duration · warnings · errors) |
| Runtime | `bpm_workflow_instance`, `bpm_workflow_task`, `bpm_workflow_history` |
| UI | Visual designer canvas · decision table editor · simulation console · task inbox |
| Engine | Runtime execution on Published version only · SLA timers · escalation jobs · C-04 alignment (no second engine) |
| Frontend | Full XLSX export library · session-backed permission hydration · column preference persistence |

**Phase 2 table count remaining:** 16 of 20 ERD-25 business tables.

---

**Sprint 25 Phase 1 — Complete.**
