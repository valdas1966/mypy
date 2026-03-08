from f_ds.grids import GridMap as Grid
from f_cs.problem.main import ProblemAlgo
from f_search.ds.state import StateCell as State


class ProblemSearch(ProblemAlgo):
    """
    ============================================================================
     Base-Class for Search-Problems in Grid's domain.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 grid: Grid,
                 name: str = 'ProblemSearch') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemAlgo.__init__(self, name=name)
        self._grid = grid
        self._name_grid = grid.name

    @property
    def grid(self) -> Grid:
        """
        ========================================================================
         Return the Problem's Grid.
        ========================================================================
        """
        if self._grid is None:
            raise ValueError(
                f'Grid not loaded: {self._name_grid}')
        return self._grid

    @property
    def name_grid(self) -> str:
        """
        ========================================================================
         Return the Grid's Name.
        ========================================================================
        """
        return self._name_grid

    def successors(self, state: State) -> list[State]:
        """
        ========================================================================
         Return the successors of the given state.
        ========================================================================
        """
        cells = self.grid.neighbors(cell=state.key)
        states = [State(key=cell) for cell in cells]
        return states

    def to_analytics(self) -> dict:
        """
        ========================================================================
         Return a dict of analytic values for reporting.
        ========================================================================
        """
        return self.grid.to_analytics()

    def load_grid(self, grids: dict[str, Grid]) -> None:
        """
        ========================================================================
         Load the Grid from the given dict.
        ========================================================================
        """
        self._grid = grids[self._name_grid]

    def __getstate__(self) -> dict:
        """
        ========================================================================
         Exclude the heavy Grid from pickle.
        ========================================================================
        """
        state = self.__dict__.copy()
        state['_grid'] = None
        return state
