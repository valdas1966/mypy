from f_search.problems.mixins import HasGrid, HasStart, HasGoal, Grid, State
from f_cs.problem import ProblemAlgo


class ProblemOOSPP(ProblemAlgo,
                   HasGrid,
                   HasStart,
                   HasGoal):
    """
    ============================================================================
     One-to-One Shortest-Path-Problem on a Grid.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 start: State,
                 goal: State) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemAlgo.__init__(self)
        HasGrid.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)
