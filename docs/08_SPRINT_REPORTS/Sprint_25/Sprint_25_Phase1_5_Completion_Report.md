# Sprint 25 Phase 1.5 Completion Report

| Field | Value |
|-------|--------|
| **Release Target** | ERP Core v1.20-beta (planned) |
| **Sprint** | Sprint 25 — Workflow & BPM Designer |
| **Phase** | Phase 1.5 — Backend Polish |
| **Status** | Complete |
| **Architecture Lock** | v1.1 — Preserved |
| **FRD / ERD** | FRD-25 / ERD-25 — Preserved |
| **New ERD Tables** | None |
| **Tables Touched** | `bpm_workflow_category` · `bpm_workflow_template` · `bpm_workflow_definition` · `bpm_workflow_version` |
| **Alembic Head** | `0471_bpm_phase15_polish` |
| **BPM Tests** | 32 passed |

---

## Scope Delivered

| # | Capability | Delivery |
|---|------------|----------|
| 1 | Publish validation service | Structured validate-before-publish |
| 2 | Soft archive | Category · Template · Definition |
| 3 | Restore | Category · Template · Definition |
| 4 | Version comparison API | Structured field diffs (no UI) |
| 5 | Template import/export | JSON export · JSON import validation |
| 6 | Search optimization | Autocomplete · Recent · Popular |
| 7 | Dashboard summary APIs | Counts only |
| 8 | Audit improvements | Publish / retire / clone reason |
| 9 | Repository optimization | Indexes · search · pagination · sorting |
| 10 | Tests | Unit · Security · Integration |

### Explicitly Not Done

- No Phase 2 ERD tables
- No redesign
- No previous-module changes (except required BPM wiring already in Phase 1)
- No frontend features beyond API readiness

---

## Files Created

### Services

| File |
|------|
| `apps/api/src/modules/bpm/service/publish_validation_service.py` |
| `apps/api/src/modules/bpm/service/version_comparison_service.py` |
| `apps/api/src/modules/bpm/service/template_import_export_service.py` |
| `apps/api/src/modules/bpm/service/bpm_dashboard_service.py` |

### Migration

| File |
|------|
| `apps/api/alembic/versions/0471_bpm_phase15_polish.py` |

### Tests

| File |
|------|
| `apps/api/src/tests/unit/bpm/test_bpm_phase15_services.py` |
| `apps/api/src/tests/security/bpm/test_bpm_phase15_permissions.py` |
| `apps/api/src/tests/integration/bpm/test_bpm_phase15_module_import.py` |

### Report

