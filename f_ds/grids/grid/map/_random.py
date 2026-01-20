from __future__ import annotations
from typing import TYPE_CHECKING
from f_utils.iter.u_iter import Pair, pairs, sample

if TYPE_CHECKING:
    from f_ds.grids.grid.map.main import GridMap as Grid, Cell


class Random:
    """
    ============================================================================
     Random Class for GridMap.
    ============================================================================
    """

    def __init__(self, grid: Grid) -> None:
        """
        ========================================================================
         Initialize the Random object.
        ========================================================================
        """
        self._grid = grid

    def cells(self, size: int = None, pct: int = None) -> list[Cell]:
        """
        ========================================================================
         Return a list of cells from the grid.
        ========================================================================
        """
        return sample(items=self._grid, size=size, pct=pct)

    def pairs(self,
              size: int,
              min_distance: int,
              tries: int = None) -> list[Pair[Cell]]:
        """
        ========================================================================
         Return a list of pairs of cells from the grid.
        ========================================================================
        """
        predicate = lambda x, y: x.distance(other=y) >= min_distance
        tries = tries if tries is not None else size * 100
        return pairs(items=self._grid,
                     size=size,
                     predicate=predicate,
                     tries=tries)
