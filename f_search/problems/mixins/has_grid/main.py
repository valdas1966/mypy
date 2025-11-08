from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_search.state import State


class HasGrid:
    """
    ============================================================================
     Base-Class for Grid-Problems in Search.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, grid: Grid) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._grid = grid

    @property
    def grid(self) -> Grid:
        """
        ========================================================================
         Return the Problem's Grid.
        ========================================================================
        """
        return self._grid

    def successors(self, state: State) -> list[State]:
        """
        ========================================================================
         Return the successors of the given state.
        ========================================================================
        """
        cells = self.grid.neighbors(cell=state.key)
        states = [State[Cell](key=cell) for cell in cells]
        return states
