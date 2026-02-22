from f_search.algos.i_1_spp.i_1_dijkstra.main import Dijkstra
from f_search.problems import ProblemSPP


class Factory:
    """
    ============================================================================
     Factory for creating Dijkstra algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> Dijkstra:
        """
        ========================================================================
         Return a Dijkstra algorithm with a ProblemSPP without obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        return Dijkstra(problem=problem)
