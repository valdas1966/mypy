from __future__ import annotations
from f_abstract.mixins.nameable import Nameable


class XYInit(Nameable):
    """
    ============================================================================
     Desc: Represents a Nameable object with a (x,Y) position in 2D-Space.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
         1. x (int|float): Object's X-Coordinate.
         2. y (int|float): Object's Y-Coordinate.
    ============================================================================
    """

    def __init__(self,
                 x: int | float,
                 y: int | float,
                 name: str = None) -> None:
        Nameable.__init__(self, name)
        self._x = x
        self._y = y

    def __str__(self) -> str:
        """
        ========================================================================
         Desc: Return STR-Representation of the Object as (X,Y).
        ========================================================================
        """
        name = self._name if self._name else str()
        return f'{name}({self.x},{self.y})'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: XYInit) -> bool:
        """
        ========================================================================
         Desc: Check if two obj are equal based on their (X,Y) coordinates.
        ========================================================================
        """
        return self.x == other.x and self.y == other.y

    @property
    def x(self) -> int | float:
        return self._x

    @property
    def y(self) -> int | float:
        return self._y
