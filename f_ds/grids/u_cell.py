from f_ds.grids.cell import Cell
from typing import Sequence


class UCell:
    """
    ============================================================================
     Cell Utils-Class.
    ============================================================================
    """

    @staticmethod
    def invalidate(*cells: Cell | Sequence[Cell]) -> None:
        """
        ========================================================================
         Invalidate multiple cells.
        ========================================================================
        """
        if len(cells) == 1:
            cells = cells[0]
        for cell in cells:
            cell.set_invalid()
