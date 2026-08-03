"""Monitoring Phase 0 package smoke."""


def test_module_import():
    import modules.monitoring as monitoring_pkg
    from modules.monitoring import (
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
    from modules.monitoring.router import monitoring_router

    assert monitoring_pkg is not None
    assert monitoring_router.prefix == "/monitoring"
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

    from modules.monitoring.router import monitoring_router

    assert monitoring_router.prefix == "/monitoring"
    shared_router_path = Path(__file__).resolve().parents[3] / "shared" / "router.py"
    source = shared_router_path.read_text(encoding="utf-8")
    assert "from modules.monitoring.router import monitoring_router" in source
    assert "include_router(monitoring_router)" in source


def test_package_smoke():
    from modules.monitoring.adapters import (
        MonitoringAnalyticsAdapter,
        MonitoringAuditAdapter,
        MonitoringExternalPlatformAdapter,
        MonitoringFoundationAdapter,
        MonitoringIntegrationHubAdapter,
        MonitoringNotificationAdapter,
        MonitoringWorkflowAdapter,
    )
    from modules.monitoring.permissions import MONITORING_PERMISSION_NAMESPACE
    from modules.monitoring.repository.base import MonitoringScopedRepository
    from modules.monitoring.service import MonitoringApplicationService, MonitoringScopeValidator
    from modules.monitoring.tasks import module_health_ping

    assert MONITORING_PERMISSION_NAMESPACE == "monitoring"
    assert MonitoringApplicationService is not None
    assert MonitoringScopeValidator is not None
    assert MonitoringScopedRepository is not None
    assert MonitoringFoundationAdapter is not None
    assert MonitoringWorkflowAdapter is not None
    assert MonitoringNotificationAdapter is not None
    assert MonitoringAuditAdapter is not None
    assert MonitoringAnalyticsAdapter is not None
    assert MonitoringIntegrationHubAdapter is not None
    assert MonitoringExternalPlatformAdapter is not None
    assert module_health_ping.name == "monitoring.module_health_ping"
    result = module_health_ping()
    assert result["status"] == "ok"
    assert result["module"] == "monitoring"
