from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.cache import Cache, DataCache


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
        graph = problem.graph
        node = graph[0, 1]
        path_from_node = [graph[0, 2], graph[1, 2], graph[2, 2]]
        data = DataCache(path=lambda: path_from_node, distance=lambda: 3)
        cache[node] = data
        return cache
