from f_search.algos.i_1_spp.i_3_astar_reusable_flags.main import (
    AStarReusableFlags)
from f_search.problems import ProblemSPP
from f_search.ds.data.incremental import DataIncremental


class Factory:
    """
    ========================================================================
     Factory for AStarReusableFlags test instances.
    ========================================================================
    """

    @staticmethod
    def without_obstacles() -> AStarReusableFlags:
        """
        ====================================================================
         AStarReusableFlags on a 4x4 grid without obstacles.
        ====================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        return AStarReusableFlags(problem=problem)

    @staticmethod
    def without_obstacles_with_data() -> AStarReusableFlags:
        """
        ====================================================================
         AStarReusableFlags on a 4x4 grid with pre-filled
          DataIncremental (cached and bounded values).
        ====================================================================
        """
        problem = ProblemSPP.Factory.without_obstacles()
        data_incremental = DataIncremental.Factory.with_cached_and_bounded()
        return AStarReusableFlags(problem=problem,
                                  data_incremental=data_incremental)
