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
    def gen_02_22() -> Path:
        """
        ====================================================================
         Generate a 02-22 path.
        ====================================================================
        """
        graph = GenGraphPath.gen_3x3()
        nodes = [graph[0, 2], graph[1, 2], graph[2, 2]]
        nodes[1].parent = nodes[0]
        nodes[2].parent = nodes[1]
        return Path(data=nodes)
