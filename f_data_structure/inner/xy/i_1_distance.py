from __future__ import annotations
from f_data_structure.inner.xy.i_0_init import XYInit
from f_const.u_enum import XYDistanceMetric


class XYDistance(XYInit):
    """
    ============================================================================
     Desc: Distantable XY object (Default by a Manhattan-Distance metric).
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. distance(other: XY,
                    metric: XYDistanceMetric = Manhattan) -> int | float
            Returns the distance between this and other XY obj.
    ============================================================================
    """

    def distance(self,
                 other: XYDistance,
                 metric: XYDistanceMetric = XYDistanceMetric.MANHATTAN
                 ) -> int | float:
        """
        ========================================================================
         Desc: Returns the distance between this and other XY obj.
        ========================================================================
        """
        if metric == XYDistanceMetric.MANHATTAN:
            diff_x = abs(self.x - other.x)
            diff_y = abs(self.y - other.y)
            return diff_x + diff_y
