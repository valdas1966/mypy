from __future__ import annotations
from f_abstract.mixins.sortable import Sortable


class HasRowsCols(Sortable):
    """
    ============================================================================
     Mixin-Class for Objects with Rows and Cols.
    ============================================================================
    """

    def __init__(self, rows: int, cols: int = None) -> None:
        self._rows = rows
        self._cols = cols if cols else rows

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def shape(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Object's Shape.
         Ex: '(1,2)'
        ========================================================================
        """
        return f'({self.rows},{self.cols})'

    def is_within(self, row: int, col: int) -> bool:
        """
        ========================================================================
         Return True if the given Row and Col are within the Shape.
        ========================================================================
        """
        return 0 <= row < self.rows and 0 <= col <= self.cols

    def key_comparison(self) -> list:
        """
        ========================================================================
         1. First comparison by the size of the shape.
         2. Second by the object's rows.
        ========================================================================
        """
        return [len(self), self.rows]

    def __len__(self) -> int:
        """
        ========================================================================
         Return the Flat-Length of the Object.
        ========================================================================
        """
        return self.rows * self.cols

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Object's Shape.
         Ex: '(1,2)'
        ========================================================================
        """
        return self.shape()

    def __repr__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Object's Shape.
         Ex: '<HasRowsCols>(1,2)'
        ========================================================================
        """
        return f'<{self.__class__.__name__}: {str(self)}>'
