"""Low-Code Phase 2C module import smoke tests."""


def test_phase2c_models_exported():
    from modules.lowcode import models

    assert models.LcDataSource is not None
    assert models.LcExpression is not None
    assert models.LcExpressionBinding is not None
    assert len(models.__all__) == 18


def test_phase2c_services_exported():
    from modules.lowcode.service import (
        DataSourceService,
        ExpressionBindingService,
        ExpressionService,
    )

    assert DataSourceService is not None
    assert ExpressionService is not None
    assert ExpressionBindingService is not None


def test_phase2c_routers_mounted():
    from modules.lowcode.router import lowcode_router

    paths = [getattr(r, "path", "") for r in lowcode_router.routes]
    assert any("data-sources" in p for p in paths)
    assert any("expressions" in p for p in paths)
    assert any("expression-bindings" in p for p in paths)


def test_form_field_has_data_source_column():
    from modules.lowcode.models import LcFormField

    assert hasattr(LcFormField, "data_source_id")


def test_application_service_wires_phase2c():
    from unittest.mock import MagicMock

    from modules.lowcode.service.application_service import LowcodeApplicationService

    app = LowcodeApplicationService(MagicMock())
    assert app.data_sources is not None
    assert app.expressions is not None
    assert app.expression_bindings is not None
