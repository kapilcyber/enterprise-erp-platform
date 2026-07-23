"""Low-Code module import smoke tests — Phase 1."""


def test_import_models():
    from modules.lowcode import models

    assert models.LcFormCategory is not None
    assert models.LcFormDefinition is not None
    assert models.LcFormVersion is not None
    assert len(models.__all__) == 18


def test_import_router():
    from modules.lowcode.router import lowcode_router

    assert lowcode_router.prefix == "/lowcode"


def test_import_services():
    from modules.lowcode.service import (
        LowcodeApplicationService,
        LowcodeIntegrationService,
        LowcodeNumberService,
    )

    assert LowcodeApplicationService is not None
    assert LowcodeIntegrationService is not None
    assert LowcodeNumberService is not None


def test_phase1_tables_only():
    from modules.lowcode.models import __all__

    expected = {
        "LcFormCategory",
        "LcFormDefinition",
        "LcFormVersion",
        "LcFormSection",
        "LcFormField",
        "LcComponent",
        "LcComponentVersion",
        "LcDataSource",
        "LcExpression",
        "LcExpressionBinding",
        "LcEventHandler",
        "LcLocalizationEntry",
        "LcPageDefinition",
        "LcPageVersion",
        "LcPageRegion",
        "LcPublishHistory",
        "LcRuntimeSubmission",
        "LcPreviewSession",
    }
    assert set(__all__) == expected


def test_shared_router_includes_lowcode():
    from shared.router import api_v1_router

    # Ensure lowcode routes are mounted under API v1
    mounted = []
    for route in api_v1_router.routes:
        path = getattr(route, "path", "") or ""
        mounted.append(path)
    assert any("categories" in p or "definitions" in p or "versions" in p for p in mounted) or any(
        "lowcode" in p for p in mounted
    )
