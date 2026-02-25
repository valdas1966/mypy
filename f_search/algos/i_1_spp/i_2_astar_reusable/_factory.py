from f_search.algos.i_1_spp.i_2_astar_reusable.main import AStarReusable
from f_search.problems import ProblemSPP
from f_search.ds.data import DataHeuristics


class Factory:
    """
    ============================================================================
     Factory for creating AStarReusable algorithms.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> AStarReusable:
        """
        ========================================================================
         Return an AStarReusable with a ProblemSPP without obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        return AStarReusable(problem=problem)

    @staticmethod
    def with_obstacles() -> AStarReusable:
        """
        ========================================================================
         Return an AStarReusable with a ProblemSPP with obstacles.
        ========================================================================
        """
        problem = ProblemSPP.Factory.with_obstacles()
        return AStarReusable(problem=problem)

    @staticmethod
    def without_obstacles_with_cell_00() -> AStarReusable:
        """
        ========================================================================
         Return an AStarReusable with a ProblemSPP without obstacles and
          with an explored Cell(0,0).
        ========================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        data = DataHeuristics.Factory.cell_00()
        return AStarReusable(problem=problem, data=data)
