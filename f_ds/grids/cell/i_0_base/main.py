from f_core.mixins.has.row_col import HasRowCol
from f_core.mixins.has.name import HasName


class CellBase(HasName, HasRowCol):
    """
    ============================================================================
     Base-Class for Cells in a 2D-Grid.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Cell's Row
                 row: int,
                 # Cell's Column
                 col: int,
                 # Cell's Name
                 name: str = 'CellBase') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        HasRowCol.__init__(self, row=row, col=col)

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by Row, then by Col (Clock-Wise Order).
        ========================================================================
        """
        return HasRowCol.key_comparison(self)

    def __str__(self) -> str:
        """
        ========================================================================
         Return a String Representation of the Cell.
        ========================================================================
        """
        return f'{self.name}{HasRowCol.__str__(self)}'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return a String Representation of the Cell.
        ========================================================================
        """
        return f'<{type(self).__name__}: Name={self.name}, Row={self.row}, Col={self.col}>'

    def __hash__(self) -> int:
        """
        ========================================================================
         Return the Hash of the Cell.
        ========================================================================
        """
        return HasRowCol.__hash__(self)
