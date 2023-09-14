from f_data_structure.f_grid.cell import Cell
from f_data_structure.mixins.traversable import Traversable
from f_const.u_enum import CoordinateSystem


class CellTraversable(Cell, Traversable):
    """
    ============================================================================
     Desc: Represents a Traversable-Cell in the Grid.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. row : int     (Cell's Row in the Grid).
        2. col : int     (Cell's Col in the Grid).
        3. name : str    (Cell's Name).
    ============================================================================
    """

    def __init__(self,
                 row: int,
                 col: int = None,
                 name: str = None,
                 coordinate_system: CoordinateSystem =
                 CoordinateSystem.CARTESIAN,
                 is_traversable: bool = True
                 ) -> None:
        Cell.__init__(self, row, col, name, coordinate_system)
        Traversable.__init__(self, is_traversable)
