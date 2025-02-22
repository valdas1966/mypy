from f_graph.path.generators.g_path import GenPath, GenNode
from f_graph.path.generators.g_graph import GenGraphPath
from f_graph.path.generators.g_cache import GenCache
from f_graph.path.boundary import Boundary
from f_graph.path.cache import Cache
from f_graph.path.path import Path


class GenBoundary:
    """
    ========================================================================
     Generate Boundaries.
    ========================================================================
    """

    @staticmethod
    def first_row_branch_3x3() -> Boundary:
        """
        ====================================================================
         Generate the Boundary for a 3x3 Grid with First-Row Branch.
        ====================================================================
        """
        graph = GenGraphPath.gen_3x3()
        branch = GenNode.first_row_branch_3x3()
        path = Path(data=branch)
        cache = Cache(data=path)
        return Boundary.from_path(path=path, graph=graph, cache=cache)
    
    @staticmethod
    def boundary_4x4() -> Boundary:
        """
        ====================================================================
         Generate the Boundary for a 4x4 Grid.
        ====================================================================
        """
        graph = GenGraphPath.gen_4x4()
        path = GenPath.boundary_4x4()
        cache = GenCache.boundary_4x4()
        return Boundary.from_path(path=path, graph=graph, cache=cache)
