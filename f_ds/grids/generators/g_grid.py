from f_ds.grids.grid import Grid, Cell


class GenGrid:
    """
    ================================================================================
     Grid generator class.
    ================================================================================
    """

    @staticmethod
    def gen_random(rows: int, pct_invalid: int) -> Grid:
        """
        ============================================================================
         Generate a random grid.
        ============================================================================
        """
        grid = Grid(rows=rows)
        cells_invalid = grid.sample(pct=pct_invalid)
        Cell.invalidate(cells_invalid)
        return grid

    @staticmethod
    def gen_3x3() -> Grid:
        """
        ============================================================================
         Generate a 3x3 grid.
        ============================================================================
        """
        return Grid(rows=3)
