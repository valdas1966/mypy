from f_hs.state import StateResource as State
from f_hs.state import NodeResource
from f_ds.grids import CellMap as Cell


class Factory:
    """
    ============================================================================
     Factory for StateResource test instances.
    ============================================================================
    """

    @staticmethod
    def at(row: int, col: int = None, resource: int = 0) -> State:
        """
        ========================================================================
         Create a StateResource at (row, col) with the given resource.
        ========================================================================
        """
        col = row if col is None else col
        cell = Cell(row=row, col=col)
        node = NodeResource(node=cell, resource=resource)
        return State(key=node)
