from __future__ import annotations
from f_data_structure.inner.cell.i_0_init import CellInit
from f_const.u_enum import ClockDirection


class CellNeighbors(CellInit):
    """
    ============================================================================
     Desc: Cell object that returns the adjacent neighbors.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. neighbors(direction: ClockDirection = CLOCKWISE) -> list[Cell]
           - Return the adjacent neighbors.
    ============================================================================
    """

    def neighbors(self,
                  direction: ClockDirection = ClockDirection.CLOCKWISE
                  ) -> list[CellNeighbors]:
        """
        ========================================================================
         Desc: Returns List[Cell] of adjacent neighbors in clockwise order.
        ========================================================================
        """
        if direction == ClockDirection.CLOCKWISE:
            return [self._neighbor_north(),
                    self._neighbor_east(),
                    self._neighbor_south(),
                    self._neighbor_west()]

    def _neighbor_north(self) -> CellNeighbors:
        """
        ========================================================================
        Desc: Return the adjacent Cell to the North (upward).
        ========================================================================
        """
        return CellNeighbors(x=self.x, y=self.y + 1)

    def _neighbor_south(self) -> CellNeighbors:
        """
        ========================================================================
        Desc: Return the adjacent Cell to the South (downward).
        ========================================================================
        """
        return CellNeighbors(x=self.x, y=self.y - 1)

    def _neighbor_west(self) -> CellNeighbors:
        """
        ========================================================================
        Desc: Return the adjacent Cell to the West (leftward).
        ========================================================================
        """
        return CellNeighbors(x=self.x - 1, y=self.y)

    def _neighbor_east(self) -> CellNeighbors:
        """
        ========================================================================
        Desc: Return the adjacent Cell to the East (rightward).
        ========================================================================
        """
        return CellNeighbors(x=self.x + 1, y=self.y)
