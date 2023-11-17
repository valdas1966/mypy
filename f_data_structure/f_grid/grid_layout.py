from f_abstract.mixins.nameable import Nameable


class GridLayout(Nameable):
    """
    ============================================================================
     Desc: Represents a Grid-Layout generic class.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None) -> None:
        self._rows = rows
        self._cols = cols or rows
        name = name + self.shape() if name else self.shape()
        Nameable.__init__(self, name)

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def total(self) -> int:
        """
        ========================================================================
         Returns a Total-Number of Positions in the Grid.
        ========================================================================
        """
        return self._rows * self._cols

    def shape(self) -> str:
        """
        ========================================================================
         Returns STR-REPR of the Grid's Shape as (num_rows,num_cols).
        ========================================================================
        """
        return f'({self._rows},{self._cols})'

    def is_within(self, row: int, col: int) -> bool:
        """
        ========================================================================
         Returns True if the given Location is within the Grid's Borders.
        ========================================================================
        """
        is_valid_row = 0 <= row < self._rows
        is_valid_col = 0 <= col < self._cols
        return is_valid_row and is_valid_col
