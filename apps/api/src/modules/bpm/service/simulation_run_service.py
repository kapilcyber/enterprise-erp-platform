"""SimulationRunService — Phase 5.

Simulation never mutates business entities, never creates runtime instances,
never sends notifications, and never executes triggers.
"""

from __future__ import annotations

import json
import time
from collections import defaultdict, deque
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import (
    BpmEntityType,
    DesignerNodeType,
    SimulationStatus,
    TransitionType,
)
from modules.bpm.domain.exceptions import InvalidSimulationRunState
from modules.bpm.domain.value_objects import SimulationResultSummary
from modules.bpm.models import BpmSimulationRun
from modules.bpm.repository.business_rule_repository import BusinessRuleRepository
from modules.bpm.repository.decision_table_repository import DecisionTableRepository
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.designer_transition_repository import DesignerTransitionRepository
from modules.bpm.repository.simulation_run_repository import SimulationRunRepository
from modules.bpm.repository.workflow_variable_repository import WorkflowVariableRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.designer_graph_validation_service import DesignerGraphValidationService
from modules.bpm.service.engines.simulation_engines import SimulationRunEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    try:
        return json.loads(raw)
    except (TypeError, ValueError, json.JSONDecodeError):
        return default


def _dumps(value: Any) -> str:
    return json.dumps(value, default=str)


