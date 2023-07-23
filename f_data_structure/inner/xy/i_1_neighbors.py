from __future__ import annotations
from f_data_structure.inner.xy.i_0_init import XYInit
from f_utils.u_enum import ClockDirection


class XYNeighbors(XYInit):
    """
    ============================================================================
     Desc: XY-Object that returns the adjacent neighbors.
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
         1. x (int|float): Object's X-Coordinate in the 2D-Space.
         2. y (int|float): Object's Y-Coordinate in the 2D-Space.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. neighbors() -> list[XY] : Return adjacent neighbors in clockwise
                                      order by default.
    ============================================================================
    """

    def __init__(self,
                 x: int | float,
                 y: int | float,
                 clock_direction: ClockDirection = ClockDirection.CLOCKWISE):
        super().__init__(x=x, y=y)
        self._clock_direction = clock_direction

    def neighbors(self) -> list[XYNeighbors]:
        """
        ========================================================================
         Desc: Returns List[XY] of adjacent neighbors in clockwise order.
        ========================================================================
        """
        if self._clock_direction == ClockDirection.CLOCKWISE:
            return [self.neighbor_north(),
                    self.neighbor_east(),
                    self.neighbor_south(),
                    self.neighbor_west()]

    def neighbor_north(self) -> XYNeighbors:
        """
        ========================================================================
        Desc: Returns the XYAble object to the north of current (upward).
               Increments y coordinate by 1.
        ========================================================================
        """
        return XYNeighbors(x=self.x, y=self.y + 1)

    def neighbor_south(self) -> XYNeighbors:
        """
        ========================================================================
        Desc: Returns the XYAble object to the south of current (downward).
               Decrements y coordinate by 1.
        ========================================================================
        """
        return XYNeighbors(x=self.x, y=self.y - 1)

    def neighbor_west(self) -> XYNeighbors:
        """
        ========================================================================
        Desc: Returns the XYAble object to the west of current (leftward).
               Decrements x coordinate by 1.
        ========================================================================
        """
        return XYNeighbors(x=self.x - 1, y=self.y)

    def neighbor_east(self) -> XYNeighbors:
        """
        ========================================================================
        Desc: Returns the XYAble object to the east of current (rightward).
               Increments y coordinate by 1.
        ========================================================================
        """
        return XYNeighbors(x=self.x + 1, y=self.y)
