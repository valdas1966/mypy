from f_graph.path.one_to_one.solution import SolutionOneToOne as Solution
from f_graph.path.one_to_one.generators.g_state import GenStateOneToOne
from f_graph.path.generators.g_cache import GenCache
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
        state = GenStateOneToOne.gen_priority()
        stats = GenStatsPath.gen_10x20x30()
        cache = GenCache.from_explored()
        return Solution(is_valid=True, cache=cache, state=state, stats=stats)


solution = GenSolutionOneToOne.gen_3x3()
print(solution.path)