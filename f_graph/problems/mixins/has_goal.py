from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class HasGoal(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Graph-Problems with single Goal-Node.
    ============================================================================
    """

    def __init__(self, goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goal = goal

    @property
    def goal(self) -> Node:
        return self._goal
