from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete, \
    Graph, Node


class SPPHeuristics(SPPConcrete):
    """
    ============================================================================
     One-to-One Shortest-Path-Problem with Heuristics.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node,
                 h_func: str = 'MANHATTAN_DISTANCE') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SPPConcrete.__init__(self, graph=graph, start=start, goal=goal)
        self._h_func = h_func

    @property
    def h_func(self) -> str:
        return self._h_func

    def calc_h(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristic-Distance from the given Node to the Goal.
        ========================================================================
        """
        return self._get_calc_h(node=node)

    def _get_calc_h(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristic-Function to Calculate by the Mapping.
        ========================================================================
        """
        h_funcs = {'MANHATTAN_DISTANCE': self._manhattan_distance}
        return h_funcs[self._h_func](node=node)

    def _manhattan_distance(self, node: Node) -> int:
        """
        ========================================================================
         Return Manhattan-Distance from Node to Goal.
        ========================================================================
        """
        return node.distance(other=self.goal)
