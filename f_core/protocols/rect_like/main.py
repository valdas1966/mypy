from typing import Protocol


class RectLike(Protocol):
    """
    ========================================================================
     Protocol for objects that can be converted to a math rectangle.
    ========================================================================
    """

    def to_rect_coords(self) -> tuple[int, int, int, int]:
        """
        ====================================================================
         Return the X-Min, Y-Min, X-Max, Y-Max values as a tuple.
        ====================================================================
        """
        ...
