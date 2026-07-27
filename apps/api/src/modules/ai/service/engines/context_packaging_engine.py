"""Context packaging engine — assemble context dict from package fields (UUID refs only)."""

import json
from uuid import UUID


class ContextPackagingEngine:
    def assemble(self, package) -> dict:
        refs: dict[str, str | None] = {
            "session_id": str(package.session_id),
            "prompt_version_id": (
                str(package.prompt_version_id) if package.prompt_version_id else None
            ),
            "module_code": package.module_code,
            "entity_id": str(package.entity_id) if package.entity_id else None,
            "lowcode_form_id": (
                str(package.lowcode_form_id) if package.lowcode_form_id else None
            ),
            "bpm_task_id": str(package.bpm_task_id) if package.bpm_task_id else None,
            "document_id": str(package.document_id) if package.document_id else None,
        }
        context_data: dict | list | str | None = None
        if package.context_json:
            try:
                context_data = json.loads(package.context_json)
            except json.JSONDecodeError:
                context_data = package.context_json
        return {
            "package_id": str(package.id),
            "package_code": package.package_code,
            "status": package.status,
            "refs": refs,
            "context": context_data,
        }

    @staticmethod
    def uuid_ref(value: UUID | None) -> str | None:
        return str(value) if value else None
