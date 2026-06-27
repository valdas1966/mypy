from f_core.mixins.tupleable.main import Tupleable


class Factory:
    """
    ============================================================================
     Factory for the Tupleable class.
    ============================================================================
    """

    class Coord(Tupleable):
        def __init__(self, x: int, y: int) -> None:
            self._x, self._y = x, y
        def to_tuple(self) -> tuple[int, int]:
            return self._x, self._y

    @staticmethod
    def coord_12() -> Tupleable:
        """
        ========================================================================
         Create a Tupleable object with the tuple (1, 2).
        ========================================================================
        """
        return Factory.Coord(x=1, y=2)

    @staticmethod
    def coord_34() -> Tupleable:
        """
        ========================================================================
         Create a Tupleable object with the tuple (3, 4).
        ========================================================================
        """
        return Factory.Coord(x=3, y=4)
