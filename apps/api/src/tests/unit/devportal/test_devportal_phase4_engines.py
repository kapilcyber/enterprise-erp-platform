"""Unit tests — Developer Portal Phase 4 engines."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from modules.devportal.domain.exceptions import (
    AnalyticsWarehouseForbidden,
    InvalidPortalReportState,
    PortalReportProjectionStale,
    PortalReportTypeError,
)
from modules.devportal.service.engines import PortalReportEngine


def test_portal_report_types_and_finalize():
    engine = PortalReportEngine()
    engine.assert_report_type("active_developers")
    engine.assert_report_type("hub_usage")
    with pytest.raises(PortalReportTypeError):
        engine.assert_report_type("billing")
    row = SimpleNamespace(
        status="draft",
        finalized_at=None,
        finalized_by=None,
        report_type="applications",
        projection_snapshot_json=None,
    )
    engine.finalize(row, user_id=uuid4())
    assert row.status == "finalized"
    with pytest.raises(InvalidPortalReportState):
        engine.assert_editable(row)


def test_export_requires_finalize_and_hub_projection():
    engine = PortalReportEngine()
    draft = SimpleNamespace(status="draft", report_type="hub_usage", projection_snapshot_json=None)
    with pytest.raises(InvalidPortalReportState):
        engine.assert_exportable(draft)
    row = SimpleNamespace(
        status="finalized",
        report_type="hub_usage",
        projection_snapshot_json=None,
    )
    with pytest.raises(PortalReportProjectionStale):
        engine.assert_projection_freshness(row)
    row.projection_snapshot_json = {"projected": True}
    engine.assert_projection_freshness(row)
    engine.assert_exportable(row)


def test_analytics_warehouse_forbidden():
    engine = PortalReportEngine()
    with pytest.raises(AnalyticsWarehouseForbidden):
        engine.assert_metadata_only()
