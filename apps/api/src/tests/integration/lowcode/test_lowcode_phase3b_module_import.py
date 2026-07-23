"""Low-Code Phase 3B module import smoke tests."""


def test_phase3b_models_exported():
    from modules.lowcode import models

    assert models.LcPageDefinition is not None
    assert models.LcPageVersion is not None
    assert models.LcPageRegion is not None
    assert len(models.__all__) == 18


def test_phase3b_services_exported():
    from modules.lowcode.service import (
        PageDefinitionService,
        PageRegionService,
        PageVersionService,
    )

    assert PageDefinitionService is not None
    assert PageVersionService is not None
    assert PageRegionService is not None


def test_phase3b_routers_mounted():
    from modules.lowcode.router import lowcode_router

    paths = [getattr(r, "path", "") for r in lowcode_router.routes]
    assert any("/pages" in p for p in paths)
    assert any("page-versions" in p for p in paths)
    assert any("page-regions" in p for p in paths)


def test_application_service_wires_phase3b():
    from unittest.mock import MagicMock

    from modules.lowcode.service.application_service import LowcodeApplicationService

    app = LowcodeApplicationService(MagicMock())
    assert app.page_definitions is not None
    assert app.page_versions is not None
    assert app.page_regions is not None
