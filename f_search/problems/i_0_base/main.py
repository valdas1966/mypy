from f_ds.grids import GridMap as Grid
from f_cs.problem.main import ProblemAlgo
from f_search.ds.state import StateCell as State
from f_ds.grids.grid.registry import GridRegistry


class ProblemSearch(ProblemAlgo):
    """
    ============================================================================
     Base-Class for Search-Problems in Grid's domain.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 # Grid or its name (on heavy cases for lazy loading)
                 grid: Grid | str,
                 name: str = 'ProblemSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemAlgo.__init__(self, name=name)
        self._grid = grid

    @property
    def grid(self) -> Grid:
        """
        ========================================================================
         Return the Problem's Grid.
        ========================================================================
        """
        if isinstance(self._grid, str):
            self._grid = GridRegistry.get(name=self._grid)
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
