from f_abstract.mixins.nameable import Nameable
from f_data_structure.f_grid.row_col import RowCol


class GridLayout(Nameable):
    """
    ============================================================================
     Desc: Represents a Grid-Layout generic class.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. num_rows (int)     : Number of Rows in the Grid.
        2. num_cols (int)     : Number of Cols in the Grid.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. shape() -> str
           - Return STR-Representation of the Grid's Shape as (1,2).
        2. is_within(row_col: RowCol) -> bool
           - Returns True if the given (row,col) are in the Grid's borders.
    ============================================================================
    """

    def __init__(self,
                 num_rows: int,
                 num_cols: int = None,
                 name: str = None) -> None:
        Nameable.__init__(self, name)
        self._num_rows = num_rows
        self._num_cols = num_cols or num_rows
        self.name = self.name + self.shape() if self.name else self.shape()

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def num_cols(self) -> int:
        return self._num_cols

    def shape(self) -> str:
        """
        ========================================================================
         Desc: Return STR-REPR of the Grid's Shape as (num_rows,num_cols).
        ========================================================================
        """
        return f'({self._num_rows},{self._num_cols})'

    def is_within(self, row_col: RowCol) -> bool:
        """
        ========================================================================
         Desc: Returns True if the given Location is within the Grid's Borders.
        ========================================================================
        """
        is_valid_row = 0 <= row_col.row < self._num_rows
        is_valid_col = 0 <= row_col.col < self._num_cols
        return is_valid_row and is_valid_col
