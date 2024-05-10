from __future__ import annotations
from f_ds.grids.i_0_base import GridBase, Cell
from typing import Generic, TypeVar
import random

C = TypeVar('C', bound=Cell)


class GridCells(Generic[C], GridBase[C]):
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
        GridBase.__init__(self, rows, cols, name)
        # 2D-Grid of Cells
        self._grid: list[list[C]] = [
                                        [C(row, col)
                                         for col in range(self.cols)]
                                        for row in range(self.rows)
                                        ]

    def cells(self) -> list[C]:
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
                     pct: int = None) -> list[C]:
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

    def neighbors(self, cell: C) -> list[C]:
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

    def make_invalid_cells(self, cells: list[C]) -> None:
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
        return len(self.cells()) / self.total()

    def pct_non_valid(self) -> int:
        """
        ========================================================================
         Returns the Percentage of Non-Valid Cells in the Grid.
        ========================================================================
        """
        return int(round((1 - self.pct_cells_valid()) * 100, 0))

    def _make_invalid_row_col(self, row: int, col: int) -> None:
        """
        ========================================================================
         Turn the Cell in the received Coords to Invalid.
        ========================================================================
        """
        self._grid[row][col].is_valid = False

    def __getitem__(self, index) -> list[C]:
        """
        ========================================================================
         1. Direct access to a Row of Cells via the [Row] Property.
         2. Direct access specific Cell using [Row][Col] Properties.
        ========================================================================
        """
        return self._grid[index]

    def __str__(self) -> str:
        # Cols Title
        res = '  ' + ' '.join((str(col) for col in range(self.cols))) + '\n'
        for row in range(self.rows):
            res += str(row) + ' '
            for col in range(self.cols):
                res += '1 ' if self._grid[row][col].is_valid else '0 '
            res += '\n'
        return res

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

    @classmethod
    def generate_list(cls,
                      cnt: int,
                      rows: int,
                      cols: int = None,
                      pct_non_valid: int = 0
                      ) -> list[GridCells]:
        """
        ========================================================================
         Generates a List of randoms Grid based on received params
          (size and percentage of invalid cells).
        ========================================================================
        """
        return [cls.generate(rows, cols, pct_non_valid) for _ in range(cnt)]
