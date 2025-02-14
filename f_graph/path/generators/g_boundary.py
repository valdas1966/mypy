from f_graph.path.generators.g_graph import GenGraphPath
from f_graph.path.generators.g_path import GenPath
from f_graph.path.generators.g_node import GenNode
from f_graph.path.boundary import Boundary
from f_graph.path.cache import Cache


class GenBoundary:
    """
    ========================================================================
     Generate Boundaries.
    ========================================================================
    """

    @staticmethod
    def gen_3x3() -> Boundary:
        """
        ====================================================================
         Generate the Boundary for a 3x3 Grid.
        ====================================================================
        """
        graph = GenGraphPath.gen_3x3()
        path = GenPath.gen_first_row_3x3()
        cache = Cache(data=path)
        return Boundary.from_path(path=path, graph=graph, cache=cache)
    
    @staticmethod
    def gen_02_22() -> Boundary:
        """
        ====================================================================
         Generate the Boundary for a 02-22 Grid.
        ====================================================================
        """
        graph = GenGraphPath.gen_3x3()
        path = GenPath.gen_02_22()
        cache = Cache(data=path)
        return Boundary.from_path(path=path, graph=graph, cache=cache)

