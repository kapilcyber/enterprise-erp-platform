"""BPM Celery task unit tests — Phase 1."""

from modules.bpm.tasks import (
    definition_inventory_snapshot,
    draft_aging_report,
    published_version_guard,
)


def test_task_names():
    assert definition_inventory_snapshot.name == "bpm.definition_inventory_snapshot"
    assert published_version_guard.name == "bpm.published_version_guard"
    assert draft_aging_report.name == "bpm.draft_aging_report"
