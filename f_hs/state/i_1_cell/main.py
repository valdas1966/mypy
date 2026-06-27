from f_hs.state import StateBase
from f_ds.grids import CellMap as Cell


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

    def to_tuple(self) -> tuple[int, int]:
        """
        ====================================================================
         Return (Row, Col) of the underlying Cell.
        ====================================================================
        """
        return self.key.to_tuple()
