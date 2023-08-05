from __future__ import annotations
from f_const.u_enum import DistanceMetric
from f_const.u_enum import CoordinateSystem
from f_abstract.interfaces.nameable import Nameable


class LocationRowCol(Nameable):
    """
    ============================================================================
     Desc: Represents a Location in a Grid.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. row (int)             : Row-Position in the Grid.
        2. col (int)             : Col-Position in the Grid.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. distance(other: LocationRowCol) -> int
           - Returns distance between this and other LocationRowCol
    ============================================================================
    """

    def __init__(self,
                 row: int,
                 col: int = None,
                 name: str = None,
                 coordinate_system: CoordinateSystem = CoordinateSystem.CARTESIAN
                 ) -> None:
        Nameable.__init__(self, name)
        self._row = row
        self._col = row if col is None else col
        self._coordinate_system = coordinate_system

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    def distance(self,
                 other: LocationRowCol,
                 metric: DistanceMetric = DistanceMetric.MANHATTAN
                 ) -> int:
        """
        ========================================================================
         Desc: Returns the distance between this and other LocationRowCol.
        ========================================================================
        """
        if metric == DistanceMetric.MANHATTAN:
            diff_row = abs(self.row - other.row)
            diff_col = abs(self.col - other.col)
            return diff_row + diff_col

    def __eq__(self, other: LocationRowCol) -> bool:
        return self.row == other.row and self.col == other.col

    def __lt__(self, other: LocationRowCol) -> bool:
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            if self.row < other.row:
                return True
            elif self.row == other.row:
                return self.col < other.col

    def __le__(self, other: LocationRowCol) -> bool:
        return self < other or self == other

    def __gt__(self, other: LocationRowCol) -> bool:
        return not (self <= other)

    def __ge__(self, other: LocationRowCol) -> bool:
        return not (self < other)
