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
         AStarCached on a 5x5 grid without cached data.
        ====================================================================
        """
        problem = ProblemSPP.Factory.for_cached()
        return AStarCached(problem=problem, is_analytics=True)

    @staticmethod
    def with_cache() -> AStarCached:
        """
        ====================================================================
         AStarCached on a 5x5 grid with cached exact distances
          for column-4 states.
        ====================================================================
        """
        problem = ProblemSPP.Factory.for_cached()
        data_cached = DataCached.Factory.six_cached()
        return AStarCached(problem=problem, data_cached=data_cached)
