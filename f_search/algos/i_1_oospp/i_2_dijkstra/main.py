from f_search.algos.i_1_oospp.i_1_astar import AStar
from f_search.problems import ProblemOOSPP, State


class Dijkstra(AStar):
    """
    ============================================================================
     Dijkstra's Algorithm for One-to-One Shortest-Path-Problem.
     Dijkstra is equivalent to A* with h(n) = 0 for all nodes.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemOOSPP,
                 verbose: bool = False,
                 name: str = 'Dijkstra') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AStar.__init__(self,
                       problem=problem,
                       verbose=verbose,
                       name=name)

    def _heuristic(self, state: State) -> int:
        """
        ========================================================================
         Return the Heuristic-Value of the given State.
         Dijkstra does not use heuristics, so h(n) = 0 for all nodes.
        ========================================================================
        """
        return 0
