from f_graph.termination.base import TerminationBase
from f_graph.nodes.i_1_path import NodePath
from typing import TypeVar

Node = TypeVar('Node', bound=NodePath)


class TerminationGoal(TerminationBase):
    """
    ============================================================================
     Termination of Search-Algorithm with single Goal.
    ============================================================================
    """

    def __init__(self, goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goal = goal

    def can(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the received Node is the desired Goal.
        ========================================================================
        """
        return node == self._goal
