from f_heuristic_search.problem_types.spp import SPP as SPPBase
from f_heuristic_search.domain.grid.graph import Graph
from f_heuristic_search.nodes.i_3_f_cell import Node


class SPP(SPPBase):
    """
    ============================================================================
     Represents the Shortest-Path-Problem in the Grid-Domain.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node) -> None:
        SPPBase.__init__(self, graph=graph, start=start, goal=goal)

    def heuristics(self, node: Node) -> int:
        """
        ========================================================================
         Return the Heuristic-Distance from the given Node to the Goal.
        ========================================================================
        """
        return node.distance(other=self.goal)
