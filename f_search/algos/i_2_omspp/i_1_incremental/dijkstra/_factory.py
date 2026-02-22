from f_search.algos.i_2_omspp.i_1_incremental.dijkstra.main import DijkstraIncremental
from f_search.problems import ProblemOMSPP


class Factory:
    """
    ============================================================================
     Factory for Incremental Dijkstra's Algorithm for OMSPP.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> DijkstraIncremental:
        """
        ========================================================================
         Return an Incremental Dijkstra's Algorithm for OMSPP without obstacles.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return DijkstraIncremental(problem=problem)
