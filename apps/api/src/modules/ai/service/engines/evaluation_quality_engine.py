"""Evaluation quality engine — metadata result stub (no inference)."""

from modules.ai.domain.enums import EvaluationStatus


class EvaluationQualityEngine:
    def summarize_metadata(self, *, status: str, metrics_json: str | None = None) -> dict:
        return {
            "quality_mode": "metadata_stub",
            "status": status,
            "has_metrics": bool(metrics_json),
            "valid": status == EvaluationStatus.COMPLETED.value,
        }
