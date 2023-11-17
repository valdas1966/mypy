from __future__ import annotations
from f_abstract.mixins.nameable import Nameable


class HasRowCol(Nameable):
    """
    ============================================================================
     Mixin for classes with Row and Col properties.
    ============================================================================
    """

    def __init__(self, row: int = None, col: int = None) -> None:
        """
        ========================================================================
         1. Inits the Object with received Row and Col arguments.
         2. If the Col is None, it takes the value of Row.
        ========================================================================
        """
        self._row = row if row is not None else 0
        self._col = col if col is not None else self._row
        Nameable.__init__(self, name=f'({self._row},{self._col})')

    @property
    # Object's Row
    def row(self) -> int:
        return self._row

    @property
    # Objects Col
    def col(self) -> int:
        return self._col

    def key_comparison(self) -> list:
        return [self.row, self.col]
