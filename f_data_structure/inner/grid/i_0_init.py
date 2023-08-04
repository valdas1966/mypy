from f_abstract.interfaces.nameable import Nameable
from f_data_structure.cell import Cell


class GridInit(Nameable):
    """
    ============================================================================
     Desc: Represents a Nameable Grid Class.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. num_rows (int) : Number of Rows in the Grid.
        2. num_cols (int) : Number of Cols in the Grid.
    ============================================================================
    """

    def __init__(self,
                 num_rows: int,
                 num_cols: int = None,
                 name: str = None
                 ) -> None:
        Nameable.__init__(self, name)
        self._num_rows = num_rows
        self._num_cols = num_cols if num_cols else num_rows
        self._grid = [[Cell(x, y) for y in range(num_cols)]
                      for x in range(num_rows)]

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def num_cols(self) -> int:
        return self._num_cols
