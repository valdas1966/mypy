from f_ds.grids.cell import Cell


class HasCell:

    def __init__(self, cell: Cell) -> None:
        self._cell = cell

    @property
    def cell(self) -> Cell:
        """
        ========================================================================
         Return the Cell of the Node.
        ========================================================================
        """
        return self._cell
