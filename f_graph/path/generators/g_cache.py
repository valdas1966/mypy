from f_graph.path.generators.g_path import GenPath, GenNode
from f_graph.path.cache import Cache
from f_graph.path.path import Path


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
         Generate a cache for a 3x3 problem from a path.
        ========================================================================
        """
        nodes = GenNode.first_row_branch_3x3()
        path = Path(data=nodes)
        return Cache.from_path(path=path)

    @staticmethod
    def boundary_4x4() -> Cache:
        """
        ========================================================================
         Generate a cache for a 4x4 problem from a boundary path.
        ========================================================================
        """
        path = GenPath.boundary_4x4()
        return Cache.from_path(path=path)        
