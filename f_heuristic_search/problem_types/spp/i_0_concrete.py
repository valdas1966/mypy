from f_heuristic_search.problem_types.mixin.has_graph import HasGraph, GraphBase
from f_heuristic_search.problem_types.mixin.has_start import HasStart, NodePath
from f_heuristic_search.problem_types.mixin.has_goal import HasGoal
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodePath)


class SPPConcrete(Generic[Graph, Node],
                  HasGraph[Graph],
                  HasStart[Node],
                  HasGoal[Node]):
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
