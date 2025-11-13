from f_search.problems import ProblemSearch, Grid, State
from f_search.problems.mixins import HasStart, HasGoals
from typing import Iterable


class ProblemOMSPP(ProblemSearch, HasStart, HasGoals):
    """
    ============================================================================
     One-to-Many Shortest-Path-Problem on a Grid.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 grid: Grid,
                 start: State,
                 goals: Iterable[State]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemSearch.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)
        HasGoals.__init__(self, goals=goals)
