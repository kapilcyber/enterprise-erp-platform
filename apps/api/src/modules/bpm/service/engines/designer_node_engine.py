"""Designer node lifecycle engine — Phase 2A."""

from modules.bpm.domain.enums import NODE_TYPE_VALUES, DesignerNodeStatus, DesignerNodeType
from modules.bpm.domain.exceptions import InvalidDesignerNodeState


class DesignerNodeEngine:
    def assert_valid_type(self, node_type: str | None) -> None:
        if not node_type or node_type not in NODE_TYPE_VALUES:
            raise InvalidDesignerNodeState(f"Unsupported node type: {node_type}")

    def activate(self, row) -> None:
        if row.status == DesignerNodeStatus.ACTIVE.value:
            raise InvalidDesignerNodeState("Node already active")
        row.status = DesignerNodeStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status != DesignerNodeStatus.ACTIVE.value:
            raise InvalidDesignerNodeState("Only active nodes can be deactivated")
        if row.node_type == DesignerNodeType.START.value:
            raise InvalidDesignerNodeState("Start node cannot be deactivated while present")
        row.status = DesignerNodeStatus.INACTIVE.value
