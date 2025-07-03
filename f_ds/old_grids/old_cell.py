from __future__ import annotations
from typing import Sequence, Iterable
from f_core.mixins.validatable_public import ValidatablePublic
from f_core.mixins.has_row_col import HasRowCol
from f_ds.old_grids.old_cell.map.distance import Distance


class Cell(HasRowCol, ValidatablePublic):
    """
    ============================================================================
     Cell in the 2D-Grid.
    ============================================================================
    """

    def __init__(self,
                 row: int = None,
                 col: int = None,
                 is_valid: bool = True
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasRowCol.__init__(self, row, col)
        ValidatablePublic.__init__(self, is_valid)
        self._distance = Distance

    @property
    def distance(self) -> type:
        """
        ========================================================================
         Return the Distance-Class.
        ========================================================================
        """
        return self._distance
    
    @staticmethod
    def invalidate(cells: Sequence[Cell]) -> None:
        """
        ========================================================================
         Invalidate multiple cells.
        ========================================================================
        """
        for cell in cells:
            cell.set_invalid()
            