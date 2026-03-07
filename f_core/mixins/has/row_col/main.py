from __future__ import annotations
from f_core.mixins.comparable import Comparable
from f_core.mixins.hashable import Hashable
from f_core.protocols.rect_like import RectLike
from typing import Self


class HasRowCol(Comparable, Hashable):
    """
    ============================================================================
     Mixin for classes with Row and Col properties.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 row: int | None = None,
                 col: int | None = None) -> None:
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
        """
        ========================================================================
         Return the object's row.
        ========================================================================
        """
        return self._row

    @property
    # Objects Col
    def col(self) -> int:
        """
        ========================================================================
         Return the object's column.
        ========================================================================
        """
        return self._col

    def neighbors(self) -> list[Self]:
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
        return [type(self)(n[0], n[1])
                for n
                in (n_north, n_east, n_south, n_west)
                if n[0] >= 0 and n[1] >= 0]

    def distance(self, other: Self) -> int:
        """
        ========================================================================
         Return Manhattan-Distance from Self to the Other.
        ========================================================================
        """
        dist_row = abs(self.row - other.row)
        dist_col = abs(self.col - other.col)
        return dist_row + dist_col

    def is_within(self,
                  rect: RectLike | None = None,
                  row_min: int | None = None,
                  col_min: int | None = None,
                  row_max: int | None = None,
                  col_max: int | None = None) -> bool:
        """
        ========================================================================
         Return True if the object is within the given Rect or range.
        ========================================================================
        """
        if rect:
            row_min, col_min, row_max, col_max = rect.to_rect_coords()
        if any(v is None for v in (row_min, col_min, row_max, col_max)):
            raise ValueError('Provide rect or all of row_min, col_min, '
                             'row_max, col_max')
        row_valid: bool = row_min <= self.row <= row_max
        col_valid: bool = col_min <= self.col <= col_max
        return row_valid and col_valid

    @property
    def key(self) -> tuple[int, int]:
        """
        ========================================================================
         Prioritize Row over the Col in Comparisons (Clock-Wise Order).
        ========================================================================
        """
        return self.row, self.col

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Object.
         Ex: 'Name(Row,Col)'
        ========================================================================
        """
        return f'({self._row},{self._col})'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return REPR-REPR of the Object.
         Ex: '<HasRowCol: Row=1, Col=2>'
        ========================================================================
        """
        return f'<{type(self).__name__}: Row={self._row}, Col={self._col}>'
