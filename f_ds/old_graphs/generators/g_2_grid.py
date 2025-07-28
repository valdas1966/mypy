from f_ds.old_graphs.i_2_grid import GraphGrid, NodeCell, Grid
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
                 type_node: Type[NodeCell] = NodeCell) -> GraphGrid:
        """
        ========================================================================
         Generate Graph of Grid.
        ========================================================================
        """
        grid = Grid.generate(rows=rows, pct_valid=pct_valid)
        return GraphGrid(grid=grid, type_node=type_node)
