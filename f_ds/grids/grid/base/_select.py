from f_ds.grids.grid.base.main import GridBase, Cell


class Select:
    """
    ============================================================================
     Select Class for GridBase.
    ============================================================================
    """

    def __init__(self,
                 grid: GridBase) -> None:
        """
        ========================================================================
         Initialize the Select object.
        ========================================================================
        """
        self._grid = grid

    def random(self, size: int = None, pct: int = None) -> list[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid.
        ========================================================================
        """
        return self._grid.sample(size=size, pct=pct)
