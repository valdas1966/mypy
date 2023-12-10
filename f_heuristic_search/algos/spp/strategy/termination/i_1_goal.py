from f_heuristic_search.algos.spp.strategy.termination.i_0_base import TerminationBase
from f_heuristic_search.algos.spp.node import Node


class TerminationGoal(TerminationBase):
    """
    ============================================================================
     Strategy for Search-Termination by a Goal-Node.
    ============================================================================
    """

    def __init__(self, goal: Node) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._goal = goal

    def can_terminate(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Node is a Goal-Node.
        ========================================================================
        """
        return node == self._goal
