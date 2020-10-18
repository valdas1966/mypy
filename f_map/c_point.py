import math
from f_const.directions import Directions


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        """
        ========================================================================
         Description: Return Manhattan-Distance between Self and Other Points.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. other : Point.
        ========================================================================
         Return: int.
        ========================================================================
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __str__(self):
        return f'({self.x},{self.y})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def direction(cls, p1, p2):
        """
        ============================================================================
         Description: Return the Direction from Point_1 to Point_2 in Degrees.
        ============================================================================
         Arguments:
        ----------------------------------------------------------------------------
            1. p1 : Point.
            2. p2 : Point
        ============================================================================
         Return: float (Degree from 0 to 360).
        ============================================================================
        """
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        res = math.atan2(dx*(-1), dy*(-1)) / math.pi * 180
        if res < 0:
            res += 360
        return res

    @classmethod
    def compass_direction(cls, p1, p2):
        """
        ============================================================================
         Description: Return Compass Direction from Point_1 to Point_2.
        ============================================================================
         Arguments:
        ----------------------------------------------------------------------------
            1. p1 : Point.
            2. p1 : Point.
        ============================================================================
         Return: Directions { UP | RIGHT | DOWN | LEFT }.
        ============================================================================
        """
        d = Point.direction(p1, p2)
        if d >= 315 or d <= 45:
            return Directions.UP
        if 45 <= d <= 135:
            return Directions.RIGHT
        if 135 <= d <= 225:
            return Directions.DOWN
        if 225 <= d <= 315:
            return Directions.LEFT

