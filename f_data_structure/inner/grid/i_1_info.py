from f_data_structure.inner.grid.i_0_init import GridInit


class GridInfo(GridInit):
    """
    ============================================================================
     Desc: Represents Grid with Info-Parameters.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. shape() -> str
           - Returns STR-Representation of the Grid's Shape as (rows, cols).
        2. num_cells_all() -> int
           - Returns Number of All Grid's Cells.
    ============================================================================
    """

    def shape(self) -> str:
        """
        ========================================================================
         Desc: Returns STR-Representation of the Grid's Shape as (rows,cols).
        ========================================================================
        """
        return f'({self.num_rows},{self.num_cols})'

    def num_cells_all(self) -> int:
        """
        ========================================================================
         Desc: Returns Number of all Grid's Cells.
        ========================================================================
        """
        return self.num_rows * self.num_cols
