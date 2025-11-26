from f_search.algos.i_2_omspp.i_2_k_dijkstra.main import KDijkstra
from f_search.problems.i_2_omspp import ProblemOMSPP


class Factory:
    """
    ============================================================================
     Factory for creating KDijkstra algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> KDijkstra:
        """
        ========================================================================
         Return a KDijkstra algorithm with a ProblemOMSPP without obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return KDijkstra(problem=problem)

    @staticmethod
    def with_obstacles() -> KDijkstra:
        """
        ========================================================================
         Return a KDijkstra algorithm with a ProblemOMSPP with obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.with_obstacles()
        return KDijkstra(problem=problem)
