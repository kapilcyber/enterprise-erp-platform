"""API Developer Portal Phase 3 package smoke."""

from pathlib import Path


def test_phase3_models_export_17():
    from modules.devportal import models

    assert len(models.__all__) >= 17
    assert "DpDocumentationEntry" in models.__all__
    assert "DpOpenapiArtifactReference" in models.__all__
    assert "DpSandboxEnvironment" in models.__all__
    assert "DpTryitSession" in models.__all__


def test_phase3_routes_registered():
    from modules.devportal.router import devportal_router

    paths = [getattr(r, "path", "") for r in devportal_router.routes]
    assert any("documentation-entries" in p for p in paths)
    assert any("openapi-artifact-references" in p for p in paths)
    assert any("sandbox-environments" in p for p in paths)
    assert any("tryit-sessions" in p for p in paths)


def test_alembic_phase3_chain():
    versions = Path(__file__).resolve().parents[4] / "alembic" / "versions"
    for name in (
        "0575_dp_documentation_entry.py",
        "0576_dp_openapi_artifact_reference.py",
        "0577_dp_sandbox_environment.py",
        "0578_dp_tryit_session.py",
        "0579_seed_devportal_phase3_permissions.py",
    ):
        assert (versions / name).exists(), name


def test_permissions_phase3_resources():
    from modules.devportal.permissions import (
        DEVPORTAL_PERMISSIONS,
        DEVPORTAL_PHASE3_PERMISSIONS,
    )

    resources = {p[1] for p in DEVPORTAL_PERMISSIONS}
    for expected in (
        "devportal.documentation_entry",
        "devportal.openapi_artifact_reference",
        "devportal.sandbox_environment",
        "devportal.tryit_session",
    ):
        assert expected in resources
    assert len(DEVPORTAL_PHASE3_PERMISSIONS) > 0


def test_application_service_wires_phase3():
    import inspect

    from modules.devportal.service.application_service import DevportalApplicationService

    src = inspect.getsource(DevportalApplicationService.__init__)
    assert "self.documentation_entries" in src
    assert "self.openapi_artifact_references" in src
    assert "self.sandbox_environments" in src
    assert "self.tryit_sessions" in src


def test_no_runtime_or_binary_ownership():
    from pathlib import Path

    service_dir = Path(__file__).resolve().parents[3] / "modules" / "devportal" / "service"
    for name in (
        "documentation_entry_service.py",
        "openapi_artifact_reference_service.py",
        "sandbox_environment_service.py",
        "tryit_session_service.py",
    ):
        source = (service_dir / name).read_text(encoding="utf-8").lower()
        assert "modules.document.models" not in source
        assert "kubernetes" not in source
        assert "kong" not in source
        assert "envoy" not in source
        assert "openapi.json" not in source or "generator" not in source
