from f_search.problems import ProblemSearch, Grid, State
from f_search.problems.mixins import HasStart, HasGoal


class ProblemSPP(ProblemSearch, HasStart, HasGoal):
    """
    ============================================================================
     One-to-One Shortest-Path-Problem on a Grid.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 grid: Grid,
                 start: State,
                 goal: State) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemSearch.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)
