from f_heuristic_search.algos.spp.strategy.termination.i_1_goal import TerminationGoal
from f_heuristic_search.algos.spp.node import Node


class TerminationLookup(TerminationGoal):
    """
    ============================================================================
     Strategy for Search-Termination using a Lookup-Table.
    ============================================================================
    """

    def __init__(self,
                 goal: Node,
                 lookup: dict[Node, int]) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        TerminationGoal.__init__(self, goal=goal)
        self._lookup = lookup

    def can_terminate(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Node is the Goal or in the Lookup-Table.
        ========================================================================
        """
        return TerminationGoal.can_terminate(node=node) or node in self._lookup
