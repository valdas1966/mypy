from f_data_structure.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


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
