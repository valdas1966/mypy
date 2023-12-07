from __future__ import annotations
from f_abstract.mixins.sortable import Sortable


class HasRowCol(Sortable):
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

    def key_comparison(self) -> list:
        return [self.row, self.col]

    def to_tuple(self) -> tuple[int, int]:
        return self.row, self.col

    def __str__(self) -> str:
        return f'({self._row},{self._col})'

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> str:
        return hash(self.__str__())
