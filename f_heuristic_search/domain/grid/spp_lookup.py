from f_heuristic_search.domain.grid.spp import SPP, Graph, Node
from f_heuristic_search.problem_types.spp_lookup import SPPLookup as \
    SPPLookupBase


class SPPLookup(SPP, SPPLookupBase):
    """
    ============================================================================
     Represents the Shortest-Path-Problem with Lookup in the Grid-Domain.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node,
                 lookup: dict[Node, int] = None) -> None:
        SPP.__init__(self, graph, start, goal)
        SPPLookupBase.__init__(self, graph, start, goal, lookup=lookup)

    def heuristics(self, node: Node) -> int:
        """
        ========================================================================
         If the given Node is in the Lookup-Table: Return the accurate distance
          to the Goal. Otherwise, return the heuristic-distance to the Goal.
        ========================================================================
        """
        if node in self._lookup:
            return len(self.lookup(node=node))
        return SPP.heuristics(self, node=node)
