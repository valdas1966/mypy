from f_data_structure.f_grid.grid_layout import GridLayout
from f_data_structure.f_grid.cell import Cell


class GridCells(GridLayout):
    """
    ============================================================================
     Desc: Represents a Grid of Cells.
           Allows direct access to a Row of Cells by [Row] Property and
            to a specific Cell by [Row][Col] Properties.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. cells() -> list[Cell]
           - Returns a flattened List of all Cells in the Grid.
    ============================================================================
    """

    def __init__(self,
                 num_rows: int,
                 num_cols: int = None,
                 name: str = None):
        GridLayout.__init__(self, num_rows, num_cols, name)
        self._grid = [
                      [Cell(row, col) for col in range(self.num_cols)]
                      for row in range(self.num_rows)
                     ]

    def cells(self) -> list[Cell]:
        """
        ========================================================================
         Desc: Returns a flattened List of all Cells in the Grid.
        ========================================================================
        """
        return [cell for row in self._grid for cell in row]

    def __getitem__(self, index) -> list[Cell]:
        """
        ========================================================================
         Desc: Allows direct access to a Row of Cells by [Row] Property and to
                a specific Cell by [Row][Col] Properties.
        ========================================================================
        """
        return self._grid[index]
