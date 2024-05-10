from f_hs.problems.path.base import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)

class HasGoal(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Path-Finding-Problems with a single Goal-Node.
     ===========================================================================
    """

    def __init__(self, goal: Node) -> None:
        self._goal = goal

    @property
    def goal(self) -> Node:
        return self._goal
