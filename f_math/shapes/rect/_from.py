from __future__ import annotations
from f_math.shapes.rect.main import Rect
from typing import TypeVar


N = TypeVar('N', int, float)


class From:
    """
    ========================================================================
     Factory class for creating Rect objects from parameters.
    ========================================================================
    """

    @staticmethod
    def Center(x: N, y: N, distance: N) -> Rect:
        """
        ========================================================================
         Create a Rect from a center point and a distance.
        ========================================================================
        """
        top = y - distance
        left = x - distance
        width = (distance * 2) + 1
        height = (distance * 2) + 1
        return Rect(top, left, width, height)
