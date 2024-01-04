from f_heuristic_search.problem_types.spp import SPP, Graph, Node


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
                 heuristics: dict[Node, int] = dict(),
                 lookup: dict[Node, list[Node]] = dict()) -> None:
        SPP.__init__(self, graph, start, goal, heuristics)
        self._lookup = lookup

    @property
    # Accurate Distance from SPP-Nodes to the Goal
    def lookup(self) -> dict[Node, int]:
        return self._lookup
