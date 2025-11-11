from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f_ds.grids.grid.base import Group, GridBase as Grid, CellBase as Cell


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

    def random(self, size: int = None, pct: int = None) -> Group[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid.
        ========================================================================
        """
        return self._grid.sample(size=size, pct=pct)

    def random_in_range(self,
                        size: int = None,
                        pct: int = None,
                        row_min: int = 0,
                        col_min: int = 0,
                        row_max: int = None,
                        col_max: int = None) -> Group[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid within a given range.
        ========================================================================
        """
        row_max = row_max if row_max is not None else self._grid.rows - 1
        col_max = col_max if col_max is not None else self._grid.cols - 1

        def predicate(cell: Cell) -> bool:
            is_valid_row = row_min <= cell.row <= row_max
            is_valid_col = col_min <= cell.col <= col_max
            return is_valid_row and is_valid_col

        cells_within = self._grid.filter(predicate=predicate)
        return cells_within.sample(size=size, pct=pct)

   