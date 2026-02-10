from f_core.mixins.has.row_col import HasRowCol
from f_core.mixins.has.name import HasName


class CellBase(HasRowCol, HasName):
    """
    ============================================================================
     Base-Class for Cells in a 2D-Grid.
    ============================================================================
    """

    # Factory
    Factory = None

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
        HasRowCol.__init__(self, row=row, col=col)
        HasName.__init__(self, name=name)

    def key_comparison(self) -> tuple[int, int]:
        """
        ========================================================================
         Return the key for comparison between two CellBase objects.
        ========================================================================
        """
        return HasRowCol.key_comparison(self)

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation of the CellBase object.
        ========================================================================
        """
        return f'{self.name}({self.row},{self.col})'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the representation of the CellBase object.
        ========================================================================
        """
        return f'<{type(self).__name__}: Name={self.name}, Row={self.row}, Col={self.col}>'
