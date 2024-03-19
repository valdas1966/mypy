from f_heuristic_search.problem_types.spp.i_0_concrete import SPP, Graph, Node


class SPPLookup(SPP):
    """
    ============================================================================
     Shortest-Path-Problem in Heuristic Search with a Lookup property.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node,
                 heuristics: dict[Node, int] = None,
                 lookup: dict[Node, list[Node]] = None) -> None:
        SPP.__init__(self, graph, start, goal, heuristics)
        self._lookup = lookup or dict()

    def heuristics(self, node: Node) -> int:
        """
        ========================================================================
         If the given Node is in the Lookup-Table: Return the accurate distance
          to the Goal. Otherwise, return the heuristic-distance to the Goal.
        ========================================================================
        """
        if node in self._lookup:
            return len(self._lookup[node])
        return SPP.heuristics(self, node=node)

    def lookup(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return accurate Distance from the given Node to the Goal.
        ========================================================================
        """
        return self._lookup[node]
