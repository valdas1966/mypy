from f_graph.path.one_to_one.solution import SolutionOneToOne as Solution
from f_graph.path.one_to_one.generators.g_state import GenStateOneToOne
from f_graph.path.one_to_one.generators.g_cache import GenCache
from f_graph.path.generators.g_stats import GenStatsPath


class GenSolutionOneToOne:
    """
    ========================================================================
     Generate solution.
    ========================================================================
    """

    @staticmethod
    def gen_3x3() -> Solution:
        """
        ========================================================================
         Generate a 3x3 solution.
        ========================================================================
        """
        state = GenStateOneToOne.gen_3x3()
        stats = GenStatsPath.gen_10x20()
        cache = GenCache.gen_3x3()
        return Solution(is_valid=True, cache=cache, state=state, stats=stats)
