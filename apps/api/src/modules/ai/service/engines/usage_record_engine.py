"""Usage record engine — append-only validate (no-op)."""


class UsageRecordEngine:
    def validate_append(self, row) -> None:
        """Append-only telemetry; no lifecycle transitions in Phase 1."""
        _ = row
