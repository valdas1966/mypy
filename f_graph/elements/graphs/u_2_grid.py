from f_graph.elements.graphs.i_2_grid import GraphGrid
from f_ds.grids.u_grid import UGrid


class UGraphGrid:
    """
    ============================================================================
     Utils-Class of Graph-Grid.
    ============================================================================
    """

    @staticmethod
    def generate(rows: int,
                 cols: int = None,
                 pct_valid: int = 100,
                 name: str = None) -> GraphGrid:
        """
        ========================================================================
         Return a generated GraphGrid by received parameters.
        ========================================================================
        """
        grid = UGrid.generate(rows=rows, cols=cols, pct_valid=pct_valid)
        return GraphGrid(grid=grid, name=name)
