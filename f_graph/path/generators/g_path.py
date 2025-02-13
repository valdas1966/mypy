from f_graph.path.path import Path
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
