from __future__ import annotations


class HasRowCol:
    """
    ============================================================================
     Mixin for classes with Row and Col properties.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. str -> '(row, col)'
        2. repr -> str
        3. eq -> (row, col) == (other.row, other.col)
        4. comparison based on row-major system.
    ============================================================================
    """

    _row: int        # Object's Row
    _col: int        # Object's Col

    def __init__(self, row: int, col: int = None) -> None:
        """
        ========================================================================
         1. Inits the Object with received Row and Col arguments.
         2. If the Col is None, it takes the value of Row.
        ========================================================================
        """
        self._row = row
        self._col = row if col is None else col

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    def __str__(self) -> str:
        return f'({self.row},{self.col})'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: HasRowCol) -> bool:
        return (self.row, self.col) == (other.row, other.col)

    def __lt__(self, other: HasRowCol) -> bool:
        return (self.row, self.col) < (other.row, other.col)

    def __le__(self, other: HasRowCol) -> bool:
        return (self.row, self.col) <= (other.row, other.col)

    def __gt__(self, other: HasRowCol) -> bool:
        return (self.row, self.col) > (other.row, other.col)

    def __ge__(self, other: HasRowCol) -> bool:
        return (self.row, self.col) >= (other.row, other.col)
