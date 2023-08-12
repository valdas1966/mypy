from __future__ import annotations
from f_data_structure.f_grid.row_col import RowCol
from f_const.u_enum import ClockDirection, CoordinateSystem


class Cell(RowCol):
    """
    ============================================================================
     Desc: Represents a Cell in the Grid.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. neighbors(direction: ClockDirection = CLOCKWISE) -> list[Cell]
           - Return the adjacent neighbors.
    ============================================================================
    """

    def neighbors(self,
                  direction: ClockDirection = ClockDirection.CLOCKWISE
                  ) -> list[Cell]:
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

    def _neighbor_north(self) -> Cell:
        """
        ========================================================================
        Desc: Return the adjacent Cell to the North (upward).
        ========================================================================
        """
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return Cell(self.row + 1, self.col)

    def _neighbor_south(self) -> Cell:
        """
        ========================================================================
        Desc: Return the adjacent Cell to the South (downward).
        ========================================================================
        """
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return Cell(self.row - 1, self.col)

    def _neighbor_west(self) -> Cell:
        """
        ========================================================================
        Desc: Return the adjacent Cell to the West (leftward).
        ========================================================================
        """
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return Cell(self.row, self.col - 1)

    def _neighbor_east(self) -> Cell:
        """
        ========================================================================
        Desc: Return the adjacent Cell to the East (rightward).
        ========================================================================
        """
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return Cell(self.row, self.col + 1)
