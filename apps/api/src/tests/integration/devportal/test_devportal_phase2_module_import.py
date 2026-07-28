"""API Developer Portal Phase 2 package smoke."""

from pathlib import Path


def test_phase2_models_export_13():
    from modules.devportal import models

    assert len(models.__all__) >= 13
    assert "DpPlan" in models.__all__
    assert "DpSubscription" in models.__all__
    assert "DpEntitlement" in models.__all__


def test_import_router_phase2_routes():
    from modules.devportal.router import devportal_router

    assert devportal_router.prefix == "/devportal"
    paths = [getattr(r, "path", "") for r in devportal_router.routes]
    assert any("/plans" in p for p in paths)
    assert any("/subscriptions" in p for p in paths)
    assert any("/entitlements" in p for p in paths)


def test_alembic_phase2_chain():
    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    for name in (
        "0571_dp_plan.py",
        "0572_dp_subscription.py",
        "0573_dp_entitlement.py",
        "0574_seed_devportal_phase2_permissions.py",
    ):
        assert (versions / name).exists(), name


def test_permissions_phase2_resources():
    from modules.devportal.permissions import (
        DEVPORTAL_PERMISSIONS,
        DEVPORTAL_PHASE2_PERMISSIONS,
    )

    resources = {p[1] for p in DEVPORTAL_PERMISSIONS}
    assert "devportal.plan" in resources
    assert "devportal.subscription" in resources
    assert "devportal.entitlement" in resources
    assert len(DEVPORTAL_PHASE2_PERMISSIONS) > 0
    assert all(
        p[1].endswith((".plan", ".subscription", ".entitlement"))
        or p[1].split(".")[-1] in {"plan", "subscription", "entitlement"}
        for p in DEVPORTAL_PHASE2_PERMISSIONS
    )


def test_application_service_wires_phase2():
    import inspect

    from modules.devportal.service.application_service import DevportalApplicationService

    src = inspect.getsource(DevportalApplicationService.__init__)
    assert "self.plans" in src
    assert "self.subscriptions" in src
    assert "self.entitlements" in src


def test_no_gateway_or_billing_in_phase2_services():
    from pathlib import Path

    service_dir = Path(__file__).resolve().parents[3] / "modules" / "devportal" / "service"
    for name in ("plan_service.py", "subscription_service.py", "entitlement_service.py"):
        source = (service_dir / name).read_text(encoding="utf-8").lower()
        assert "modules.integration.models" not in source
        assert "billing" not in source
        assert "payment" not in source
        assert "kong" not in source
        assert "envoy" not in source
        assert "gateway enforce" not in source