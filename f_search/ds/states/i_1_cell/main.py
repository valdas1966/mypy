from f_ds.grids.cell import CellMap as Cell
from f_search.ds.states import StateBase


class StateCell(StateBase[Cell]):
    """
    ============================================================================
     State representing a cell in a grid.
    ============================================================================
    """
    
    # Factory
    Factory = None

    def __init__(self,
                 key: Cell,
                 name: str = 'StateCell') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StateBase.__init__(self, key=key, name=name)

    def __str__(self) -> str:
        """
        ========================================================================
         Return the STR-REPR of the StateCell.
        ========================================================================
        """
        return f'({self.key.row},{self.key.col})'
