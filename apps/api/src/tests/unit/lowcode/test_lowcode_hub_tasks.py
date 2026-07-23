"""Low-Code Celery task smoke tests — Phase 1."""

from modules.lowcode import tasks


def test_task_names_registered():
    assert tasks.form_inventory_snapshot.name == "lowcode.form_inventory_snapshot"
    assert tasks.published_version_guard.name == "lowcode.published_version_guard"
    assert tasks.draft_aging_report.name == "lowcode.draft_aging_report"
