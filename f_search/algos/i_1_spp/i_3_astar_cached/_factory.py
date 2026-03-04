from f_search.algos.i_1_spp.i_3_astar_cached.main import AStarCached
from f_search.problems import ProblemSPP
from f_search.ds.data.cached import DataCached


class Factory:
    """
    ========================================================================
     Factory for AStarCached test instances.
    ========================================================================
    """

    @staticmethod
    def without_cache() -> AStarCached:
        """
        ====================================================================
         AStarCached on a 6x6 grid without cached data.
        ====================================================================
        """
        problem = ProblemSPP.Factory.for_cached()
        return AStarCached(problem=problem)

    @staticmethod
    def with_cache() -> AStarCached:
        """
        ====================================================================
         AStarCached on a 6x6 grid with cached exact distances
          to goals from states on the optimal path.
        ====================================================================
        """
        problem = ProblemSPP.Factory.for_cached()
        data_cached = DataCached.Factory.six_cached()
        return AStarCached(problem=problem, data_cached=data_cached)

    @staticmethod
    def with_bounded() -> AStarCached:
        """
        ====================================================================
         AStarCached on a 6x6 grid with cached exact distances
          to goals from states on the optimal path and lower bounds for
          states that are adjacent neighbors to states on the optimal path.
        ====================================================================
        """
        problem = ProblemSPP.Factory.for_cached()
        data_cached = DataCached.Factory.six_bounded()
        return AStarCached(problem=problem, data_cached=data_cached)

    @staticmethod
    def with_bounded_depth_1() -> AStarCached:
        """
        ====================================================================
         AStarCached on a 6x6 grid with cached exact distances
          to goals from states on the optimal path and lower bounds for
          states that are adjacent neighbors to states on the optimal path,
          and lower boundes for their adjacent neighbors by heuristic
          propagation.
        ====================================================================
        """
        problem = ProblemSPP.Factory.for_cached()
        data_cached = DataCached.Factory.six_bounded_depth_1()
        return AStarCached(problem=problem, data_cached=data_cached)

    @staticmethod
    def with_bounded_depth_2() -> AStarCached:
        """
        ====================================================================
         AStarCached on a 6x6 grid with cached exact distances
          to goals from states on the optimal path and lower bounds for
          states that are adjacent neighbors to states on the optimal path,
          and lower boundes for their adjacent neighbors by heuristic
          propagation.
        ====================================================================
        """
        problem = ProblemSPP.Factory.for_cached()
        data_cached = DataCached.Factory.six_bounded_depth_2()
        return AStarCached(problem=problem, data_cached=data_cached)
