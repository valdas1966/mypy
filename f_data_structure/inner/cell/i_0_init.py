from f_abstract.interfaces.nameable import Nameable
from f_abstract.interfaces.validatable import Validatable
from f_data_structure.xy import XY


class CellInit(Nameable, Validatable, XY):
    """
    ============================================================================
     Desc: Represents a Cell object with a Name and Coordinates in a Grid.
           The Cell can be either Validatable (traversable) or not.
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
        1. name (str)            : Cell's Name.
        2. x (int)               : Cell's X-Coordinate.
        3. y (int)               : Cells' Y-Coordinate.
        4. is_valid (bool)       : Cell's Validity (Traversability).
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: Cell) -> int
           - Return the distance between this and other Cell.
              Uses Manhattan distance by default.
    ============================================================================
    """

    def __init__(self,
                 x: int,                       # Cell's X-Coordinate
                 y: int,                       # Cell's Y-Coordinate
                 name: str = None,             # Cell's Name (Optional)
                 is_valid: bool = True         # Cell's Traversability
                 ) -> None:
        Nameable.__init__(self, name=name)
        Validatable.__init__(self, is_valid=is_valid)
        XY.__init__(self, x=x, y=y)

    def __str__(self):
        """
        ========================================================================
         Desc: Returns Cell's STR-Representation in format of "Name(X,Y)" or
                "(X,Y)" when Name is None.
        ========================================================================
        """
        return f'{Nameable.__str__(self)}{XY.__str__(self)}'
