"""API Developer Portal Phase 0 package smoke."""


def test_module_import():
    import modules.devportal as devportal_pkg
    from modules.devportal import (
        adapters,
        dependencies,
        domain,
        models,
        permissions,
        repository,
        schemas,
        service,
        tasks,
    )
    from modules.devportal.router import devportal_router

    assert devportal_pkg is not None
    assert devportal_router.prefix == "/devportal"
    assert domain is not None
    assert models is not None
    assert repository is not None
    assert service is not None
    assert adapters is not None
    assert schemas is not None
    assert permissions is not None
    assert dependencies is not None
    assert tasks is not None


def test_router_mount():
    from pathlib import Path

    from modules.devportal.router import devportal_router

    assert devportal_router.prefix == "/devportal"
    shared_router_path = Path(__file__).resolve().parents[3] / "shared" / "router.py"
    source = shared_router_path.read_text(encoding="utf-8")
    assert "from modules.devportal.router import devportal_router" in source
    assert "include_router(devportal_router)" in source


def test_package_smoke():
    from modules.devportal.adapters import (
        DevportalAnalyticsAdapter,
        DevportalDocumentAdapter,
        DevportalFoundationAdapter,
        DevportalIntegrationHubAdapter,
    )
    from modules.devportal.permissions import DEVPORTAL_PERMISSION_NAMESPACE, DEVPORTAL_PERMISSIONS
    from modules.devportal.repository.base import DevportalScopedRepository
    from modules.devportal.service import DevportalApplicationService, DevportalScopeValidator
    from modules.devportal.tasks import module_health_ping

    assert DEVPORTAL_PERMISSION_NAMESPACE == "devportal"
    assert DEVPORTAL_PERMISSIONS  # Phase 1 seeded constants
    assert DevportalApplicationService is not None
    assert DevportalScopeValidator is not None
    assert DevportalScopedRepository is not None
    assert DevportalFoundationAdapter is not None
    assert DevportalIntegrationHubAdapter is not None
    assert DevportalDocumentAdapter is not None
    assert DevportalAnalyticsAdapter is not None
    assert module_health_ping.name == "devportal.module_health_ping"
    result = module_health_ping()
    assert result["status"] == "ok"
    assert result["module"] == "devportal"
    assert result["phase"] in {0, 1, 2, 3, 4}
    assert models_empty() is False  # Phase 1 exports models


def models_empty() -> bool:
    from modules.devportal import models

    return list(models.__all__) == []
