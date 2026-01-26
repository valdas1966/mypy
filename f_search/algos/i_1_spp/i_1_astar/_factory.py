from f_search.algos.i_1_spp.i_1_astar.main import AStar, ProblemSPP
from f_search.ds.data import DataBestFirst
from f_search.problems import State


class Factory:
    """
    ============================================================================
     Factory for creating AStar algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> AStar:
        """
        ========================================================================
         Return a AStar algorithm with a ProblemSPP without obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        return AStar(problem=problem)

    @staticmethod
    def with_obstacles() -> AStar:
        """
        ========================================================================
         Return a AStar algorithm with a ProblemSPP with obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.with_obstacles()
        return AStar(problem=problem)
