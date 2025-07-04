from __future__ import annotations


class HasRowCol:
    """
    ============================================================================
     Mixin for classes with Row and Col properties.
    ============================================================================
    """

    def __init__(self,
                 row: int = None,
                 col: int = None) -> None:
        """
        ========================================================================
         1. Inits the Object with received Row and Col arguments.
         2. If the Col is None, it takes the value of Row.
        ========================================================================
        """
        self._row = row if row is not None else 0
        self._col = col if col is not None else self._row

    @property
    # Object's Row
    def row(self) -> int:
        return self._row

    @property
    # Objects Col
    def col(self) -> int:
        return self._col

    def neighbors(self) -> list[HasRowCol]:
        """
        ========================================================================
         Return a List of Neighbor Cells in Clock-Wise Order
           (North, East, South, West).
        ========================================================================
        """
        n_north = self.row - 1, self.col
        n_east = self.row, self.col + 1
        n_south = self.row + 1, self.col
        n_west = self.row, self.col - 1
        return [HasRowCol(n[0], n[1])
                for n
                in (n_north, n_east, n_south, n_west)
                if n[0] >= 0 and n[1] >= 0]

    def key_comparison(self) -> list:
        """
        ========================================================================
         Prioritize Row over the Col in Comparisons (Clock-Wise Order).
        ========================================================================
        """
        return [self.row, self.col]
    
    def to_tuple(self) -> tuple[int, int]:
        """
        ========================================================================
         Return a Tuple of (Row, Col).
        ========================================================================
        """
        return (self.row, self.col)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Object.
         Ex: 'Name(Row,Col)'
        ========================================================================
        """
        return f'({self._row},{self._col})'

    def __hash__(self) -> int:
        """
        ========================================================================
         Return Hash-Value by (Row, Col).
        ========================================================================
        """
        return hash((self.row, self.col))
