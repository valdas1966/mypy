from f_search.problems.i_0_base.main import ProblemSearch
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from f_search.problems.mixins import HasStart


class ProblemNeighborhood(ProblemSearch, HasStart):
    """
    ============================================================================
     Neighborhood Problem.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 grid: Grid,
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
