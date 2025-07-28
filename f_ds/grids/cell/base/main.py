from f_core.mixins.has.row_col import HasRowCol
from f_core.mixins.has.name import HasName


class CellBase(HasName, HasRowCol):
    """
    ============================================================================
     Base-Class for Cells in a 2D-Grid.
    ============================================================================
    """

    def __init__(self,
                 # Cell's Row
                 row: int,
                 # Cell's Column
                 col: int,
                 # Cell's Name
                 name: str = 'Cell') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        HasRowCol.__init__(self, row=row, col=col)

    def __str__(self) -> str:
        """
        ========================================================================
         Return a String Representation of the Cell.
        ========================================================================
        """
        return f'{self.name}{HasRowCol.__str__(self)}'
