from f_data_structure.inner.xy.i_1_order import XYOrder
from f_data_structure.inner.xy.i_1_distance import XYDistance
from f_const.u_enum import CoordinateSystem


class XY(XYOrder, XYDistance):
    """
    ============================================================================
     Desc: XY Nameable object that is also Orderable (default by cartesian
            coordinate system) and can calculate its distance to other XY obj.
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
        1. name (str)         : Object's Name.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. x (int|float)      : Object's X-Coordinate.
        2. y (int|float)      : Object's Y-Coordinate.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. distance(other: XY) -> int|float
           - Returns the distance between this object and another XY object.
              Uses Manhattan distance by default.
    ============================================================================
    """

    def __init__(self,
                 x: int | float,
                 y: int | float,
                 name: str = None,
                 coordinate_system: CoordinateSystem = CoordinateSystem.CARTESIAN
                 ) -> None:
        XYOrder.__init__(self, x, y, name, coordinate_system)
