from f_core.mixins.has.record import HasRecord
from f_ds.grids import GridMap as Grid
from f_cs.problem import ProblemAlgo
from f_search.ds.states import StateCell as State


class ProblemSearch(ProblemAlgo, HasRecord):
    """
    ============================================================================
     Base-Class for Search-Problems in Grid's domain.
    ============================================================================
    """

    RECORD_SPEC = {
        'grid': lambda o: o.grid.record
    }

    # Factory
    Factory = None

    def __init__(self, grid: Grid, name: str = 'ProblemSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemAlgo.__init__(self, name=name)
        HasRecord.__init__(self, name=name)
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
        states = [State(key=cell) for cell in cells]
        return states
