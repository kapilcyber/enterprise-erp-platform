"""Tool allow-list engine — validate published tool version bindings (pure)."""

from uuid import UUID

from modules.ai.domain.enums import ToolVersionStatus
from modules.ai.domain.exceptions import ToolAllowListViolation


class ToolAllowListEngine:
    def validate_tool_version_ids(
        self,
        tool_version_ids: list[UUID],
        *,
        published_lookup: dict[UUID, object],
    ) -> None:
        """Ensure every referenced tool version exists and is published."""
        if not tool_version_ids:
            return
        missing: list[str] = []
        not_published: list[str] = []
        for tv_id in tool_version_ids:
            row = published_lookup.get(tv_id)
            if row is None:
                missing.append(str(tv_id))
            elif getattr(row, "status", None) != ToolVersionStatus.PUBLISHED.value:
                not_published.append(str(tv_id))
        if missing or not_published:
            parts: list[str] = []
            if missing:
                parts.append(f"not found: {', '.join(missing)}")
            if not_published:
                parts.append(f"not published: {', '.join(not_published)}")
            raise ToolAllowListViolation("; ".join(parts))

    def validate_allow_list(
        self,
        tool_version_ids: list[UUID],
        *,
        published_lookup: dict[UUID, object],
    ) -> dict:
        """Non-throwing validation for publish gates."""
        issues: list[dict] = []
        for tv_id in tool_version_ids:
            row = published_lookup.get(tv_id)
            if row is None:
                issues.append(
                    {"code": "TOOL_VERSION_NOT_FOUND", "tool_version_id": str(tv_id)}
                )
            elif getattr(row, "status", None) != ToolVersionStatus.PUBLISHED.value:
                issues.append(
                    {"code": "TOOL_VERSION_NOT_PUBLISHED", "tool_version_id": str(tv_id)}
                )
        return {"valid": len(issues) == 0, "issues": issues}
