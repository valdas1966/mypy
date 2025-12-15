from __future__ import annotations
from typing import TYPE_CHECKING
from f_utils.iter.u_iter import pairs

if TYPE_CHECKING:
    from f_ds.grids.grid.map.main import GridMap as Grid, CellMap as Cell


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

    def pairs(self,
              size: int,
              min_distance: int) -> list[tuple[Cell, Cell]]:
        """
        ========================================================================
         Return a list of pairs of cells from the grid.
        ========================================================================
        """
        predicate = lambda x, y: x.distance(other=y) >= min_distance
        tries = size * 100
        return pairs(data=self._grid, size=size, predicate=predicate, tries=tries)
