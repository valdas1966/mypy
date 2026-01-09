from f_search.algos.i_2_omspp.i_1_incremental.astar.main import AStarIncremental
from f_search.problems.i_2_omspp.main import ProblemOMSPP


class Factory:
    """
    ============================================================================
     Factory for A* Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """
    
    @staticmethod
    def without_obstacles() -> AStarIncremental:
        """
        ========================================================================
         Return an A* Algorithm for One-to-Many Shortest-Path-Problem.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return AStarIncremental(problem=problem)
