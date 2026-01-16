from f_search.algos.i_1_spp import Dijkstra
from f_search.problems import ProblemSPP
from f_search.ds.states import StateBase as State


class DijkstraNeighborhood(Dijkstra):
    """
    ============================================================================
     Dijkstra's Algorithm to find Node's K-Neighborhood.
    ============================================================================
    """
    
    # Factory
    Factory: type = None
    
    def __init__(self,
                 problem: ProblemSPP,
                 steps: int,
                 name: str = 'DijkstraNeighborhood') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Dijkstra.__init__(self, problem=problem, name=name)
        self._steps = steps
        
    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Check if the Algorithm can terminate.
        ========================================================================
        """
        best = self.data.best
        g_best = self.data.g[best]
        return g_best > self._steps
    
    def _create_solution(self, is_valid: bool) -> set[State]:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        return self.data.explored
