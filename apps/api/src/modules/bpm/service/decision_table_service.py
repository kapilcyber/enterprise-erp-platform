"""DecisionTableService — Phase 2B."""

from __future__ import annotations

import json
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, DecisionTableStatus
from modules.bpm.domain.exceptions import InvalidDecisionTableState
from modules.bpm.models import BpmDecisionTable
from modules.bpm.repository.decision_table_repository import DecisionTableRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import DecisionTableEngine, WorkflowVersionEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class DecisionTableService:
    def __init__(self, db: Session) -> None:
        self._repo = DecisionTableRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = DecisionTableEngine()
        self._version_engine = WorkflowVersionEngine()
        self._audit = AuditService(db)

    def _require_editable_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        self._version_engine.assert_editable(version)
        return version

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmDecisionTable:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Decision table not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        version_id: UUID,
        *,
        company_id: UUID | None = None,
        **fields,
    ):
        version = self._require_editable_version(ctx, version_id)
        rows_json = fields.get("rows_json")
        self._engine.assert_rows_json(rows_json)
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("table_code", None) or self._numbers.generate(
            BpmEntityType.DECISION_TABLE, cid, BpmDecisionTable, "table_code"
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = DecisionTableStatus.ENABLED.value
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            table_code=code,
            **fields,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_decision_table",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        if "rows_json" in fields and fields["rows_json"] is not None:
            self._engine.assert_rows_json(fields["rows_json"])
        if (
            "status" in fields
            and fields["status"] is not None
            and fields["status"]
            not in (
                DecisionTableStatus.ENABLED.value,
                DecisionTableStatus.DISABLED.value,
            )
        ):
            raise InvalidDecisionTableState(f"Unsupported status: {fields['status']}")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Decision table not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_decision_table",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def enable(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        self._engine.enable(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def disable(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        self._engine.disable(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def replace_rows(self, ctx: TenantContext, row_id: UUID, rows: list[dict]):
        """Replace full decision-table row set (draft versions only)."""
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        if not isinstance(rows, list):
            raise InvalidDecisionTableState("rows must be a list")
        normalized = []
        for i, item in enumerate(rows):
            if not isinstance(item, dict):
                raise InvalidDecisionTableState(f"Row {i} must be an object")
            entry = dict(item)
            entry.setdefault("row_id", str(uuid4()))
            entry.setdefault("priority", i)
            normalized.append(entry)
        payload = json.dumps(normalized)
        self._engine.assert_rows_json(payload)
        return self.update(ctx, row_id, rows_json=payload)

    def add_row(self, ctx: TenantContext, row_id: UUID, row_payload: dict):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        rows = self._parse_rows(row.rows_json)
        entry = dict(row_payload)
        entry.setdefault("row_id", str(uuid4()))
        entry.setdefault("priority", len(rows))
        rows.append(entry)
        return self.update(ctx, row_id, rows_json=json.dumps(rows))

    def update_row(self, ctx: TenantContext, row_id: UUID, decision_row_id: str, row_payload: dict):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        rows = self._parse_rows(row.rows_json)
        found = False
        for i, existing in enumerate(rows):
            if str(existing.get("row_id")) == str(decision_row_id):
                merged = dict(existing)
                merged.update(row_payload)
                merged["row_id"] = decision_row_id
                rows[i] = merged
                found = True
                break
        if not found:
            raise NotFoundException("Decision table row not found")
        return self.update(ctx, row_id, rows_json=json.dumps(rows))

    def remove_row(self, ctx: TenantContext, row_id: UUID, decision_row_id: str):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        rows = self._parse_rows(row.rows_json)
        new_rows = [r for r in rows if str(r.get("row_id")) != str(decision_row_id)]
        if len(new_rows) == len(rows):
            raise NotFoundException("Decision table row not found")
        return self.update(ctx, row_id, rows_json=json.dumps(new_rows))

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_editable_version(ctx, row.version_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Decision table not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_decision_table",
            entity_id=deleted.id,
            operation="delete",
            performed_by=ctx.user_id,
        )
        return deleted

    @staticmethod
    def _parse_rows(rows_json: str | None) -> list[dict]:
        if not rows_json:
            return []
        try:
            data = json.loads(rows_json)
        except json.JSONDecodeError as exc:
            raise InvalidDecisionTableState(f"Invalid rows_json: {exc}") from exc
        if not isinstance(data, list):
            raise InvalidDecisionTableState("rows_json must be a JSON array")
        return data
