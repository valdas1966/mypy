from f_heuristic_search.problem_types.spp_lookup import SPPLookup, Node
from f_heuristic_search.algos.spp.a_star import AStar


class AStarLookup(AStar[Node]):
    """
    ============================================================================
     AStar with Lookup-Table (Accurate distances from Nodes to Goal).
    ============================================================================
    """

    def __init__(self, spp: SPPLookup) -> None:
        AStar.__init__(self, spp=spp)

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Search-Process can be Terminated.
        ========================================================================
        """
        return AStar._can_terminate(self) or self._best in self.spp.lookup

    def _calc_heuristics(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristic-Distance from the Node to the Goal.
        ========================================================================
        """
        if node in self.spp.lookup:
            return sum(n.w for n in self.spp.lookup[node])
        return AStar._calc_heuristics(self, node)
