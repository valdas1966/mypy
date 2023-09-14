from f_data_structure.f_grid.grid_layout import GridLayout
from f_data_structure.f_grid.cell import Cell
from typing import Type
import random


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
           [*] Returns a flattened List of all Cells in the Grid.
        2. num_all() -> int
           [*] Returns Number of Cells in the Grid.
        3. __getitem__(self, index) -> list[Cell]
           [*] Allows direct access to a Row of Cells by [Row] Property and to
                a specific Cell by [Row][Col] Properties.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 class_cell: Type[Cell] = Cell):
        GridLayout.__init__(self, rows, cols, name)
        self._grid = [
                      [class_cell(row, col) for col in range(self.cols)]
                      for row in range(self.rows)
                     ]

    def cells(self) -> list[Cell]:
        """
        ========================================================================
         Desc: Returns a flattened List of all Cells in the Grid.
        ========================================================================
        """
        return [cell for row in self._grid for cell in row]

    def cells_random(self,
                     size: int = None,
                     pct: int = None) -> list[Cell]:
        """
        ========================================================================
         Desc: Return List of Random-Cells from the Grid.
        ------------------------------------------------------------------------
                Either [size] or [pct] should be provided:
                1. size : The number of random cells to retrieve.
                2. pct  : The percentage of total cells to retrieve.
        ========================================================================
        """
        if pct:
            size = int(pct * len(self) / 100)
        return random.sample(self.cells(), k=size)

    def __len__(self) -> int:
        """
        ========================================================================
         Desc: Returns a Number of Cells in the Grid.
        ========================================================================
        """
        return self.rows * self.cols

    def __getitem__(self, index) -> list[Cell]:
        """
        ========================================================================
         Desc: Allows direct access to a Row of Cells by [Row] Property and to
                a specific Cell by [Row][Col] Properties.
        ========================================================================
        """
        return self._grid[index]
