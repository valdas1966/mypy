from f_graph.path.graph import GraphPath as Graph, NodePath
from f_ds.grids.generators.g_grid import GenGrid


class GenGraphPath:
    """
    ================================================================================
     Graph-Path generator.
    ================================================================================
    """

    @staticmethod
    def gen_3x3() -> Graph:
        """
        ============================================================================
         Generate a 3x3 grid graph.
        ============================================================================
        """
        grid = GenGrid.gen_3x3()
        return Graph(grid=grid, type_node=NodePath)
    
    @staticmethod
    def gen_4x4() -> Graph:
        """
        ============================================================================
         Generate a 4x4 grid graph.
        ============================================================================
        """
        grid = GenGrid.gen_4x4()    
        return Graph(grid=grid, type_node=NodePath)
    