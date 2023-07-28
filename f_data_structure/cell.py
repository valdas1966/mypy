from f_data_structure.xy import XY


class Cell(XY):
    """
    ============================================================================
     Desc: Cell object in the Grid.
            Has (x,y) integer coordinates and
             indicates whether the cell is traversable.
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
        1. name (str)            : Cell's Name.
        2. x (int)               : Cell's X-Coordinate.
        3. y (int)               : Cell's Y-Coordinate.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: Cell) -> int
           - Returns the distance between this cell and another.
              Uses Manhattan distance by default.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. is_traversable : bool (Traversable Cell in the Grid).
    ============================================================================
    """

    def __init__(self,
                 x: int,
                 y: int,
                 name: str = None,
                 is_traversable: bool = True) -> None:
        XY.__init__(self, x, y, name)
        self._is_traversable = is_traversable

    @property
    def is_traversable(self) -> bool:
        return self._is_traversable

    @is_traversable.setter
    def is_traversable(self, new_value: bool) -> None:
        self._is_traversable = new_value
