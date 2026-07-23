"""Low-Code Phase 2B module import smoke tests."""


def test_phase2b_models_exported():
    from modules.lowcode import models

    assert models.LcComponent is not None
    assert models.LcComponentVersion is not None
    assert len(models.__all__) == 18


def test_phase2b_services_exported():
    from modules.lowcode.service import ComponentService, ComponentVersionService

    assert ComponentService is not None
    assert ComponentVersionService is not None


def test_phase2b_routers_mounted():
    from modules.lowcode.router import lowcode_router

    paths = [getattr(r, "path", "") for r in lowcode_router.routes]
    assert any("components" in p for p in paths)
    assert any("component-versions" in p for p in paths)


def test_form_field_has_component_version_column():
    from modules.lowcode.models import LcFormField

    assert hasattr(LcFormField, "component_version_id")
