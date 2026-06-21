from f_hs.state import StateBase
from f_ds.grids import CellMap as Cell
from typing import Self


class StateCell(StateBase[Cell]):
    """
    ========================================================================
     Search State wrapping a CellMap for Grid-Based Pathfinding.
    ========================================================================
    """

    def __init__(self, key: Cell) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        StateBase.__init__(self, key=key)

    @property
    def rc(self) -> tuple[int, int]:
        """
        ====================================================================
         Return (Row, Col) of the underlying Cell.
        ====================================================================
        """
        return self.key.rc

    def distance(self, other: Self) -> int:
        """
        ====================================================================
         Return the Manhattan Distance to another StateCell.
        ====================================================================
        """
        return self.key.distance(other.key)
