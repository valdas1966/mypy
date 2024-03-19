from f_data_structure.nodes.i_2_cell import NodeCell
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeCell)


class HasGoal(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Problems with a Goal Node.
    ============================================================================
    """

    def __init__(self, goal: Node) -> None:
        self._goal = goal

    @property
    def goal(self) -> Node:
        return self._goal
