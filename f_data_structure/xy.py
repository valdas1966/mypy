from f_data_structure.inner.xy.i_1_order import XYOrder
from f_data_structure.inner.xy.i_1_distance import XYDistance


class XY(XYOrder, XYDistance):
    """
    ============================================================================
     Desc: XY object that is orderable and can calculate its distance to
            another XY object.
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
        1. x (int|float): Object's X-Coordinate.
        2. y (int|float): Object's Y-Coordinate.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: XY) -> int|float
           - Returns the distance between this object and another XY object.
              Uses Manhattan distance by default.
    ============================================================================
    """

    def __init__(self, x: int | float, y: int | float) -> None:
        XYOrder.__init__(self, x, y)
        XYDistance.__init__(self, x, y)
