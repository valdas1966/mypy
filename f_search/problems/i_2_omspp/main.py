from f_search.problems import ProblemSearch
from f_search.problems.i_1_spp.main import ProblemSPP
from f_search.problems.mixins import HasStart, HasGoals
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid
from typing import Self


class ProblemOMSPP(ProblemSearch, HasStart, HasGoals):
    """
    ============================================================================
     One-to-Many Shortest-Path-Problem on a Grid.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 grid: Grid,
                 start: State,
                 goals: list[State],
                 name: str = 'ProblemOMSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemSearch.__init__(self, grid=grid, name=name)
        HasStart.__init__(self, start=start)
        HasGoals.__init__(self, goals=goals)

    @property
    def h_start(self) -> float:
        """
        ========================================================================
         Return avg Manhattan distance from Start to Goals.
        ========================================================================
        """
        goals = self.goals
        return sum(self.start.distance(g) for g in goals) / len(goals)

    @property
    def norm_h_start(self) -> float:
        """
        ========================================================================
         Return normalized h_start [0,100] relative to max Manhattan dist.
        ========================================================================
        """
        return self.grid.norm_distance(distance=self.h_start)

    @property
    def h_goals(self) -> float:
        """
        ========================================================================
         Return avg pairwise Manhattan distance between Goals.
        ========================================================================
        """
        goals = self.goals
        n = len(goals)
        if n < 2:
            return 0.0
        total = sum(goals[i].distance(goals[j])
                    for i in range(n) for j in range(i + 1, n))
        return total / (n * (n - 1) / 2)

    @property
    def norm_h_goals(self) -> float:
        """
        ========================================================================
         Return normalized h_goals [0,100] relative to max Manhattan dist.
        ========================================================================
        """
        return self.grid.norm_distance(distance=self.h_goals)

    def to_analytics(self) -> dict:
        """
        ========================================================================
         Return a dict of analytic values for reporting.
        ========================================================================
        """
        d = ProblemSearch.to_analytics(self)
        d['h_start'] = self.h_start
        d['norm_h_start'] = self.norm_h_start
        d['h_goals'] = self.h_goals
        d['norm_h_goals'] = self.norm_h_goals
        return d

    def to_spps(self) -> list[ProblemSPP]:
        """
        ========================================================================
         Convert the ProblemOMSPP to a list of ProblemSPPs.
        ========================================================================
        """
        sub_problems: list[ProblemSPP] = []
        for goal in self.goals:
            sub_problem = ProblemSPP(grid=self.grid,
                                     start=self.start,
                                     goal=goal)
            sub_problems.append(sub_problem)
        return sub_problems
