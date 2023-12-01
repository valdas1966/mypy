from __future__ import annotations
from f_data_structure.f_grid.grid_layout import GridLayout
from f_data_structure.f_grid.cell import Cell
import random


class GridCells(GridLayout):
    """
    ============================================================================
     1. Represents a 2D-Grid of Cells.
    ============================================================================
    """

    _grid: list[list[Cell]]    # 2D-Grid of Cells.

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None) -> None:
        GridLayout.__init__(self, rows, cols, name)
        self._grid = [
                      [Cell(row, col) for col in range(self.cols)]
                      for row in range(self.rows)
                     ]

    def cells(self) -> list[Cell]:
        """
        ========================================================================
         Desc: Returns a flattened List of Grid's valid Cells.
        ========================================================================
        """
        return [cell
                for row
                in self._grid
                for cell
                in row
                if cell.is_valid]

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
            size = int(pct * self.total() / 100)
        return random.sample(self.cells(), k=size)

    def neighbors(self, cell: Cell) -> list[Cell]:
        """
        ========================================================================
         Returns a list of valid neighbors for a given Cell.
        ========================================================================
        """
        coords = [(cell.row - 1, cell.col),
                  (cell.row, cell.col - 1),
                  (cell.row, cell.col + 1),
                  (cell.row + 1, cell.col)
                  ]
        coords_valid = [(r, c) for r, c in coords if self.is_within(r, c)]
        return [self._grid[r][c]
                for r, c
                in coords_valid
                if self._grid[r][c].is_valid]

    def make_invalid(self, cells: list[Cell | tuple]) -> None:
        """
        ========================================================================
         Turns received List[Cell|Tuple] to invalid.
        ========================================================================
        """
        for t in cells:
            if isinstance(t, Cell):
                row, col = t.row, t.col
            else:
                row, col = t
            self._grid[row][col].is_valid = False

    def pct_cells_valid(self) -> float:
        """
        ========================================================================
         Returns Percentage of Valid-Cells in the Grid.
        ========================================================================
        """
        return len(self.cells()) / (self.rows * self.cols)

    def __getitem__(self, index) -> list[Cell]:
        """
        ========================================================================
         Allows direct access to a Row of Cells by [Row] Property and to a
          specific Cell by [Row][Col] Properties.
        ========================================================================
        """
        return self._grid[index]

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 pct_non_valid: int = 0
                 ) -> GridCells:
        """
        ========================================================================
         Generates a random Grid based on received params
          (size and percentage of invalid cells).
        ========================================================================
        """
        grid = GridCells(rows, cols)
        cells_random = grid.cells_random(pct=pct_non_valid)
        grid.make_invalid(cells_random)
        return grid