| File |
|------|
| `docs/07_RELEASES/Sprint_25_Phase1_5_Completion_Report.md` |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/api/src/modules/bpm/domain/value_objects.py` | Validation / compare / page / dashboard / import VOs |
| `apps/api/src/modules/bpm/models/workflow_version.py` | `publish_reason` · `retire_reason` · `clone_reason` |
| `apps/api/src/modules/bpm/models/workflow_category.py` | Search indexes |
| `apps/api/src/modules/bpm/models/workflow_template.py` | Search / module / updated indexes |
| `apps/api/src/modules/bpm/models/workflow_definition.py` | Search / template indexes |
| `apps/api/src/modules/bpm/repository/base.py` | `paginate_sorted` |
| `apps/api/src/modules/bpm/repository/workflow_category_repository.py` | Page · archive · restore · count |
| `apps/api/src/modules/bpm/repository/workflow_template_repository.py` | Page · autocomplete · recent · popular · archive · restore |
| `apps/api/src/modules/bpm/repository/workflow_definition_repository.py` | Page · archive · restore · count |
| `apps/api/src/modules/bpm/repository/workflow_version_repository.py` | Published count · status counts |
| `apps/api/src/modules/bpm/service/workflow_category_service.py` | Archive / restore / pagination |
| `apps/api/src/modules/bpm/service/workflow_template_service.py` | Archive / restore / search helpers / pagination |
| `apps/api/src/modules/bpm/service/workflow_definition_service.py` | Archive / restore / pagination |
| `apps/api/src/modules/bpm/service/workflow_version_service.py` | Validate-before-publish · reason audit |
| `apps/api/src/modules/bpm/service/application_service.py` | Phase 1.5 facade wiring |
| `apps/api/src/modules/bpm/service/__init__.py` | Export new services |
| `apps/api/src/modules/bpm/schemas.py` | Phase 1.5 request/response schemas |
| `apps/api/src/modules/bpm/permissions.py` | Phase 1.5 permission codes |
| `apps/api/src/modules/bpm/dependencies.py` | Sort params · page payload |
| `apps/api/src/modules/bpm/routers/__init__.py` | New endpoints |
| `apps/api/src/modules/bpm/router.py` | Dashboard router include |

---

## New APIs

**Mount:** `/api/v1/bpm`

### Dashboard

| Method | Path | Permission |
|--------|------|------------|
| GET | `/dashboard/summary` | `bpm.dashboard:read` |

Counts: categories · templates · definitions · draft · published · retired

### Categories

| Method | Path | Permission |
|--------|------|------------|
| POST | `/categories/{id}/archive` | `bpm.category:archive` |
| POST | `/categories/{id}/restore` | `bpm.category:restore` |

List returns paginated payload (`items` · `total` · `page` · `page_size` · `sort_by` · `sort_dir`).

### Templates

| Method | Path | Permission |
|--------|------|------------|
| GET | `/templates/autocomplete?q=` | `bpm.template:read` |
| GET | `/templates/recent` | `bpm.template:read` |
| GET | `/templates/popular` | `bpm.template:read` |
| GET | `/templates/{id}/export` | `bpm.template:export` |
| POST | `/templates/import/validate` | `bpm.template:import` |
| POST | `/templates/{id}/archive` | `bpm.template:archive` |
| POST | `/templates/{id}/restore` | `bpm.template:restore` |

### Definitions

| Method | Path | Permission |
|--------|------|------------|
| POST | `/definitions/{id}/archive` | `bpm.definition:archive` |
| POST | `/definitions/{id}/restore` | `bpm.definition:restore` |

### Versions

| Method | Path | Permission |
|--------|------|------------|
| GET | `/versions/compare?left_id=&right_id=` | `bpm.version:compare` |
| POST | `/versions/{id}/validate-publish` | `bpm.version:validate` |
| POST | `/versions/{id}/publish` | body: `publish_reason` |
| POST | `/versions/{id}/retire` | body: `retire_reason` |
| POST | `/versions/{id}/clone` | body: `clone_reason` |

Publish runs validation first; fails with structured conflict when invalid.

---

## Repository Changes

| Repository | Changes |
|------------|---------|
| `BpmScopedRepository` | `paginate_sorted` helper |
| `WorkflowCategoryRepository` | PageResult · soft archive · restore · `count_active` |
| `WorkflowTemplateRepository` | PageResult · autocomplete · recent · popular · archive · restore · `count_active` |
| `WorkflowDefinitionRepository` | PageResult · archive · restore · `count_active` |
| `WorkflowVersionRepository` | `count_published` · `count_by_status` |

### Indexes Added (migration `0471`)

- category: `(company_id, category_name)` · `(company_id, category_code)`
- template: `(company_id, template_name)` · `(company_id, template_code)` · `(company_id, module_code)` · `(company_id, updated_at)`
- definition: `(company_id, definition_name)` · `(company_id, definition_code)` · `(template_id)`

### Columns Added (existing table only)

| Table | Columns |
|-------|---------|
| `bpm_workflow_version` | `publish_reason` · `retire_reason` · `clone_reason` |

---

## Services

| Service | Role |
|---------|------|
| `PublishValidationService` | Exactly-one-published · category · template · definition · version state · ownership · module/entity dependency |
| `VersionComparisonService` | Structured field diffs between two versions |
| `TemplateImportExportService` | JSON export · JSON import validation only |
| `BpmDashboardService` | Aggregate counts |
| `WorkflowCategoryService` | + archive / restore / sorted pagination |
| `WorkflowTemplateService` | + archive / restore / autocomplete / recent / popular |
| `WorkflowDefinitionService` | + archive / restore / sorted pagination |
| `WorkflowVersionService` | + validate-before-publish · reason audit fields |

### Soft Archive Semantics

- Soft archive only (`is_deleted` / `deleted_at` / `deleted_by`)
- No hard delete
- Restore clears soft-archive flags

---

## Permissions (Phase 1.5 additions)

| Permission |
|------------|
| `bpm.category:archive` · `bpm.category:restore` |
| `bpm.template:archive` · `bpm.template:restore` · `bpm.template:export` · `bpm.template:import` |
| `bpm.definition:archive` · `bpm.definition:restore` |
| `bpm.version:compare` · `bpm.version:validate` |
| `bpm.dashboard:read` |

Roles re-synced: `BPM_ADMIN` · `PROCESS_DESIGNER` · `PROCESS_OWNER` · `WORKFLOW_OPERATOR` · `WORKFLOW_AUDITOR`

---

## Tests

| Suite | Coverage | Result |
|-------|----------|--------|
| Unit | Publish VO · compare VO · import validation · dashboard keys · immutability | PASS |
| Security | Phase 1.5 permission presence · role slices | PASS |
| Integration | Service imports · route paths · reason columns · 4-table lock | PASS |
| Prior Phase 1 suite | Engines · tasks · permissions · imports | PASS |
| **Total BPM** | | **32 passed** |

---

## Remaining Work for Phase 2

| Area | Remaining |
|------|-----------|
| Visual Designer | `bpm_designer_node` · `bpm_designer_transition` |
| Intelligence | `bpm_decision_table` · `bpm_business_rule` · `bpm_workflow_variable` · `bpm_form_reference` |
| Governance | `bpm_assignment_rule` · `bpm_escalation_policy` · `bpm_sla_policy` · `bpm_task_delegation` |
| Triggers / Comms | `bpm_workflow_trigger` · `bpm_notification_template` |
| Simulation | `bpm_simulation_run` |
| Runtime | `bpm_workflow_instance` · `bpm_workflow_task` · `bpm_workflow_history` |
| UI | Visual designer · decision tables · simulation console · task inbox |
| Engine | Runtime on Published only · SLA · escalation · C-04 (no second engine) |

**Phase 2 table count remaining:** 16 of 20 ERD-25 business tables.

---

**Sprint 25 Phase 1.5 — Complete.**
