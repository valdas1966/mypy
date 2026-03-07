class HasRowsCols:
    """
    ============================================================================
     Mixin-Class for Objects with Rows and Cols.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 rows: int,
                 cols: int | None = None) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        self._rows = rows
        self._cols = cols if cols is not None else rows

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

    def shape(self) -> tuple[int, int]:
        """
        ========================================================================
         Return the Shape as a tuple of (rows, cols).
        ========================================================================
        """
        return self._rows, self._cols

    def is_within(self, row: int, col: int) -> bool:
        """
        ========================================================================
         Return True if the given Row and Col are within the Shape.
        ========================================================================
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

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
         Ex: '(5,10)'
        ========================================================================
        """
        return f'({self._rows},{self._cols})'
