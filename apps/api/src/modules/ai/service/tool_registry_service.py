"""Tool registry service — metadata registry façade (NO execution)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import ToolVersionStatus
from modules.ai.domain.json_bindings import parse_uuid_list
from modules.ai.repository.agent_version_repository import AgentVersionRepository
from modules.ai.repository.tool_repository import ToolRepository
from modules.ai.repository.tool_version_repository import ToolVersionRepository
from modules.foundation.domain.value_objects import TenantContext


class ToolRegistryService:
    """Metadata-only tool registry — agents never access repositories directly."""

    def __init__(self, db: Session) -> None:
        self._agent_versions = AgentVersionRepository(db)
        self._tool_versions = ToolVersionRepository(db)
        self._tools = ToolRepository(db)

    def list_allowed_tools_for_agent_version(
        self, ctx: TenantContext, agent_version_id: UUID
    ) -> dict:
        av = self._agent_versions.get(ctx, agent_version_id)
        if av is None:
            raise NotFoundException("Agent version not found")
        tool_version_ids = parse_uuid_list(av.tool_version_ids_json)
        entries: list[dict] = []
        for tv_id in tool_version_ids:
            tv = self._tool_versions.get(ctx, tv_id)
            if tv is None:
                continue
            tool = self._tools.get(ctx, tv.tool_id)
            entries.append(
                {
                    "tool_version_id": str(tv.id),
                    "tool_id": str(tv.tool_id),
                    "tool_code": tool.tool_code if tool else None,
                    "tool_name": tool.tool_name if tool else None,
                    "version_number": tv.version_number,
                    "version_code": tv.version_code,
                    "status": tv.status,
                    "contract_key": tv.contract_key,
                    "side_effect_class": tool.side_effect_class if tool else None,
                    "published": tv.status == ToolVersionStatus.PUBLISHED.value,
                }
            )
        return {
            "agent_version_id": str(agent_version_id),
            "registry_mode": "metadata_only",
            "tools": entries,
        }

    def resolve_tool_metadata(self, ctx: TenantContext, tool_version_id: UUID) -> dict:
        tv = self._tool_versions.get(ctx, tool_version_id)
        if tv is None:
            raise NotFoundException("Tool version not found")
        tool = self._tools.get(ctx, tv.tool_id)
        return {
            "tool_version_id": str(tv.id),
            "tool_id": str(tv.tool_id),
            "tool_code": tool.tool_code if tool else None,
            "module_code": tool.module_code if tool else None,
            "contract_key": tv.contract_key,
            "input_schema_json": tv.input_schema_json,
            "output_schema_json": tv.output_schema_json,
            "status": tv.status,
            "registry_mode": "metadata_only",
        }
