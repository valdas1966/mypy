from f_graph.path.one_to_one.algos.bfs import BFS
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.generators.g_cache import GenCache


class GenBFS:
    """
    ============================================================================
     Generator for BFS-Algorithms.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> BFS:
        """
        ========================================================================
         Generate a BFS-Algorithm for a 3x3-Grid.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        return BFS(problem=problem)
    
    @staticmethod
    def gen_3x3_cache() -> BFS:
        """
        ========================================================================
         Generate a BFS-Algorithm for a 3x3-Grid with cache.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        cache = GenCache.gen_3x3()
        return BFS(problem=problem, cache=cache)
