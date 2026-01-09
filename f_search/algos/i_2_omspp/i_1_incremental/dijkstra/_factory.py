from f_search.algos.i_2_omspp.i_1_incremental.dijkstra.main import DijkstraIncremental
from f_search.problems.i_2_omspp.main import ProblemOMSPP


class Factory:
    """
    ============================================================================
     Factory for Dijkstra Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """
    
    @staticmethod
    def without_obstacles() -> DijkstraIncremental:
        """
        ========================================================================
         Return a Dijkstra Algorithm for One-to-Many Shortest-Path-Problem.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return DijkstraIncremental(problem=problem)
