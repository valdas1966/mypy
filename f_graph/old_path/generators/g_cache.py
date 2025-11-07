from f_graph.old_path.generators.g_path import GenPath, GenNode
from f_graph.old_path.generators.g_graph import GenGraphPath
from f_hs.ds.cache import Cache
from f_hs.ds.path import Path


class GenCache:
    """
    ============================================================================
     Cache-Generator for One-to-One Path-Finding Problems.
    ============================================================================
    """
   
    @staticmethod
    def from_explored() -> Cache:
        """
        ========================================================================
         Generate a cache for a 3x3 problem from an explored set.
        ========================================================================
        """     
        explored = set(GenNode.first_row_branch_3x3())
        return Cache.from_explored(explored=explored)

    @staticmethod
    def from_path() -> Cache:
        """
        ========================================================================
         Generate a cache for a 3x3 problem from a old_path.
        ========================================================================
        """
        nodes = GenNode.first_row_branch_3x3()
        path = Path(data=nodes)
        return Cache.from_path(path=path)

    @staticmethod
    def best_0_1() -> Cache:
        """
        ========================================================================
         Generate a cache for a 3x3 problem from a boundary old_path.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        nodes = [graph[0, 1], graph[0, 2], graph[1, 2], graph[2, 2]]
        path = Path.from_list(nodes=nodes)
        for node in path:
            node.h = 0
        return Cache.from_path(path=path)

    @staticmethod
    def boundary_4x4() -> Cache:
        """
        ========================================================================
         Generate a cache for a 4x4 problem from a boundary old_path.
        ========================================================================
        """
        path = GenPath.boundary_4x4()
        return Cache.from_path(path=path)        
