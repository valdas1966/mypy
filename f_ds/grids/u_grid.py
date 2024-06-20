from f_ds.grids.grid import Grid
from f_utils import u_list

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
        cells = grid.to_list()
        cells_to_invalidate = u_list.to_sample(li=cells, pct=pct_valid)
        for cell in cells_to_invalidate:
            cell.set_invalid()
        return grid
