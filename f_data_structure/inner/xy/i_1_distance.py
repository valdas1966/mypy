from __future__ import annotations
from f_data_structure.inner.xy.i_0_init import XYInit
from f_utils.u_enum import XYDistanceMetric


class XYDistance(XYInit):
    """
    ============================================================================
     Desc: XY-Object with a distance() method to other XY-Object.
            (Default by a Manhattan-Distance metric).
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
         1. x (int|float): Object's X-Coordinate in the 2D-Space.
         2. y (int|float): Object's Y-Coordinate in the 2D-Space.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. distance(other: XYDistance) -> int | float
            Returns the distance between this and other XY obj.
    ============================================================================
    """
    def __init__(self,
                 x: int | float,
                 y: int | float,
                 distance_metric: XYDistanceMetric = XYDistanceMetric.MANHATTAN):
        super().__init__(x=x, y=y)
        self._distance_metric = distance_metric

    def distance(self, other: XYDistance) -> int | float:
        """
        ========================================================================
         Desc: Returns the distance between this and other XY obj.
        ========================================================================
        """
        if self._distance_metric == XYDistanceMetric.MANHATTAN:
            diff_x = abs(self.x - other.x)
            diff_y = abs(self.y - other.y)
            return diff_x + diff_y
