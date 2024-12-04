from f_ds.grids.u_grid import UGrid
from f_graph.path.graph import GraphPath as Graph
from typing import Type


class GenGraph:
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
        grid = UGrid.generate(rows=rows, pct_valid=pct_valid)
        return GraphGrid(grid=grid, type_node=type_node)
