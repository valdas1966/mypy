from __future__ import annotations
from typing import Sequence
from f_core.mixins.validatable_public import ValidatablePublic
from f_core.mixins.has_row_col import HasRowCol


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

    @staticmethod
    def invalidate(cells: Sequence[Cell]) -> None:
        """
        ========================================================================
         Invalidate multiple cells.
        ========================================================================
        """
        for cell in cells:
            cell.set_invalid()
            