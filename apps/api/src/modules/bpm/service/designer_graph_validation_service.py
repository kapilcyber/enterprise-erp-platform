"""Designer graph validation — Phase 2A (design-time only)."""

from collections import defaultdict, deque
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import DesignerNodeType
from modules.bpm.domain.value_objects import GraphValidationResult, ValidationIssue
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.designer_transition_repository import DesignerTransitionRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.foundation.domain.value_objects import TenantContext


class DesignerGraphValidationService:
    def __init__(self, db: Session) -> None:
        self._versions = WorkflowVersionRepository(db)
        self._nodes = DesignerNodeRepository(db)
        self._transitions = DesignerTransitionRepository(db)

    def validate(
        self,
        ctx: TenantContext,
        version_id: UUID,
        *,
        allow_cycles: bool = False,
    ) -> GraphValidationResult:
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")

        nodes = self._nodes.list_by_version(ctx, version_id)
        transitions = self._transitions.list_by_version(ctx, version_id)
        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []

        starts = [n for n in nodes if n.node_type == DesignerNodeType.START.value]
        ends = [n for n in nodes if n.node_type == DesignerNodeType.END.value]

        if len(starts) != 1:
            issues.append(
                ValidationIssue(
                    code="START_NODE_COUNT",
                    message=f"Exactly one Start Node required (found {len(starts)})",
                    field="node_type",
                )
            )
        if len(ends) < 1:
            issues.append(
                ValidationIssue(
                    code="END_NODE_MISSING",
                    message="At least one End Node is required",
                    field="node_type",
                )
            )

        node_ids = {n.id for n in nodes}
        adjacency: dict[UUID, list[UUID]] = defaultdict(list)
        reverse_adj: dict[UUID, list[UUID]] = defaultdict(list)

        for t in transitions:
            if t.from_node_id not in node_ids or t.to_node_id not in node_ids:
                issues.append(
                    ValidationIssue(
                        code="TRANSITION_NODE_MISSING",
                        message=f"Transition {t.transition_code} references missing node(s)",
                        field="from_node_id",
                    )
                )
                continue
            if t.from_node_id == t.to_node_id:
                warnings.append(
                    ValidationIssue(
                        code="SELF_LOOP",
                        message=f"Transition {t.transition_code} is a self-loop",
                        severity="warning",
                        field="to_node_id",
                    )
                )
            adjacency[t.from_node_id].append(t.to_node_id)
            reverse_adj[t.to_node_id].append(t.from_node_id)

        # Duplicate edges already constrained by UK; still report soft check
        seen_edges: set[tuple[UUID, UUID]] = set()
        for t in transitions:
            edge = (t.from_node_id, t.to_node_id)
            if edge in seen_edges:
                issues.append(
                    ValidationIssue(
                        code="DUPLICATE_TRANSITION",
                        message=f"Duplicate transition {t.from_node_id} -> {t.to_node_id}",
                        field="from_node_id",
                    )
                )
            seen_edges.add(edge)

        # Orphan detection: node with no inbound and no outbound (except sole start/end edge cases)
        for n in nodes:
            out_deg = len(adjacency.get(n.id, []))
            in_deg = len(reverse_adj.get(n.id, []))
            if out_deg == 0 and in_deg == 0 and n.node_type not in {
                DesignerNodeType.START.value,
                DesignerNodeType.END.value,
            }:
                issues.append(
                    ValidationIssue(
                        code="ORPHAN_NODE",
                        message=f"Orphan node {n.node_code}",
                        field="node_code",
                    )
                )
            elif out_deg == 0 and in_deg == 0 and len(nodes) > 1:
                issues.append(
                    ValidationIssue(
                        code="ORPHAN_NODE",
                        message=f"Disconnected node {n.node_code}",
                        field="node_code",
                    )
                )

        # Reachability from start (if exactly one start)
        if len(starts) == 1 and nodes:
            start_id = starts[0].id
            visited: set[UUID] = set()
            q: deque[UUID] = deque([start_id])
            while q:
                cur = q.popleft()
                if cur in visited:
                    continue
                visited.add(cur)
                for nxt in adjacency.get(cur, []):
                    if nxt not in visited:
                        q.append(nxt)
            unreachable = [n for n in nodes if n.id not in visited]
            for n in unreachable:
                issues.append(
                    ValidationIssue(
                        code="UNREACHABLE_NODE",
                        message=f"Node {n.node_code} unreachable from Start",
                        field="node_code",
                    )
                )

        # Cycle detection
        if not allow_cycles and nodes:
            cycle = self._find_cycle(node_ids, adjacency)
            if cycle:
                issues.append(
                    ValidationIssue(
                        code="CIRCULAR_TRANSITION",
                        message="Circular transition detected (set allow_cycles to permit)",
                        field="transition",
                    )
                )

        return GraphValidationResult(
            valid=len(issues) == 0,
            version_id=version_id,
            issues=issues,
            warnings=warnings,
            node_count=len(nodes),
            transition_count=len(transitions),
            start_count=len(starts),
            end_count=len(ends),
        )

    @staticmethod
    def _find_cycle(node_ids: set[UUID], adjacency: dict[UUID, list[UUID]]) -> bool:
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {n: WHITE for n in node_ids}

        def dfs(u: UUID) -> bool:
            color[u] = GRAY
            for v in adjacency.get(u, []):
                if v not in color:
                    continue
                if color[v] == GRAY:
                    return True
                if color[v] == WHITE and dfs(v):
                    return True
            color[u] = BLACK
            return False

        return any(color[n] == WHITE and dfs(n) for n in node_ids)
