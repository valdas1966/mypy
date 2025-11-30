from __future__ import annotations


class HasRowsCols:
    """
    ============================================================================
     Mixin-Class for Objects with Rows and Cols.
    ============================================================================
    """

    RECORD_SPEC = {
        'rows': lambda o: o.rows,
        'cols': lambda o: o.cols,
    }

    def __init__(self,
                 rows: int,
                 cols: int = None) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._rows = rows
        self._cols = cols if cols else rows

    @property
    def rows(self) -> int:
        """
        ========================================================================
         Return the number of rows.
        ========================================================================
        """
        return self._rows

    @property
    def cols(self) -> int:
        """
        ========================================================================
         Return the number of columns.
        ========================================================================
        """
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
        return 0 <= row < self.rows and 0 <= col < self.cols

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

    def __hash__(self) -> int:
        """
        ========================================================================
         Compute Hash-Value by Object's Shape.
        ========================================================================
        """
        return hash((self.rows, self.cols))