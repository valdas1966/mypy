from f_abstract.interfaces.nameable import Nameable
from f_data_structure.f_grid.location_row_col import LocationRowCol
from f_math import u_combinatorics


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
        2. is_within(row: int, col: int) -> bool
           - Returns True if the given (row,col) are in the Grid's borders.
    ============================================================================
    """

    def __init__(self,
                 num_rows: int,
                 num_cols: int = None,
                 name: str = None) -> None:
        Nameable.__init__(self, name)
        self._num_rows = num_rows
        self._num_cols = num_cols if num_cols else num_rows

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def num_cols(self) -> int:
        return self._num_cols

    def shape(self) -> str:
        return f'({self._num_rows},{self._num_cols})'

    def is_within(self,
                  row: int = None,
                  col: int = None,
                  loc: LocationRowCol = None) -> bool:
        """
        ========================================================================
         Desc: Returns True if the given Location is within the Grid's Borders.
        ========================================================================
        """
        if loc:
            row, col = loc.row, loc.col
        is_valid_row = 0 <= row < self._num_rows
        is_valid_col = 0 <= col <= self._num_cols
        return is_valid_row and is_valid_col
