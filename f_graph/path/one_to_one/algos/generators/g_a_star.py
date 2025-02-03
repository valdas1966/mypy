from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.one_to_one.algos.a_star import AStar
from f_graph.path.generators.g_cache import GenCache


class GenAStar:
    """
    ============================================================================
     Generator for A* Algorithm.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> AStar:
        """
        ========================================================================
         Generate an A* Algorithm for a 3x3-Grid.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        return AStar(problem=problem)
    
    @staticmethod
    def gen_3x3_cache() -> AStar:
        """
        ========================================================================
         Generate an A* Algorithm for a 3x3-Grid with cache.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        cache = GenCache.gen_3x3()
        return AStar(problem=problem, cache=cache)
