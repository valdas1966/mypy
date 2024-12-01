from f_graph.graphs.i_1_grid import GraphGrid, NodeCell
from f_ds.grids.u_grid import UGrid as u_grid
from typing import Type


class UGraphGrid:
    """
    ============================================================================
     GraphGrid Utils-Class.
    ============================================================================
    """

    @staticmethod
    def generate(rows: int,
                 cols: int = None,
                 pct_valid: int = 100,
                 type_node: Type[NodeCell] = NodeCell,
                 name: str = None) -> GraphGrid:
        """
        ========================================================================
         Generate list GraphGrid with Random valid nodes based on list given Pct.
        ========================================================================
        """
        grid = u_grid.generate(rows, cols, pct_valid)
        return GraphGrid(grid=grid, type_node=type_node, name=name)

    @staticmethod
    def generate_multiple(n: int,
                          rows: int,
                          cols: int = None,
                          pct_valid: int = 100,
                          type_node: Type[NodeCell] = NodeCell):
        """
        ========================================================================
         Generate multiple random GraphGrids.
        ========================================================================
        """
        return [UGraphGrid.generate(rows, cols, pct_valid, type_node)
                for _ in range(n)]
