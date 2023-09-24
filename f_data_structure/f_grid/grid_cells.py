from __future__ import annotations
from f_data_structure.f_grid.grid_layout import GridLayout
from f_data_structure.f_grid.cell import Cell
import random


class GridCells(GridLayout):
    """
    ============================================================================
     1. Represents a 2D-Grid of Cells.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. cells() -> list[Cell]
           [*] Returns a flattened List of all Grid's valid Cells.
        2. cells_random(size: int, pct: int) -> list[Cell]
           [*] Returns a List of random Grid's valid Cells.
        3. neighbors() -> List[Cell]
           [*] Returns a list of Cell's valid neighbors.
        4. make_invalid(cells: list[Cell) -> None
           [*] Turns list[Cell] into invalid cells.
        5. is_within(cell: Cell) -> bool
           [*] Returns True if the received Cell is within the Grid's borders.
        6. pct_cells_valid() -> float
           [*] Returns Percentage of Valid-Cells in the Grid.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. __getitem__(self, index) -> list[Cell]
           [*] Allows direct access to a Row of Cells (list) by [Row] Property
                and to a specific Cell by [Row][Col] Properties.
    ============================================================================
     Class Methods:
    ----------------------------------------------------------------------------
        1. generate(rows: int,
                    cols: int = None,
                    name: str = None,
                    pct_cells_invalid: int = 0) -> GridCells
        [*] Generates a random Grid based on received parameters
            (size and percentage of invalid cells).
    ============================================================================
    """

    _name: str                 # Grid's Name.
    _rows: int                 # Number of Rows in the Grid.
    _cols: int                 # Number of Cols in the Grid.
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
            size = int(pct * len(self) / 100)
        return random.sample(self.cells(), k=size)

    def neighbors(self, cell: Cell) -> list[Cell]:
        """
        ========================================================================
         Returns a list of Cell's valid neighbors.
        ========================================================================
        """
        coords = [(cell.row - 1, cell.col),
                  (cell.row, cell.col - 1),
                  (cell.row, cell.col + 1),
                  (cell.row + 1, cell.col)
                  ]
        return [self._grid[row][col]
                for row, col
                in coords
                if self.is_within(row, col) and self._grid[row][col].is_valid]

    def make_invalid(self, cells: list[Cell]) -> None:
        """
        ========================================================================
         Turns received List[Cell] to invalid.
        ========================================================================
        """
        for cell in cells:
            cell.is_valid = False

    def is_within(self, cell: Cell) -> bool:
        """
        ========================================================================
         Returns True if the received Cell is withing the Grid's boundaries.
        ========================================================================
        """
        return super().is_within(cell.row, cell.col)

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
         Desc: Allows direct access to a Row of Cells by [Row] Property and to
                a specific Cell by [Row][Col] Properties.
        ========================================================================
        """
        return self._grid[index]

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 pct_non_valid: int = 0
                 ) -> GridCells:
        """
        ========================================================================
         Generates a random Grid based on received params
          (size and percentage of invalid cells).
        ========================================================================
        """
        grid = GridCells(rows, cols, name)
        cells_random = grid.cells_random(pct=pct_non_valid)
        grid.make_invalid(cells_random)
        return grid
