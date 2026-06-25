from f_core.mixins.tupleable import Tupleable


class Point(Tupleable):
    """
    ============================================================================
     2-D Point (x, y) in a normalized 0-100 coordinate space.
    ============================================================================
     x is the horizontal axis (maps to CSS left / SVG x), y is the vertical
     axis (maps to CSS top / SVG y). Equality, ordering, hashing and
     unpacking come from Tupleable via the (x, y) to_tuple().
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 x: float,
                 y: float) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        """
        ========================================================================
         Get the horizontal coordinate (0-100).
        ========================================================================
        """
        return self._x

    @property
    def y(self) -> float:
        """
        ========================================================================
         Get the vertical coordinate (0-100).
        ========================================================================
        """
        return self._y

    def to_tuple(self) -> tuple[float, float]:
        """
        ========================================================================
         Return the Point as an (x, y) tuple.
        ========================================================================
        """
        return self._x, self._y

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Point.
        ========================================================================
        """
        return f'({self._x}, {self._y})'
