from __future__ import annotations
from f_data_structure.inner.xy.i_0_init import XYInit
from f_utils.u_enum import CoordinateSystem


class XYOrder(XYInit):
    """
    ============================================================================
     Desc: Ordered XY object (default by Cartesian-Coordinate-System).
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
        1. x (int|float): Object's X-Coordinate in the 2D-Space.
        2. y (int|float): Object's Y-Coordinate in the 2D-Space.
    ============================================================================
    """

    def __init__(self,
                 x: int | float,
                 y: int | float,
                 coordinate_system: CoordinateSystem = CoordinateSystem.CARTESIAN):
        super().__init__(x=x, y=y)
        self._coordinate_system = coordinate_system

    def __lt__(self, other: XYOrder) -> bool:
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __le__(self, other: XYOrder) -> bool:
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return self < other or self == other

    def __gt__(self, other: XYOrder) -> bool:
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return not (self <= other)

    def __ge__(self, other: XYOrder) -> bool:
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return not (self < other)
