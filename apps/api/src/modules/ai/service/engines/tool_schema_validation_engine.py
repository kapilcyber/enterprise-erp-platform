"""Tool schema validation engine — input_schema_json structure stub."""

import json


class ToolSchemaValidationEngine:
    def validate_input_schema(self, input_schema_json: str) -> dict:
        issues: list[dict] = []
        if not input_schema_json or not input_schema_json.strip():
            issues.append({"code": "INPUT_SCHEMA_EMPTY", "field": "input_schema_json"})
            return {"valid": False, "issues": issues, "schema_mode": "metadata_stub"}
        try:
            parsed = json.loads(input_schema_json)
        except json.JSONDecodeError as exc:
            issues.append(
                {
                    "code": "INPUT_SCHEMA_INVALID_JSON",
                    "field": "input_schema_json",
                    "message": str(exc),
                }
            )
            return {"valid": False, "issues": issues, "schema_mode": "metadata_stub"}
        if not isinstance(parsed, dict):
            issues.append(
                {"code": "INPUT_SCHEMA_NOT_OBJECT", "field": "input_schema_json"}
            )
        return {"valid": len(issues) == 0, "issues": issues, "schema_mode": "metadata_stub"}
