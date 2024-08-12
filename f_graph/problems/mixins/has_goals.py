from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class HasGoals(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Graph-Problems with single Goal-Node.
    ============================================================================
    """

    def __init__(self, goals: set[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goals = goals

    @property
    def goals(self) -> set[Node]:
        return self._goals
