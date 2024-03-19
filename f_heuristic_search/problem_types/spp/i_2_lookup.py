from f_heuristic_search.problem_types.spp.i_1_heuristics import \
    SPPHeuristics, Graph, Node


class SPPLookup(SPPHeuristics):
    """
    ============================================================================
     1. One-to-One Shortest-Path-Problem with a Lookup-Table.
     2. The Lookup-Table holds the Optimal-Path from some Node to Goal.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node,
                 h_func: str = 'MANHATTAN_DISTANCE',
                 lookup: dict[Node, tuple[Node, ...]] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SPPHeuristics.__init__(self,
                               graph=graph,
                               start=start,
                               goal=goal,
                               h_func=h_func)
        self._lookup = lookup

    @property
    def lookup(self) -> dict[Node, tuple[Node, ...]]:
        return self._lookup

    def calc_h(self, node: Node) -> int:
        """
        ========================================================================
         If Node in Lookup -> Return accurate distance to Goal.
         Otherwise -> Return heuristic distance to Goal.
        ========================================================================
        """
        if node in self._lookup:
            return len(self._lookup[node])
        return SPPHeuristics.calc_h(node=node)

    def lookup_to_goal(self, node: Node) -> tuple[Node, ...]:
        """
        ========================================================================
         Return Optimal-Path from Node to Goal.
        ========================================================================
        """
        return self._lookup[node]

