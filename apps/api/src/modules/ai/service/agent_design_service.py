"""Agent design service — design-time metadata only (NO execution)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.adapters.bpm_port import AiBpmAdapter
from modules.ai.domain.json_bindings import parse_uuid_list
from modules.ai.repository.agent_repository import AgentRepository
from modules.ai.repository.agent_version_repository import AgentVersionRepository
from modules.ai.repository.skill_repository import SkillRepository
from modules.ai.service.engines import AgentOrchestrationLimitsEngine
from modules.ai.service.publish_validation_service import PublishValidationService
from modules.ai.service.tool_registry_service import ToolRegistryService
from modules.foundation.domain.value_objects import TenantContext


class AgentDesignService:
    """Design-time metadata aggregation — no runtime orchestration."""

    def __init__(self, db: Session) -> None:
        self._agents = AgentRepository(db)
        self._agent_versions = AgentVersionRepository(db)
        self._skills = SkillRepository(db)
        self._tool_registry = ToolRegistryService(db)
        self._bpm = AiBpmAdapter(db)
        self._limits_engine = AgentOrchestrationLimitsEngine()
        self._publish_validator = PublishValidationService(db)

    def get_design_snapshot(self, ctx: TenantContext, agent_version_id: UUID) -> dict:
        av = self._agent_versions.get(ctx, agent_version_id)
        if av is None:
            raise NotFoundException("Agent version not found")
        agent = self._agents.get(ctx, av.agent_id)
        skill_ids = parse_uuid_list(av.skill_ids_json)
        skills: list[dict] = []
        for sid in skill_ids:
            skill = self._skills.get(ctx, sid)
            if skill:
                skills.append(
                    {
                        "skill_id": str(skill.id),
                        "skill_code": skill.skill_code,
                        "skill_name": skill.skill_name,
                        "status": skill.status,
                    }
                )
        tool_registry = self._tool_registry.list_allowed_tools_for_agent_version(
            ctx, agent_version_id
        )
        limits = self._limits_engine.validate(
            max_steps=av.max_steps, max_tokens=av.max_tokens
        )
        return {
            "design_mode": "metadata_only",
            "agent_id": str(av.agent_id),
            "agent_code": agent.agent_code if agent else None,
            "agent_name": agent.agent_name if agent else None,
            "agent_version_id": str(av.id),
            "version_number": av.version_number,
            "version_code": av.version_code,
            "status": av.status,
            "prompt_version_id": str(av.prompt_version_id),
            "skills": skills,
            "tools": tool_registry["tools"],
            "knowledge_base_id": str(av.knowledge_base_id) if av.knowledge_base_id else None,
            "bpm_definition_id": str(
                self._bpm.resolve_bpm_definition_ref(ctx, av.bpm_definition_id)
            )
            if av.bpm_definition_id
            else None,
            "orchestration_limits": limits,
            "max_steps": av.max_steps,
            "max_tokens": av.max_tokens,
        }

    def validate_design(self, ctx: TenantContext, agent_version_id: UUID) -> dict:
        result = self._publish_validator.validate_agent_version(ctx, agent_version_id)
        payload = result.to_dict() if hasattr(result, "to_dict") else {
            "valid": result.valid,
            "issues": [{"code": i.code, "message": i.message} for i in result.issues],
        }
        payload["design_mode"] = "metadata_only"
        return payload
