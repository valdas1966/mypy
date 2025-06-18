from f_ds.grids.grid import Grid, Cell


class GenGrid:
    """
    ================================================================================
     Grid generator class.
    ================================================================================
    """

    @staticmethod
    def random(rows: int,
               cols: int = None,
               pct_invalid: int = 0,
               name: str = None) -> Grid:
        """
        ============================================================================
         Generate a random grid.
        ============================================================================
        """
        grid = Grid(rows=rows, cols=cols, name=name)
        cells_invalid = grid.sample(pct=pct_invalid)
        Cell.invalidate(cells_invalid)
        return grid

    @staticmethod
    def full_3x3() -> Grid:
        """
        ============================================================================
         Generate a 3x3 grid.
        ============================================================================
        """
        return Grid(rows=3)
