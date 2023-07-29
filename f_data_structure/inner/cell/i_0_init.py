from f_data_structure.xy import XY


class CellInit(XY):
    """
    ============================================================================
     Desc: Represents a Cell (XY object with integer x,y coordinates).
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
        1. name (str)            : Cell's Name.
        2. x (int)               : Cell's X-Coordinate.
        3. y (int)               : Cells' Y-Coordinate.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: Cell) -> int
           - Return the distance between this and other Cell.
              Uses Manhattan distance by default.
    ============================================================================
    """
    pass
