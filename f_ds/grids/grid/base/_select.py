from __future__ import annotations
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from f_ds.grids.grid import GridBase as Grid
    from f_ds.grids.cell import CellBase as Cell


class Select:
    """
    ============================================================================
     Select Class for GridBase.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid) -> None:
        """
        ========================================================================
         Initialize the Select object.
        ========================================================================
        """
        self._grid = grid

    def rect(self,
             row_min: int = 0,
             col_min: int = 0,
             row_max: int = None,
             col_max: int = None) -> Iterator[Cell]:
        """
        ========================================================================
         1. Return an iterator over the cells in a given rectangle.
         2. The values are exclusive.
        ========================================================================
        """
        # Set Row-Min and Col-Min
        row_min = max(row_min, 0)
        col_min = max(col_min, 0)
        # Set Row-Max
        if row_max is None:
            row_max = self._grid.rows - 1
        else:
            row_max = min(row_max, self._grid.rows - 1)
        # Set Col-Max
        if col_max is None:
            col_max = self._grid.cols - 1
        else:
            col_max = min(col_max, self._grid.cols - 1)
        # Iterate over the cells in the rectangle
        for row in range(row_min, row_max):
            grid_row = self._grid[row]
            for col in range(col_min, col_max):
                yield grid_row[col]

    def rect_around(self, cell: Cell, distance: int) -> Iterator[Cell]:
        """
        ========================================================================
         Return an iterator over the cells in a rectangle around a given cell.
        ========================================================================
        """
        row_min = cell.row - distance
        col_min = cell.col - distance
        row_max = cell.row + distance + 1
        col_max = cell.col + distance + 1
        return self.rect(row_min=row_min,
                         col_min=col_min,
                         row_max=row_max,
                         col_max=col_max)
