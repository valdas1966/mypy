from f_data_structure.inner.cell.i_1_traversable import CellTraversable
from f_data_structure.inner.cell.i_1_neighbors import CellNeighbors


class Cell(CellTraversable, CellNeighbors):
    """
    ============================================================================
     Desc: Represents Cell in the Grid (XY object with int [x,y] coordinates).
            It indicates whether it is Traversable and can provide a list of
             its adjacent Cell-Neighbors.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. is_traversable : bool (Traversable Cell in the Grid).
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. neighbors(ClockDirection=CLOCKWISE) -> list[Cell]
           - Returns List of Cell-Neighbors (in default by ClockWise direction).
    ============================================================================
    """
    pass
