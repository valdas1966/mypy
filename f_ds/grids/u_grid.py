from f_ds.grids.grid import Grid
from f_ds.grids.u_cell import UCell


class UGrid:
    """
    ============================================================================
     Grid Utils-Class.
    ============================================================================
    """

    @staticmethod
    def generate(rows: int,
                 cols: int = None,
                 pct_valid: int = 100,
                 name: str = None) -> Grid:
        """
        ========================================================================
         Generate a Grid with Random Valid-Cells based on a given Percentage.
        ========================================================================
        """
        grid = Grid(name=name, rows=rows, cols=cols)
        cells_to_invalidate = grid.sample(pct=100-pct_valid)
        UCell.invalidate(cells_to_invalidate)
        return grid

    @staticmethod
    def generate_multiple(n: int,
                          rows: int,
                          cols: int = None,
                          pct_valid: int = 100):
        """
        ========================================================================
         Generate multiple random Grids.
        ========================================================================
        """
        return [UGrid.generate(rows, cols, pct_valid) for _ in range(n)]
