from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.one_to_one.cache import Cache, DataCache


class GenCache:
    """
    ============================================================================
     Cache-Generator for One-to-One Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> Cache:
        """
        ========================================================================
         Generate a cache for a 3x3 problem.
        ========================================================================
        """
        cache = Cache()
        problem = GenProblemOneToOne.gen_3x3()
        goal, pre_goal = problem.goal, problem.pre_goal
        data_goal = DataCache(path=lambda: [], distance=lambda: 0)
        cache[goal] = data_goal
        data_pre_goal = DataCache(path=lambda: [goal], distance=lambda: 1)
        cache[pre_goal] = data_pre_goal
        return cache
