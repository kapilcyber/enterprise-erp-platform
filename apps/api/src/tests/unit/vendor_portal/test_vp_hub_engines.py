"""Vendor Portal engine unit tests."""

from types import SimpleNamespace

from modules.vendor_portal.service.engines.portal_account_engine import PortalAccountEngine
from modules.vendor_portal.service.engines.quote_submission_engine import QuoteSubmissionEngine
from modules.vendor_portal.service.engines.asn_engine import AsnEngine


def test_portal_account_submit_approve():
    row = SimpleNamespace(status="draft")
    eng = PortalAccountEngine()
    eng.submit(row)
    assert row.status == "submitted"
    eng.approve(row)
    assert row.status == "approved"


def test_quote_submission_flow():
    row = SimpleNamespace(status="draft")
    eng = QuoteSubmissionEngine()
    eng.submit(row)
    assert row.status == "submitted"
    eng.approve(row)
    assert row.status == "accepted"


def test_asn_flow():
    row = SimpleNamespace(status="draft")
    eng = AsnEngine()
    eng.submit(row)
    assert row.status == "submitted"
    eng.approve(row)
    assert row.status == "approved"
