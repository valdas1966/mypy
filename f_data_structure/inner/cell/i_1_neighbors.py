from __future__ import annotations
from f_data_structure.inner.cell.i_0_init import CellInit
from f_utils.u_enum import ClockDirection


class CellNeighbors(CellInit):
    """
    ============================================================================
     Desc: XY-Object that returns the adjacent neighbors.
    ============================================================================
    Inherited Properties:
    ----------------------------------------------------------------------------
        1. name (str)            : Cell's Name.
        2. x (int)               : Cell's X-Coordinate.
        3. y (int)               : Cells' Y-Coordinate.
        4. is_valid (bool)       : Cell's Validity (Traversability).
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: Cell) -> int
           - Return the distance between this and other Cell.
              Uses Manhattan distance by default.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. neighbors() -> list[Cell]
           - Return adjacent neighbors (in clockwise order by default).
        2. neighbor_north() -> Cell
           - Returns Cell to the North of current (upward).
        3. neighbor_east() -> Cell
           - Returns Cell to the East of current (leftward).
        4. neighbor_south() -> Cell
           - Returns Cell to the South of current (downward).
        5. neighbor_west() -> Cell
           - Returns Cell to the West of current (rightward).
    ============================================================================
    """

    def __init__(self,
                 x: int | float,
                 y: int | float,
                 clock_direction: ClockDirection = ClockDirection.CLOCKWISE):
        super().__init__(x=x, y=y)
        self._clock_direction = clock_direction

    def neighbors(self) -> list[CellNeighbors]:
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

    def neighbor_north(self) -> CellNeighbors:
        """
        ========================================================================
        Desc: Returns the XYAble object to the north of current (upward).
               Increments y coordinate by 1.
        ========================================================================
        """
        return CellNeighbors(x=self.x, y=self.y + 1)

    def neighbor_south(self) -> CellNeighbors:
        """
        ========================================================================
        Desc: Returns the XYAble object to the south of current (downward).
               Decrements y coordinate by 1.
        ========================================================================
        """
        return CellNeighbors(x=self.x, y=self.y - 1)

    def neighbor_west(self) -> CellNeighbors:
        """
        ========================================================================
        Desc: Returns the XYAble object to the west of current (leftward).
               Decrements x coordinate by 1.
        ========================================================================
        """
        return CellNeighbors(x=self.x - 1, y=self.y)

    def neighbor_east(self) -> Cell.XYNeighbors:
        """
        ========================================================================
        Desc: Returns the XYAble object to the east of current (rightward).
               Increments y coordinate by 1.
        ========================================================================
        """
        return CellNeighbors(x=self.x + 1, y=self.y)
