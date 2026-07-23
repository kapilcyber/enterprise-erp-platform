"""Low-Code Phase 3A module import smoke tests."""


def test_phase3a_models_exported():
    from modules.lowcode import models

    assert models.LcEventHandler is not None
    assert models.LcLocalizationEntry is not None
    assert len(models.__all__) == 18


def test_phase3a_services_exported():
    from modules.lowcode.service import EventHandlerService, LocalizationEntryService

    assert EventHandlerService is not None
    assert LocalizationEntryService is not None


def test_phase3a_routers_mounted():
    from modules.lowcode.router import lowcode_router

    paths = [getattr(r, "path", "") for r in lowcode_router.routes]
    assert any("event-handlers" in p for p in paths)
    assert any("localization-entries" in p for p in paths)


def test_application_service_wires_phase3a():
    from unittest.mock import MagicMock

    from modules.lowcode.service.application_service import LowcodeApplicationService

    app = LowcodeApplicationService(MagicMock())
    assert app.event_handlers is not None
    assert app.localization_entries is not None
