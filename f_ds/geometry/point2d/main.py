from f_core.mixins.tupleable import Tupleable


class Point2D(Tupleable):
    """
    ============================================================================
     2-D integer lattice point (row, col) — a grid-coordinate value object.
    ============================================================================
     A pure coordinate: equality, ordering, hashing, unpacking and indexing
     come from Tupleable via the (row, col) to_tuple(). Unlike HasRowCol it
     carries NO grid behavior (no neighbors / is_within / Manhattan distance)
     — that keeps it a footgun-free coordinate for the Connectivity policy,
     whose movement-model distance must never collide with a stored metric.
     Distinct from geometry.Point, which is a float (x, y) GUI coordinate.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 row: int,
                 col: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._row = row
        self._col = col

    @property
    def row(self) -> int:
        """
        ========================================================================
         Get the row coordinate (vertical axis).
        ========================================================================
        """
        return self._row

    @property
    def col(self) -> int:
        """
        ========================================================================
         Get the col coordinate (horizontal axis).
        ========================================================================
        """
        return self._col

    def to_tuple(self) -> tuple[int, int]:
        """
        ========================================================================
         Return the Point as a (row, col) tuple.
        ========================================================================
        """
        return self._row, self._col

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation. Ex: '(3, 5)'
        ========================================================================
        """
        return f'({self._row}, {self._col})'
