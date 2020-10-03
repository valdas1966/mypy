import math
from f_const.directions import Directions


def direction(x1, y1, x2, y2):
    """
    ============================================================================
     Description: Return the Direction from Point_1 to Point_2 in Degrees.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. x1 : float (X-Value of Point 1).
        2. y1 : float (Y-Value of Point 1).
        3. x2 : float (X-Value of Point 2).
        4. y2 : float (Y-Value of Point 2).
    ============================================================================
     Return: float (Degree from 0 to 360).
    ============================================================================
    """
    dx = x1 - x2
    dy = y1 - y2
    res = math.atan2(dx*(-1), dy*(-1)) / math.pi * 180
    if res < 0:
        res += 360
    return res


def compass_direction(x1, y1, x2, y2):
    """
    ============================================================================
     Description: Return Compass Direction from Point_1 to Point_2
    Args:
        x1:
        y1:
        x2:
        y2:

    Returns:

    """
    d = direction(x1, y1, x2, y2)
    if d >= 315 or d < 45:
        return Directions.UP
    if 45 <= d < 135:
        return Directions.RIGHT
    if 135 <= d < 225:
        return Directions.DOWN
    if 225 <= d < 315:
        return Directions.LEFT

