from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f_ds.grids.grid.map import GridMap as Grid, CellMap as Cell


class Select:
    """
    ============================================================================
     Select-Class for selecting Cells in a Grid.
    ============================================================================
    """

    def __init__(self, grid: Grid) -> None:
        """
        ========================================================================
         Initialize the Select-Class.
        ========================================================================
        """
        self._grid = grid

    def cells_random(self,
                     size: int = None,
                     pct: int = None) -> list[Cell]:
        """
        ========================================================================
         Return a list of random cells from the grid by size or percentage.
        ========================================================================
        """
        group = self._grid.to_group(name="Random-Cells")
        selected = group.sample(size=size, pct=pct)
        return selected.data
