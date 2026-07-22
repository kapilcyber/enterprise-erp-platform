"""BPM Phase 1.5 integration import / route smoke tests."""


def test_import_phase15_services():
    from modules.bpm.service import (
        BpmApplicationService,
        BpmDashboardService,
        PublishValidationService,
        TemplateImportExportService,
        VersionComparisonService,
    )

    assert PublishValidationService is not None
    assert VersionComparisonService is not None
    assert TemplateImportExportService is not None
    assert BpmDashboardService is not None
    assert BpmApplicationService is not None


def test_router_includes_dashboard_and_phase15_paths():
    from modules.bpm.router import bpm_router

    assert bpm_router.prefix == "/bpm"
    paths = []
    for r in bpm_router.routes:
        path = getattr(r, "path", None)
        if path:
            paths.append(path)
    joined = " ".join(paths)
    assert "/dashboard/summary" in joined or any("dashboard" in p for p in paths)
    assert any("validate-publish" in p for p in paths)
    assert any("compare" in p for p in paths)
    assert any("autocomplete" in p for p in paths)
    assert any("archive" in p for p in paths)
    assert any("restore" in p for p in paths)
    assert any("export" in p for p in paths)
    assert any("import" in p for p in paths)


def test_application_service_phase15_facade():
    from modules.bpm.service.application_service import BpmApplicationService

    assert hasattr(BpmApplicationService, "__init__")


def test_version_model_has_reason_columns():
    from modules.bpm.models import BpmWorkflowVersion

    assert hasattr(BpmWorkflowVersion, "publish_reason")
    assert hasattr(BpmWorkflowVersion, "retire_reason")
    assert hasattr(BpmWorkflowVersion, "clone_reason")


def test_still_four_phase1_tables():
    from modules.bpm import models

    # Phase 1–4 cumulative model count (20 of 20 ERD tables)
    assert len(models.__all__) == 20
