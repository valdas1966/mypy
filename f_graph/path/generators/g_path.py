from f_graph.path.path import Path
from f_graph.path.generators.g_graph import GenGraphPath
from f_graph.path.generators.g_node import GenNode


class GenPath:
    """
    ========================================================================
     Generate paths.
    ========================================================================
    """

    @staticmethod
    def gen_first_row_3x3() -> Path:
        """
        ====================================================================
         Generate a first row path.
        ====================================================================
        """ 
        nodes = GenNode.gen_first_row_3x3()
        nodes[1].parent = nodes[0]
        nodes[2].parent = nodes[1]
        return Path(data=nodes)
    
    @staticmethod
    def boundary_4x4() -> Path:
        """
        ====================================================================
         Generate a boundary path.
        ====================================================================
        """
        graph = GenGraphPath.gen_4x4()
        graph[3, 3].parent = None
        graph[2, 3].parent = graph[3, 3]
        graph[1, 3].parent = graph[2, 3]
        graph[0, 3].parent = graph[1, 3]
        graph[0, 2].parent = graph[0, 3]
        graph[0, 1].parent = graph[0, 2]
        graph[0, 0].parent = graph[0, 1]
        graph[1, 0].parent = graph[0, 0]
        graph[2, 0].parent = graph[1, 0]
        nodes = [graph[3, 3], graph[2, 3], graph[1, 3], graph[0, 3],
                 graph[0, 2], graph[0, 1], graph[0, 0],
                 graph[1, 0], graph[2, 0]]
        return Path(data=nodes)
