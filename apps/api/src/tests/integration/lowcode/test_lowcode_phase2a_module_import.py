"""Low-Code Phase 2A module import smoke tests."""


def test_phase2a_models_exported():
    from modules.lowcode import models

    assert models.LcFormSection is not None
    assert models.LcFormField is not None
    assert len(models.__all__) == 18


def test_phase2a_services_exported():
    from modules.lowcode.service import (
        FormFieldService,
        FormSectionService,
        FormStructureValidationService,
    )

    assert FormSectionService is not None
    assert FormFieldService is not None
    assert FormStructureValidationService is not None


def test_phase2a_routers_mounted():
    from modules.lowcode.router import lowcode_router

    paths = [getattr(r, "path", "") for r in lowcode_router.routes]
    assert any("sections" in p for p in paths)
    assert any("fields" in p for p in paths)
    assert any("structure" in p for p in paths)
