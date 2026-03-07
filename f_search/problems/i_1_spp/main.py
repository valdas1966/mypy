from f_search.problems import ProblemSearch
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from f_search.problems.mixins import HasStart, HasGoal
from typing import Self


class ProblemSPP(ProblemSearch, HasStart, HasGoal):
    """
    ============================================================================
     One-to-One Shortest-Path-Problem on a Grid.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 grid: Grid,
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

    @property
    def h_start(self) -> int:
        """
        ========================================================================
         Return Manhattan distance between Start and Goal.
        ========================================================================
        """
        return self.start.distance(other=self.goal)

    @property
    def norm_h_start(self) -> float:
        """
        ========================================================================
         Return normalized distance [0,100] relative to max Manhattan dist.
        ========================================================================
        """
        return self.grid.norm_distance(distance=self.h_start)

    def to_analytics(self) -> dict:
        """
        ========================================================================
         Return a dict of analytic values for reporting.
        ========================================================================
        """
        d = ProblemSearch.to_analytics(self)
        d['h_start'] = self.h_start
        d['norm_h_start'] = self.norm_h_start
        return d

    def reverse(self, name: str = None) -> Self:
        """
        ========================================================================
         Return a reversed Problem (Start and Goal swapped).
        ========================================================================
        """
        name = name if name else self.name
        return type(self)(grid=self.grid,
                          start=self.goal,
                          goal=self.start,
                          name=name)
