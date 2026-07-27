"""Cost record engine — append-only validate (no-op)."""


class CostRecordEngine:
    def validate_append(self, row) -> None:
        """Append-only cost telemetry; no lifecycle transitions in Phase 1."""
        _ = row
