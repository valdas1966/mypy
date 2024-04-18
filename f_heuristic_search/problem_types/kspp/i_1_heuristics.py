from f_heuristic_search.problem_types.kspp.i_0_concrete import KSPPConcrete
from f_data_structure.graphs.i_1_grid import GraphGrid
from f_data_structure.nodes.i_2_cell import NodeCell
from enum import Enum, auto
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphGrid)
Node = TypeVar('Node', bound=NodeCell)


class SPPHeuristics(Generic[Graph, Node], KSPPConcrete[Graph, Node]):
    """
    ============================================================================
     One-to-Many Shortest-Path-Problem with Heuristics.
    ============================================================================
    """

    class HEURISTIC(Enum):
        """
        ========================================================================
         Enum for different Heuristic-Functions that the class enables.
        ========================================================================
        """
        NEAREST = auto(),
        FARTHEST = auto()

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goals: tuple[Node, ...],
                 h_func: HEURISTIC = HEURISTIC.NEAREST) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        KSPPConcrete.__init__(self, graph=graph, start=start, goals=goals)
        self._h_func = h_func

    @property
    def h_func(self) -> HEURISTIC:
        return self._h_func

    def calc_h(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristic-Distance from the given Node to the Goal.
        ========================================================================
        """
        if self._h_func == self.HEURISTIC.MANHATTAN_DISTANCE:
            return node.distance(other=self.goal)
