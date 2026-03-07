from f_search.algos.i_2_omspp.i_1_incremental.astar_backward.main import (
    AStarIncrementalBackward)
from f_search.problems.i_2_omspp.main import ProblemOMSPP


class Factory:
    """
    ========================================================================
     Factory for AStarIncrementalBackward test instances.
    ========================================================================
    """

    @staticmethod
    def without_obstacles() -> AStarIncrementalBackward:
        """
        ====================================================================
         AStarIncrementalBackward on a 4x4 grid without obstacles.
        ====================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return AStarIncrementalBackward(problem=problem)

    @staticmethod
    def without_obstacles_with_bounds() -> AStarIncrementalBackward:
        """
        ====================================================================
         AStarIncrementalBackward on a 4x4 grid without obstacles,
          with_bounds=True.
        ====================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return AStarIncrementalBackward(problem=problem,
                                        with_bounds=True)
