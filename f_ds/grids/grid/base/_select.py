from __future__ import annotations
from f_math.shapes import Rect
from f_utils import u_iter
from typing import TYPE_CHECKING, Callable

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

    def sample(self, size: int = None, pct: int = None) -> list[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid.
        ========================================================================
        """
        return u_iter.sample(items=self._grid, size=size, pct=pct)

    def filter(self, predicate: Callable[[Cell], bool]) -> list[Cell]:
        """
        ========================================================================
         Return a list of Cells from the Grid that satisfy the predicate.
        ========================================================================
        """
        return u_iter.filter(items=self._grid, predicate=predicate)

    def random_in_rect(self,
                       size: int = None,
                       pct: int = None,
                       rect: Rect = None) -> list[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid within a given rectangle.
        ========================================================================
        """
        row_min, col_min, row_max, col_max = rect.to_min_max()
        return self.random_in_range(size=size,
                                    pct=pct,
                                    row_min=row_min,
                                    row_max=row_max,
                                    col_min=col_min,
                                    col_max=col_max)

    def random_in_range(self,
                        size: int = None,
                        pct: int = None,
                        row_min: int = None,
                        col_min: int = None,
                        row_max: int = None,
                        col_max: int = None) -> list[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid within a given range.
        ========================================================================
        """
        row_min = row_min if row_min is not None else 0
        col_min = col_min if col_min is not None else 0
        row_max = row_max if row_max is not None else self._grid.rows - 1
        col_max = col_max if col_max is not None else self._grid.cols - 1

        def predicate(cell: Cell) -> bool:
            """
            ========================================================================
             Predicate to filter Cells within a given range.
            ========================================================================
            """
            return cell.is_within(row_min, row_max, col_min, col_max)

        cells_within = u_iter.filter(items=self._grid, predicate=predicate)
        return u_iter.sample(items=cells_within, size=size, pct=pct)
