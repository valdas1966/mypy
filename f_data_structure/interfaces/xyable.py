
class XYAble:
    """
    ============================================================================
     Desc: Represents an Object with a (x,Y) position in 2D-Space.
            Can calculate distances to other XYAble objects.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
         1. x (int): Object's X-Coordinate in the 2D-Space.
         2. y (int): Object's Y-Coordinate in the 2D-Space.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. distance(other: XYAble) -> int : Return Manhattan-Distance between
                                              this and other XYAble object.
        2. neighbors() -> list[XYAble]    : Return adjacent neighbors in
                                             clockwise order.
    ============================================================================
    """

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def distance(self, other: 'XYAble') -> int:
        """
        ========================================================================
         Desc: Returns the Manhattan-Distance between this and other XYAble obj.
        ========================================================================
        """
        diff_x = abs(self.x - other.x)
        diff_y = abs(self.y - other.y)
        return diff_x + diff_y

    def neighbors(self) -> list['XYAble']:
        """
        ========================================================================
         Desc: Returns List[XYAble] of adjacent neighbors in clockwise order.
        ========================================================================
        """
        return [self.neighbor_north(),
                self.neighbor_east(),
                self.neighbor_south(),
                self.neighbor_west()]

    def neighbor_north(self) -> 'XYAble':
        """
        ========================================================================
        Desc: Returns the XYAble object to the north of current (upward).
               Increments y coordinate by 1.
        ========================================================================
        """
        return XYAble(x=self.x, y=self.y + 1)

    def neighbor_south(self) -> 'XYAble':
        """
        ========================================================================
        Desc: Returns the XYAble object to the south of current (downward).
               Decrements y coordinate by 1.
        ========================================================================
        """
        return XYAble(x=self.x, y=self.y - 1)

    def neighbor_west(self) -> 'XYAble':
        """
        ========================================================================
        Desc: Returns the XYAble object to the west of current (leftward).
               Decrements x coordinate by 1.
        ========================================================================
        """
        return XYAble(x=self.x - 1, y=self.y)

    def neighbor_east(self) -> 'XYAble':
        """
        ========================================================================
        Desc: Returns the XYAble object to the east of current (rightward).
               Increments y coordinate by 1.
        ========================================================================
        """
        return XYAble(x=self.x + 1, y=self.y)

    def __str__(self) -> str:
        """
        ========================================================================
         Desc: Return STR-Representation of the Object as (X,Y).
        ========================================================================
        """
        return f'({self.x},{self.y})'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: 'XYAble') -> bool:
        """
        ========================================================================
         Desc: Check if two obj are equal based on their (X,Y) coordinates.
        ========================================================================
        """
        return self.x == other.x and self.y == other.y

    def __nq__(self, other: 'XYAble') -> bool:
        """
        ========================================================================
         Desc: Check if two obj are not equal based on their (X,Y) coordinates.
        ========================================================================
        """
        return not self.__eq__(other=other)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y
