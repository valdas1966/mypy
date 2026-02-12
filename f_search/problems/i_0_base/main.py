from f_ds.grids import GridMap as Grid
from f_cs.problem.main import ProblemAlgo
from f_search.ds.state import StateCell as State
from typing import Self


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
    def grid(self) -> Grid | str:
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

    def to_light(self) -> Self:
        """
        ========================================================================
         Return a light object (Grid.Name instead of Grid object).
        ========================================================================
        """
        return type(self)(grid=self.grid.name, name=self.name)

    def to_heavy(self, grids: dict[str, Grid]) -> Self:
        """
        ========================================================================
         Return a heavy object (Grid object instead of Grid.Name).
        ========================================================================
        """
        return type(self)(grid=grids[self.grid], name=self.name)
