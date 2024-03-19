from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete, \
    Graph, Node
from enum import Enum, auto


class SPPHeuristics(SPPConcrete):
    """
    ============================================================================
     One-to-One Shortest-Path-Problem with Heuristics.
    ============================================================================
    """

    class Heuristic(Enum):
        """
        ========================================================================
         Enum for different Heuristic-Functions that the class enables.
        ========================================================================
        """
        MANHATTAN_DISTANCE = auto()

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node,
                 h_func: Heuristic = Heuristic.MANHATTAN_DISTANCE) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SPPConcrete.__init__(self, graph=graph, start=start, goal=goal)
        self._h_func = h_func

    @property
    def h_func(self) -> Heuristic:
        return self._h_func

    def calc_h(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristic-Distance from the given Node to the Goal.
        ========================================================================
        """
        if self._h_func == self.Heuristic.MANHATTAN_DISTANCE:
            return node.distance(other=self.goal)
