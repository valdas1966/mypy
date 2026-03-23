from f_search.algos.i_2_omspp.i_1_repeated.astar_backward.main import (
    AStarRepeatedBackward)
from f_search.problems.i_2_omspp import ProblemOMSPP


class Factory:
    """
    ========================================================================
     Factory for AStarRepeatedBackward test instances.
    ========================================================================
    """

    @staticmethod
    def without_obstacles() -> AStarRepeatedBackward:
        """
        ====================================================================
         AStarRepeatedBackward on a 4x4 grid without obstacles.
        ====================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return AStarRepeatedBackward(problem=problem)

    @staticmethod
    def with_obstacles() -> AStarRepeatedBackward:
        """
        ====================================================================
         AStarRepeatedBackward on a 4x4 grid with obstacles.
        ====================================================================
        """
        problem = ProblemOMSPP.Factory.with_obstacles()
        return AStarRepeatedBackward(problem=problem)
