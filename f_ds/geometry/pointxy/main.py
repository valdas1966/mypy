from f_core.mixins.tupleable import Tupleable


class PointXY(Tupleable):
    """
    ============================================================================
     2-D PointXY (x, y) — a coordinate pair with no fixed frame.
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
         Get the horizontal (x-axis) coordinate.
        ========================================================================
        """
        return self._x

    @property
    def y(self) -> float:
        """
        ========================================================================
         Get the vertical (y-axis) coordinate.
        ========================================================================
        """
        return self._y

    def to_tuple(self) -> tuple[float, float]:
        """
        ========================================================================
         Return the PointXY as an (x, y) tuple.
        ========================================================================
        """
        return self._x, self._y
