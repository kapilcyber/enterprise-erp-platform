"""JSON UUID array binding helpers for Phase 3 metadata fields."""

import json
from uuid import UUID


def parse_uuid_list(raw: str | None) -> list[UUID]:
    if not raw or not raw.strip():
        return []
    parsed = json.loads(raw)
    if not isinstance(parsed, list):
        raise ValueError("Expected JSON array of UUID strings")
    return [UUID(str(item)) for item in parsed]


def serialize_uuid_list(ids: list[UUID] | None) -> str:
    if not ids:
        return "[]"
    return json.dumps([str(i) for i in ids])
