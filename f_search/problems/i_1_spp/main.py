from f_search.problems import ProblemSearch
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from f_search.problems.mixins import HasStart, HasGoal


class ProblemSPP(ProblemSearch, HasStart, HasGoal):
    """
    ============================================================================
     One-to-One Shortest-Path-Problem on a Grid.
    ============================================================================
    """
    
    # Factory
    Factory = None

    def __init__(self,
                 grid: Grid | str,
                 start: State,
                 goal: State,
                 name: str = 'ProblemSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemSearch.__init__(self, grid=grid, name=name)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)

    def __str__(self) -> str:
        """
        ========================================================================
         Return the STR-REPR of the ProblemSPP.
        ========================================================================
        """
        return f'{self.name}(Grid={str(self.grid)}, Start={str(self.start)}, Goal={str(self.goal)})'
