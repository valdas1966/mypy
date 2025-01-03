from f_graph.elements.graphs.i_2_grid import GraphGrid, NodeGraph
from f_ds.grids.u_grid import UGrid
from typing import Type


class GenGraphGrid:
    """
    ============================================================================
     Utils-Class for generating Graph of Grid.
    ============================================================================
    """

    @staticmethod
    def generate(rows: int,
                 pct_valid: int = 100,
                 type_node: Type[NodeGraph] = NodeGraph) -> GraphGrid:
        """
        ========================================================================
         Generate Graph of Grid.
        ========================================================================
        """
        grid = UGrid.gen(rows=rows, pct_valid=pct_valid)
        return GraphGrid(grid=grid, type_node=type_node)
