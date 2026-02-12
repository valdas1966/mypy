from f_search.problems.i_0_base.main import ProblemSearch
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from f_search.problems.mixins import HasStart
from typing import Self


class ProblemNeighborhood(ProblemSearch, HasStart):
    """
    ============================================================================
     Neighborhood Problem.
    ============================================================================
    """
    
    # Factory
    Factory: type | None = None

    def __init__(self,
                 grid: Grid | str,
                 start: State,
                 steps_max: int,
                 name: str = 'ProblemNeighborhood') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemSearch.__init__(self, grid=grid, name=name)
        HasStart.__init__(self, start=start)
        self._steps_max = steps_max

    @property
    def steps_max(self) -> int:
        """
        ========================================================================
         Return the maximum step.
        ========================================================================
        """
        return self._steps_max

    def to_light(self) -> Self:
        """
        ========================================================================
         Return a light object (Grid.Name instead of Grid object).
        ========================================================================
        """
        return type(self)(grid=self.grid.name,
                          start=self.start,
                          steps_max=self.steps_max,
                          name=self.name)

    def to_heavy(self, grids: dict[str, Grid]) -> Self:
        """
        ========================================================================
         Return a heavy object (Grid object instead of Grid.Name).
        ========================================================================
        """
        return type(self)(grid=grids[self.grid],
                          start=self.start,
                          steps_max=self.steps_max,
                          name=self.name)
