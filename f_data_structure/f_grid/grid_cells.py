from __future__ import annotations
from f_data_structure.f_grid.grid_layout import GridLayout
from f_data_structure.f_grid.cell import Cell
import random


class GridCells(GridLayout):
    """
    ============================================================================
     Represents a 2D-Grid of Cells.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GridLayout.__init__(self, rows, cols, name)
        # 2D-Grid of Cells
        self._grid: list[list[Cell]] = [
                                        [Cell(row, col)
                                         for col in range(self.cols)]
                                        for row in range(self.rows)
                                        ]

    def cells(self) -> list[Cell]:
        """
        ========================================================================
         Desc: Returns a flattened List of the Grid's valid Cells.
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
         Desc: Return a List of Random-Cells from the Grid.
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

    def make_invalid_cells(self, cells: list[Cell]) -> None:
        """
        ========================================================================
         Turns the received List[Cell] to Invalid.
        ========================================================================
        """
        for cell in cells:
            self._make_invalid_row_col(cell.row, cell.col)

    def make_invalid_tuples(self, tuples: list[tuple]) -> None:
        """
        ========================================================================
         Turns the received List[Tuple] to Invalid.
        ========================================================================
        """
        for t in tuples:
            self._make_invalid_row_col(t[0], t[1])

    def pct_cells_valid(self) -> float:
        """
        ========================================================================
         Returns the Percentage of Valid-Cells in the Grid.
        ========================================================================
        """
        return len(self.cells()) / (self.rows * self.cols)

    def pct_non_valid(self) -> int:
        """
        ========================================================================
         Returns the Percentage of Non-Valid Cells in the Grid.
        ========================================================================
        """
        return round((1 - self.pct_cells_valid()) * 100, 0)

    def _make_invalid_row_col(self, row: int, col: int) -> None:
        """
        ========================================================================
         Turn the Cell in the received Coords to Invalid.
        ========================================================================
        """
        self._grid[row][col].is_valid = False

    def __getitem__(self, index) -> list[Cell]:
        """
        ========================================================================
         1. Direct access to a Row of Cells via the [Row] Property.
         2. Direct access specific Cell using [Row][Col] Properties.
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
        grid.make_invalid_cells(cells_random)
        return grid
