from f_heuristic_search.problem_types.mixin.has_graph import HasGraph, Graph
from f_heuristic_search.problem_types.mixin.has_start import HasStart
from f_heuristic_search.problem_types.mixin.has_goal import HasGoal
from f_data_structure.nodes.i_2_cell import NodeCell
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeCell)


class SPPConcrete(Generic[Node], HasGraph, HasStart[Node], HasGoal[Node]):
    """
    ============================================================================
     Represents a one-to-one Shortest-Path-Problem in Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasGraph.__init__(self, graph=graph)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)

    def __str__(self) -> str:
        """
        ========================================================================
         1. Return STR-REPR of the SPP.
         2. Example: 'SPP[Maze]: (0,1) -> (2,3)'
        ========================================================================
        """
        return f'SPP[{self._graph.name}]: {self._start} -> {self._goal}'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the SPP.
        ========================================================================
        """
        return self.__str__()
