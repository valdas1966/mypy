from f_hs.state.i_0_base.main import StateBase
from f_ds.grids.cell.i_1_map import CellMap


class StateCell(StateBase[CellMap]):
    """
    ========================================================================
     Search State wrapping a CellMap for Grid-Based Pathfinding.
    ========================================================================
    """

    def __init__(self, key: CellMap) -> None:
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

    def event_key(self) -> tuple[int, int]:
        """
        ====================================================================
         Canonical comparable representation for recording-test
         normalizers — `(row, col)` tuple unwrapped from the
         underlying CellMap.
        ====================================================================
        """
        return self.rc

    def distance(self, other: 'StateCell') -> int:
        """
        ====================================================================
         Return the Manhattan Distance to another StateCell.
        ====================================================================
        """
        return self.key.distance(other.key)

    def __str__(self) -> str:
        """
        ====================================================================
         Return the String Representation.
        ====================================================================
        """
        return str(self.key)
