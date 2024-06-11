from __future__ import annotations
from f_abstract.mixins.validatable import Validatable
from f_abstract.mixins.has_row_col import HasRowCol


class Cell(HasRowCol, Validatable):
    """
    ============================================================================
     Represents a Cell in a 2D-Grid.
    ============================================================================
    """

    def __init__(self,
                 row: int = None,
                 col: int = None,
                 is_valid: bool = True
                 ) -> None:
        HasRowCol.__init__(self, row, col)
        Validatable.__init__(self, is_valid)
