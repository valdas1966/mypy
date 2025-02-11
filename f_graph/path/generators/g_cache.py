from f_graph.path.generators.g_graph import GenGraphPath
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
        graph = GenGraphPath.gen_3x3()
        node = graph[0, 1]
        path_from_node = [graph[0, 2], graph[1, 2], graph[2, 2]]
        data = DataCache(path=lambda: path_from_node, distance=lambda: 3)
        cache[node] = data

        return cache
    
    @staticmethod
    def gen_3x3_from_explored() -> Cache:
        """
        ========================================================================
         Generate a cache for a 3x3 problem from an explored set.
        ========================================================================
        """     
        graph = GenGraphPath.gen_3x3()
        graph[2, 2].parent = None
        graph[1, 2].parent = graph[2, 2]
        explored = {graph[2, 2], graph[1, 2]}
        return Cache.from_explored(explored=explored)

    @staticmethod
    def gen_3x3_from_path() -> Cache:
        """
        ========================================================================
         Generate a cache for a 3x3 problem from a path.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        graph[2, 2].parent = graph[1, 2]
        graph[1, 2].parent = graph[0, 2]
        graph[0, 2].parent = graph[0, 1]
        path = [graph[0, 1], graph[0, 2], graph[1, 2], graph[2, 2]]
        return Cache.from_path(path=path)
    
    @staticmethod
    def gen_data_cache() -> DataCache:
        """
        ========================================================================
         Generate a data cache.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        path = [graph[0, 0], graph[0, 1]]
        return DataCache(path=lambda: path, distance=lambda: 2)
