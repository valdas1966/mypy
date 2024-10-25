from __future__ import annotations
from f_abstract.mixins.validatable_public import ValidatablePublic
from f_abstract.mixins.has_row_col import HasRowCol


class Cell(HasRowCol, ValidatablePublic):
    """
    ============================================================================
     Represents list Cell in list 2D-Grid.
    ============================================================================
    """

    def __init__(self,
                 row: int = None,
                 col: int = None,
                 is_valid: bool = True
                 ) -> None:
        HasRowCol.__init__(self, row, col)
        ValidatablePublic.__init__(self, is_valid)