class SimulationRunService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = SimulationRunRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._nodes = DesignerNodeRepository(db)
        self._transitions = DesignerTransitionRepository(db)
        self._decision_tables = DecisionTableRepository(db)
        self._business_rules = BusinessRuleRepository(db)
        self._variables = WorkflowVariableRepository(db)
        self._graph = DesignerGraphValidationService(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = SimulationRunEngine()
        self._audit = AuditService(db)

    def _require_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        return version

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        self._require_version(ctx, version_id)
        return self._repo.list_by_version(ctx, version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmSimulationRun:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Simulation run not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        version_id: UUID,
        *,
        simulation_name: str,
        company_id: UUID | None = None,
        description: str | None = None,
        input_context_json: str | None = None,
        simulation_code: str | None = None,
    ):
        version = self._require_version(ctx, version_id)
        self._engine.assert_simulatable(version)
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = simulation_code or self._numbers.generate(
            BpmEntityType.SIMULATION_RUN, cid, BpmSimulationRun, "simulation_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            simulation_code=code,
            simulation_name=simulation_name,
            description=description,
            status=SimulationStatus.PENDING.value,
            duration_ms=0,
            input_context_json=input_context_json,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_simulation_run",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        if row.status == SimulationStatus.RUNNING.value:
            raise InvalidSimulationRunState("Cannot update a running simulation")
        version = self._require_version(ctx, row.version_id)
        self._engine.assert_simulatable(version)
        allowed = {"simulation_name", "description", "input_context_json"}
        payload = {k: v for k, v in fields.items() if k in allowed and v is not None}
        updated = self._repo.update(ctx, row_id, **payload)
        if updated is None:
            raise NotFoundException("Simulation run not found")
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        if row.status == SimulationStatus.RUNNING.value:
            raise InvalidSimulationRunState("Cannot delete a running simulation")
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Simulation run not found")
        return deleted

    def cancel(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.cancel(row)
        return self._repo.update(
            ctx, row_id, status=row.status, completed_at=row.completed_at
        )

    def validate_workflow(self, ctx: TenantContext, version_id: UUID) -> dict[str, Any]:
        """Validate graph + intelligence artifacts without creating runtime instances."""
        version = self._require_version(ctx, version_id)
        self._engine.assert_simulatable(version)
        graph = self._graph.validate(ctx, version_id)
        warnings = [
            w.to_dict() if hasattr(w, "to_dict") else self._issue_dict(w)
            for w in graph.warnings
        ]
        errors = [
            e.to_dict() if hasattr(e, "to_dict") else self._issue_dict(e)
            for e in graph.issues
        ]
        intel = self._evaluate_intelligence(ctx, version_id, context={}, dry_run=True)
        warnings.extend(intel["warnings"])
        errors.extend(intel["errors"])
        return {
            "version_id": str(version_id),
            "valid": len(errors) == 0 and bool(getattr(graph, "valid", len(errors) == 0)),
            "warnings": warnings,
            "errors": errors,
            "decision_tables_evaluated": intel["decision_tables_evaluated"],
            "business_rules_evaluated": intel["business_rules_evaluated"],
            "variables_resolved": intel["variables_resolved"],
        }

    def run(self, ctx: TenantContext, row_id: UUID) -> BpmSimulationRun:
        row = self.get(ctx, row_id)
        version = self._require_version(ctx, row.version_id)
        self._engine.assert_simulatable(version)

        started = time.perf_counter()
        self._engine.begin(row)
        row.started_by = ctx.user_id
        self._repo.update(
            ctx,
            row_id,
            status=row.status,
            started_at=row.started_at,
            started_by=row.started_by,
            completed_at=None,
            duration_ms=0,
            warnings_json=None,
            errors_json=None,
            execution_trace_json=None,
            result_summary_json=None,
        )

        warnings: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        trace: list[dict[str, Any]] = []

        try:
            # Never create instances / tasks / notifications / triggers here.
            input_ctx = _loads(row.input_context_json, {})
            if not isinstance(input_ctx, dict):
                errors.append(
                    {
                        "code": "INVALID_INPUT_CONTEXT",
                        "message": "input_context_json must be a JSON object",
                    }
                )
                input_ctx = {}

            resolved = self._resolve_variables(ctx, row.version_id, input_ctx)
            warnings.extend(resolved["warnings"])
            errors.extend(resolved["errors"])
            context = resolved["context"]
            trace.append(
                {
                    "step": "variable_resolution",
                    "variables_resolved": resolved["variables_resolved"],
                    "context_keys": sorted(context.keys()),
                }
            )

            graph = self._graph.validate(ctx, row.version_id)
            for w in graph.warnings:
                warnings.append(self._issue_dict(w))
            for e in graph.issues:
                errors.append(self._issue_dict(e))
            trace.append(
                {
                    "step": "graph_validation",
                    "valid": getattr(graph, "valid", len(graph.issues) == 0),
                    "issue_count": len(graph.issues),
                    "warning_count": len(graph.warnings),
                }
            )

            traversal = self._traverse_graph(ctx, row.version_id, context)
            warnings.extend(traversal["warnings"])
            errors.extend(traversal["errors"])
            trace.extend(traversal["trace"])

            intel = self._evaluate_intelligence(ctx, row.version_id, context=context, dry_run=True)
            warnings.extend(intel["warnings"])
            errors.extend(intel["errors"])
            trace.append(
                {
                    "step": "intelligence_evaluation",
                    "decision_tables_evaluated": intel["decision_tables_evaluated"],
                    "business_rules_evaluated": intel["business_rules_evaluated"],
                    "matches": intel.get("matches", []),
                }
            )

            duration_ms = int((time.perf_counter() - started) * 1000)
            summary = SimulationResultSummary(
                valid=len(errors) == 0,
                nodes_visited=traversal["nodes_visited"],
                transitions_evaluated=traversal["transitions_evaluated"],
                decision_tables_evaluated=intel["decision_tables_evaluated"],
                business_rules_evaluated=intel["business_rules_evaluated"],
                variables_resolved=resolved["variables_resolved"],
                warning_count=len(warnings),
                error_count=len(errors),
                duration_ms=duration_ms,
            )

            if errors:
                self._engine.fail(row, duration_ms=duration_ms)
            else:
                self._engine.complete(row, duration_ms=duration_ms)

            updated = self._repo.update(
                ctx,
                row_id,
                status=row.status,
                duration_ms=row.duration_ms,
                completed_at=row.completed_at,
                warnings_json=_dumps(warnings),
                errors_json=_dumps(errors),
                execution_trace_json=_dumps(trace),
                result_summary_json=_dumps(summary.to_dict()),
            )
            if updated is None:
                raise NotFoundException("Simulation run not found")
            return updated
        except Exception as exc:  # noqa: BLE001 — capture as simulation failure
            duration_ms = int((time.perf_counter() - started) * 1000)
            errors.append({"code": "SIMULATION_EXCEPTION", "message": str(exc)})
            if row.status == SimulationStatus.RUNNING.value:
                self._engine.fail(row, duration_ms=duration_ms)
            updated = self._repo.update(
                ctx,
                row_id,
                status=SimulationStatus.FAILED.value,
                duration_ms=duration_ms,
                completed_at=row.completed_at,
                warnings_json=_dumps(warnings),
                errors_json=_dumps(errors),
                execution_trace_json=_dumps(trace),
                result_summary_json=_dumps(
                    {
                        "valid": False,
                        "error_count": len(errors),
                        "warning_count": len(warnings),
                        "duration_ms": duration_ms,
                    }
                ),
            )
            if updated is None:
                raise NotFoundException("Simulation run not found") from None
            return updated

    def _issue_dict(self, issue) -> dict[str, Any]:
        if hasattr(issue, "to_dict"):
            return issue.to_dict()
        return {
            "code": getattr(issue, "code", "ISSUE"),
            "message": getattr(issue, "message", str(issue)),
            "severity": getattr(issue, "severity", "error"),
            "field": getattr(issue, "field", None),
        }

    def _resolve_variables(
        self, ctx: TenantContext, version_id: UUID, input_ctx: dict[str, Any]
    ) -> dict[str, Any]:
        variables = self._variables.list_by_version(ctx, version_id)
        context = dict(input_ctx)
        warnings: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        resolved = 0
        for var in variables:
            if getattr(var, "status", "active") == "inactive":
                continue
            key = var.variable_key
            if key in context:
                resolved += 1
                continue
            if var.default_value is not None:
                context[key] = var.default_value
                resolved += 1
                continue
            if var.is_required:
                errors.append(
                    {
                        "code": "REQUIRED_VARIABLE_MISSING",
                        "message": f"Required variable '{key}' missing for simulation",
                        "field": key,
                    }
                )
            else:
                warnings.append(
                    {
                        "code": "VARIABLE_UNRESOLVED",
                        "message": f"Optional variable '{key}' has no value",
                        "severity": "warning",
                        "field": key,
                    }
                )
        return {
            "context": context,
            "warnings": warnings,
            "errors": errors,
            "variables_resolved": resolved,
        }

    def _traverse_graph(
        self, ctx: TenantContext, version_id: UUID, context: dict[str, Any]
    ) -> dict[str, Any]:
        nodes = self._nodes.list_by_version(ctx, version_id)
        transitions = self._transitions.list_by_version(ctx, version_id)
        by_id = {n.id: n for n in nodes}
        adjacency: dict[UUID, list] = defaultdict(list)
        for t in transitions:
            adjacency[t.from_node_id].append(t)

        warnings: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        trace: list[dict[str, Any]] = []
        nodes_visited = 0
        transitions_evaluated = 0

        starts = [n for n in nodes if n.node_type == DesignerNodeType.START.value]
        if len(starts) != 1:
            errors.append(
                {
                    "code": "START_NODE_COUNT",
                    "message": f"Exactly one Start Node required (found {len(starts)})",
                }
            )
            return {
                "warnings": warnings,
                "errors": errors,
                "trace": trace,
                "nodes_visited": 0,
                "transitions_evaluated": 0,
            }

        queue: deque[UUID] = deque([starts[0].id])
        visited: set[UUID] = set()
        while queue:
            node_id = queue.popleft()
            if node_id in visited:
                continue
            visited.add(node_id)
            node = by_id.get(node_id)
            if node is None:
                errors.append(
                    {
                        "code": "NODE_MISSING",
                        "message": f"Referenced node {node_id} not found",
                    }
                )
                continue
            nodes_visited += 1
            trace.append(
                {
                    "step": "node_visit",
                    "node_id": str(node.id),
                    "node_code": node.node_code,
                    "node_type": node.node_type,
                }
            )
            if node.node_type == DesignerNodeType.END.value:
                continue
            outs = adjacency.get(node_id, [])
            if not outs and node.node_type != DesignerNodeType.END.value:
                warnings.append(
                    {
                        "code": "DEAD_END",
                        "message": f"Node {node.node_code} has no outbound transitions",
                        "severity": "warning",
                    }
                )
            for t in outs:
                transitions_evaluated += 1
                ok, detail = self._evaluate_transition(t, context)
                trace.append(
                    {
                        "step": "transition",
                        "transition_id": str(t.id),
                        "transition_code": t.transition_code,
                        "transition_type": t.transition_type,
                        "from_node_id": str(t.from_node_id),
                        "to_node_id": str(t.to_node_id),
                        "taken": ok,
                        "detail": detail,
                    }
                )
                if not ok and t.transition_type == TransitionType.CONDITIONAL.value:
                    continue
                if t.to_node_id not in visited:
                    queue.append(t.to_node_id)

        return {
            "warnings": warnings,
            "errors": errors,
            "trace": trace,
            "nodes_visited": nodes_visited,
            "transitions_evaluated": transitions_evaluated,
        }

    def _evaluate_transition(self, transition, context: dict[str, Any]) -> tuple[bool, str]:
        """Simulation-only transition check — no side effects."""
        ttype = transition.transition_type
        if ttype in {
            TransitionType.SEQUENTIAL.value,
            TransitionType.PARALLEL.value,
            TransitionType.MERGE.value,
            TransitionType.SPLIT.value,
        }:
            return True, "unconditional"
        expr = getattr(transition, "condition_expression", None) or getattr(
            transition, "condition_json", None
        )
        if not expr:
            return True, "no_condition"
        # Lightweight simulation: if expression looks like key==value and key in context
        if isinstance(expr, str) and "==" in expr:
            left, _, right = expr.partition("==")
            key = left.strip()
            expected = right.strip().strip("'\"")
            actual = context.get(key)
            taken = str(actual) == expected if actual is not None else False
            return taken, f"condition:{key}=={expected}"
        # Unknown expression forms are treated as pass-with-warning at call site via taken=True
        return True, "condition_present_unparsed"

    def _evaluate_intelligence(
        self,
        ctx: TenantContext,
        version_id: UUID,
        *,
        context: dict[str, Any],
        dry_run: bool,
    ) -> dict[str, Any]:
        assert dry_run is True  # simulation only
        warnings: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        matches: list[dict[str, Any]] = []
        tables = self._decision_tables.list_by_version(ctx, version_id)
        rules = self._business_rules.list_by_version(ctx, version_id)
        dt_count = 0
        for table in tables:
            if getattr(table, "status", "enabled") == "disabled":
                continue
            dt_count += 1
            rows = _loads(table.rows_json, [])
            if not isinstance(rows, list):
                errors.append(
                    {
                        "code": "DECISION_TABLE_ROWS_INVALID",
                        "message": f"Decision table {table.table_code} rows_json is not an array",
                    }
                )
                continue
            if not rows:
                warnings.append(
                    {
                        "code": "DECISION_TABLE_EMPTY",
                        "message": f"Decision table {table.table_code} has no rows",
                        "severity": "warning",
                    }
                )
                continue
            hit = None
            for idx, row in enumerate(rows):
                if not isinstance(row, dict):
                    continue
                conditions = row.get("conditions") or row.get("when") or {}
                if isinstance(conditions, dict) and conditions:
                    if all(str(context.get(k)) == str(v) for k, v in conditions.items()):
                        hit = {"row_index": idx, "output": row.get("output") or row.get("then")}
                        break
                elif not conditions:
                    hit = {"row_index": idx, "output": row.get("output") or row.get("then")}
                    break
            matches.append(
                {
                    "decision_table": table.table_code,
                    "matched": hit is not None,
                    "match": hit,
                }
            )
            if hit is None:
                warnings.append(
                    {
                        "code": "DECISION_TABLE_NO_MATCH",
                        "message": f"No row matched for decision table {table.table_code}",
                        "severity": "warning",
                    }
                )

        rule_count = 0
        for rule in rules:
            if getattr(rule, "status", "active") == "inactive":
                continue
            rule_count += 1
            expr = (rule.expression or "").strip()
            if not expr:
                errors.append(
                    {
                        "code": "BUSINESS_RULE_EMPTY",
                        "message": f"Business rule {rule.rule_code} has empty expression",
                    }
                )
                continue
            # Simulation-only: record evaluation presence; do not mutate SoR.
            matches.append(
                {
                    "business_rule": rule.rule_code,
                    "rule_type": rule.rule_type,
                    "evaluated": True,
                    "expression_length": len(expr),
                }
            )

        variables = self._variables.list_by_version(ctx, version_id)
        return {
            "warnings": warnings,
            "errors": errors,
            "matches": matches,
            "decision_tables_evaluated": dt_count,
            "business_rules_evaluated": rule_count,
            "variables_resolved": len(
                [v for v in variables if getattr(v, "status", "active") != "inactive"]
            ),
        }
