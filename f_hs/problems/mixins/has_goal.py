from f_ds.graphs.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class HasGoal(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Path-Finding-Problems with a single Goal-Node.
     ===========================================================================
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
