"""Graph-driven initial task generation from published designer graph — Phase 5 polish.

Reuses WorkflowTaskService. Does not introduce a duplicate execution engine.
Never writes peer-module ORM rows.
"""

from collections import defaultdict, deque
from uuid import UUID

from sqlalchemy.orm import Session

from modules.bpm.domain.enums import DesignerNodeType, TaskExecutionMode
from modules.bpm.models.designer_node import BpmDesignerNode
from modules.bpm.repository.designer_node_repository import DesignerNodeRepository
from modules.bpm.repository.designer_transition_repository import DesignerTransitionRepository
from modules.bpm.service.workflow_task_service import WorkflowTaskService
from modules.foundation.domain.value_objects import TenantContext

_TASK_NODE_TYPES = {
    DesignerNodeType.USER_TASK.value,
    DesignerNodeType.APPROVAL_TASK.value,
    DesignerNodeType.VALIDATION.value,
}

_PASS_THROUGH = {
    DesignerNodeType.START.value,
    DesignerNodeType.GATEWAY.value,
    DesignerNodeType.PARALLEL_GATEWAY.value,
    DesignerNodeType.EXCLUSIVE_GATEWAY.value,
    DesignerNodeType.INCLUSIVE_GATEWAY.value,
    DesignerNodeType.TIMER.value,
    DesignerNodeType.API.value,
    DesignerNodeType.SUB_WORKFLOW.value,
}


class GraphDrivenTaskGenerationService:
    """Seed runtime tasks from the published designer graph when an instance starts."""

    def __init__(self, db: Session) -> None:
        self._nodes = DesignerNodeRepository(db)
        self._transitions = DesignerTransitionRepository(db)
        self._tasks = WorkflowTaskService(db)

    def generate_initial_tasks(self, ctx: TenantContext, instance) -> list:
        version_id: UUID = instance.version_id
        nodes = self._nodes.list_by_version(ctx, version_id)
        transitions = self._transitions.list_by_version(ctx, version_id)
        if not nodes:
            return []

        by_id = {n.id: n for n in nodes}
        adjacency: dict[UUID, list[UUID]] = defaultdict(list)
        for t in transitions:
            adjacency[t.from_node_id].append(t.to_node_id)

        starts = [n for n in nodes if n.node_type == DesignerNodeType.START.value]
        if len(starts) != 1:
            return []

        # BFS: collect first wave of task nodes reachable through pass-through nodes only.
        queue: deque[tuple[UUID, int]] = deque([(starts[0].id, 0)])
        visited: set[UUID] = set()
        initial: list[tuple[BpmDesignerNode, int]] = []

        while queue:
            node_id, depth = queue.popleft()
            if node_id in visited:
                continue
            visited.add(node_id)
            node = by_id.get(node_id)
            if node is None:
                continue
            if node.node_type in _TASK_NODE_TYPES:
                initial.append((node, depth))
                continue
            if node.node_type == DesignerNodeType.END.value:
                continue
            if node.node_type in _PASS_THROUGH:
                for nxt in adjacency.get(node_id, []):
                    if nxt not in visited:
                        queue.append((nxt, depth + 1))

        created = []
        for seq, (node, depth) in enumerate(initial):
            mode = TaskExecutionMode.SEQUENTIAL.value
            parallel_key = None
            if node.node_type == DesignerNodeType.APPROVAL_TASK.value:
                # Parallel approvals share a group when peers share the same depth.
                peers = [
                    n for n, d in initial if d == depth and n.node_type == node.node_type
                ]
                if len(peers) > 1:
                    mode = TaskExecutionMode.PARALLEL.value
                    parallel_key = f"depth-{depth}"
            task = self._tasks.create(
                ctx,
                instance.id,
                task_name=getattr(node, "node_name", None) or node.node_code,
                company_id=instance.company_id,
                description=getattr(node, "description", None),
                execution_mode=mode,
                parallel_group_key=parallel_key,
                sequence_order=seq,
                node_id=node.id,
                metadata_json=None,
            )
            created.append(task)
        return created
